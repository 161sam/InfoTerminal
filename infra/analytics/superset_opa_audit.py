import os, json, requests

U = os.getenv("SUPERSET_URL","http://superset.analytics.svc.cluster.local:8088")
USER = os.getenv("SUPERSET_USER","admin")
PASS = os.getenv("SUPERSET_PASS","adminadmin")

DB_NAME="clickhouse_logs"
SQLA = os.getenv("CH_URI","clickhousedb+connect://default:@clickhouse.clickhouse.svc.cluster.local:8123/logs")

s = requests.Session()
def login():
    r = s.post(f"{U}/api/v1/security/login", json={"username":USER,"password":PASS,"provider":"db"})
    r.raise_for_status()
    s.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})

def ensure_db():
    r=s.get(f"{U}/api/v1/database/?q=%7B%22page_size%22:1000%7D").json()
    for d in r["result"]:
        if d["database_name"]==DB_NAME: return d["id"]
    r=s.post(f"{U}/api/v1/database/", json={"database_name":DB_NAME,"sqlalchemy_uri":SQLA,"expose_in_sqllab":True})
    r.raise_for_status(); return r.json()["id"]

def ensure_dataset(db_id, schema, table_name):
    q={"filters":[{"col":"table_name","opr":"eq","value":table_name},{"col":"schema","opr":"eq","value":schema},{"col":"database","opr":"rel_o_m","value":db_id}]}
    r=s.get(f"{U}/api/v1/dataset/?q={requests.utils.quote(json.dumps(q))}").json()
    if r["count"]>0: return r["result"][0]["id"]
    r=s.post(f"{U}/api/v1/dataset/", json={"database":db_id,"schema":schema,"table_name":table_name})
    r.raise_for_status(); return r.json()["id"]

def ensure_chart(ds_id, name, viz_type, params):
    q={"filters":[{"col":"slice_name","opr":"eq","value":name}]}
    r=s.get(f"{U}/api/v1/chart/?q={requests.utils.quote(json.dumps(q))}").json()
    payload={"slice_name":name,"viz_type":viz_type,"params":json.dumps(params),"datasource_id":ds_id,"datasource_type":"table"}
    if r["count"]>0:
        cid=r["result"][0]["id"]; s.put(f"{U}/api/v1/chart/{cid}", json=payload); return cid
    r=s.post(f"{U}/api/v1/chart/", json=payload); r.raise_for_status(); return r.json()["id"]

def ensure_dashboard(title, chart_ids):
    q={"filters":[{"col":"dashboard_title","opr":"eq","value":title}]}
    r=s.get(f"{U}/api/v1/dashboard/?q={requests.utils.quote(json.dumps(q))}").json()
    if r["count"]==0:
        r=s.post(f"{U}/api/v1/dashboard/", json={"dashboard_title":title,"published":True})
        r.raise_for_status()
    dash=s.get(f"{U}/api/v1/dashboard/?q={requests.utils.quote(json.dumps(q))}").json()["result"][0]
    dash_id=dash["id"]
    layout={"DASHBOARD_VERSION_KEY":"v2","ROOT_ID":{"type":"ROOT","id":"ROOT_ID","children":["GRID"]},"GRID":{"type":"GRID","id":"GRID","children":[]}}
    for i,cid in enumerate(chart_ids):
        cid_key=f"CHART_{i}"
        layout["GRID"]["children"].append(cid_key)
        layout[cid_key]={"type":"CHART","id":cid_key,"children":[],"meta":{"chartId":cid}}
    s.put(f"{U}/api/v1/dashboard/{dash_id}", json={"position_json":json.dumps(layout)})
    return dash_id

def main():
    login()
    db_id = ensure_db()
    ds_id = ensure_dataset(db_id, "logs", "opa_decisions")
    charts=[]
    charts.append(ensure_chart(ds_id,"OPA Decisions per Minute","echarts_timeseries_line",{
        "metrics":["count"],"groupby":["__time_grain"],"adhoc_filters":[],"time_grain_sqla":"minute","time_range":"Last 2 hours","x_axis":"__time"
    }))
    charts.append(ensure_chart(ds_id,"Deny Rate %","big_number_total",{
        "metric":"count","adhoc_filters":[{"expressionType":"SIMPLE","subject":"allowed","operator":"==","comparator":"0"}],"subheader":"Denies / All","y_axis_format":",.2f"
    }))
    charts.append(ensure_chart(ds_id,"Top Policies (denies)","table",{
        "all_columns":["path","allowed"],"adhoc_filters":[{"expressionType":"SIMPLE","subject":"allowed","operator":"==","comparator":"0"}],"order_by_cols":["[\"count\", false]"],"row_limit":10
    }))
    charts.append(ensure_chart(ds_id,"Top Users (denies)","table",{
        "all_columns":["user","allowed"],"adhoc_filters":[{"expressionType":"SIMPLE","subject":"allowed","operator":"==","comparator":"0"}],"order_by_cols":["[\"count\", false]"],"row_limit":10
    }))
    ensure_dashboard("OPA Audit (ClickHouse)", charts)
    print("OPA Audit dashboard created.")

if __name__=="__main__":
    main()
