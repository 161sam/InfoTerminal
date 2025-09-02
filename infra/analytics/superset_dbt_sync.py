import os, json, time, requests, pathlib
U = os.getenv("SUPERSET_URL", "http://superset.analytics.svc.cluster.local:8088")
USER = os.getenv("SUPERSET_USER","admin")
PASS = os.getenv("SUPERSET_PASS","adminadmin")
DB_NAME = os.getenv("SUPERSET_DB_NAME","infoterminal_pg")
SQLA = os.getenv("SQLALCHEMY_URI", f"postgresql+psycopg2://{os.getenv('PG_USER','app')}:{os.getenv('PG_PASS','app')}@{os.getenv('PG_HOST','postgres-postgresql.data.svc.cluster.local')}:{os.getenv('PG_PORT','5432')}/{os.getenv('PG_DB','infoterminal')}")

ART_DIR = pathlib.Path(os.getenv("DBT_ARTIFACTS", "etl/dbt/target"))
MANIFEST = ART_DIR / "manifest.json"
CATALOG  = ART_DIR / "catalog.json"

s = requests.Session()
def login():
    r=s.post(f"{U}/api/v1/security/login", json={"username":USER,"password":PASS,"provider":"db"}); r.raise_for_status()
    s.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})

def ensure_db():
    # get or create database
    r=s.get(f"{U}/api/v1/database/?q=%7B%22page_size%22:1000%7D").json()
    for d in r["result"]:
        if d["database_name"]==DB_NAME: return d["id"]
    r=s.post(f"{U}/api/v1/database/", json={"database_name":DB_NAME,"sqlalchemy_uri":SQLA,"expose_in_sqllab":True})
    r.raise_for_status(); return r.json()["id"]

def ensure_dataset(db_id, schema, table_name):
    q = {"filters":[{"col":"table_name","opr":"eq","value":table_name},{"col":"schema","opr":"eq","value":schema}]}
    r=s.get(f"{U}/api/v1/dataset/?q={requests.utils.quote(json.dumps(q))}").json()
    if r["count"]>0: return r["result"][0]["id"]
    r=s.post(f"{U}/api/v1/dataset/", json={"database":db_id,"schema":schema,"table_name":table_name})
    r.raise_for_status(); return r.json()["id"]

def ensure_chart(ds_id, name, viz_type, params):
    q={"filters":[{"col":"slice_name","opr":"eq","value":name}]}
    r=s.get(f"{U}/api/v1/chart/?q={requests.utils.quote(json.dumps(q))}").json()
    payload={"slice_name":name,"viz_type":viz_type,"params":json.dumps(params),"datasource_id":ds_id,"datasource_type":"table"}
    if r["count"]>0:
        cid=r["result"][0]["id"]
        s.put(f"{U}/api/v1/chart/{cid}", json=payload)
        return cid
    r=s.post(f"{U}/api/v1/chart/", json=payload); r.raise_for_status(); return r.json()["id"]

def ensure_dashboard(title, chart_ids):
    q={"filters":[{"col":"dashboard_title","opr":"eq","value":title}]}
    r=s.get(f"{U}/api/v1/dashboard/?q={requests.utils.quote(json.dumps(q))}").json()
    if r["count"]==0:
        r=s.post(f"{U}/api/v1/dashboard/", json={"dashboard_title":title,"published":True})
        r.raise_for_status()
    dash=s.get(f"{U}/api/v1/dashboard/?q={requests.utils.quote(json.dumps(q))}").json()["result"][0]
    dash_id=dash["id"]
    # simple layout: one row with all charts
    cells=[(f"CHART_{i}", cid) for i,cid in enumerate(chart_ids)]
    layout={"DASHBOARD_VERSION_KEY":"v2","ROOT_ID":{"type":"ROOT","id":"ROOT_ID","children":["GRID_ID"]},"GRID_ID":{"type":"GRID","id":"GRID_ID","children":["ROW0"]},"ROW0":{"type":"ROW","id":"ROW0","children":[k for k,_ in cells]}}
    for k,cid in cells:
        layout[k]={"type":"CHART","id":k,"children":[],"meta":{"chartId":cid}}
    s.put(f"{U}/api/v1/dashboard/{dash_id}", json={"position_json":json.dumps(layout)})
    return dash_id

def main():
    assert MANIFEST.exists(), f"Missing {MANIFEST}"
    login()
    db_id = ensure_db()
    mani = json.loads(MANIFEST.read_text())
    # pick dbt models
    models=[]
    for k,v in mani["nodes"].items():
        if v.get("resource_type")!="model": continue
        schema=v.get("schema") or v.get("fqn",[None,])[0]
        name=v.get("name")
        if not schema or not name: continue
        models.append((schema,name))
    # upsert datasets
    ds_ids={}
    for schema,name in models:
        ds_ids[name]=ensure_dataset(db_id, schema, name)
    # opinionated charts
    charts=[]
    if "fct_eod_prices" in ds_ids:
        charts.append(ensure_chart(
            ds_ids["fct_eod_prices"],
            "OpenBB Close by Symbol",
            "echarts_timeseries_line",
            {"time_range":"No filter","metrics":["avg__close"],"groupby":["symbol"],"granularity_sqla":"as_of_date","x_axis":"as_of_date"}
        ))
    if "dim_asset_enriched" in ds_ids:
        charts.append(ensure_chart(
            ds_ids["dim_asset_enriched"],
            "Asset Directory",
            "table",
            {"all_columns":["symbol","isin"],"order_by_cols":[]}
        ))
    if charts:
        ensure_dashboard("OpenBB Overview (dbt sync)", charts)
    print(f"Synced {len(models)} models, {len(charts)} charts.")

if __name__=="__main__":
    main()
