try:
    from obs.otel_boot import setup_otel  # type: ignore
except Exception:  # pragma: no cover
    def setup_otel(app, service_name: str = "graph-views"):
        return app

import os, json, secrets, time, sys
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Query
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from it_logging import setup_logging
from contextlib import asynccontextmanager, contextmanager
from psycopg2.pool import SimpleConnectionPool
from pathlib import Path

SERVICE_DIR = Path(__file__).resolve().parent
PARENT_DIR = SERVICE_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _shared.cors import apply_cors, get_cors_settings_from_env
from fastapi.responses import JSONResponse
from _shared.health import make_healthz, make_readyz, probe_db

# --- PG ENV Fallbacks (injected) ---
import os as _os
def _pg_env(*names, default=None):
    for n in names:
        v = _os.getenv(n)
        if v:
            return v
    return default
PG = {
  "host": _pg_env("PG_HOST","PGHOST","POSTGRES_HOST","DB_HOST","DATABASE_HOST","PGHOSTADDR","HOST", default="127.0.0.1"),
  "port": int(_pg_env("PG_PORT","PGPORT","POSTGRES_PORT","DB_PORT","DATABASE_PORT","PORT", default="5432")),
  "dbname": _pg_env("PG_DB","PGDATABASE","POSTGRES_DB","DB_NAME","DATABASE_NAME","PGDATABASE", default="it_graph"),
  "user": _pg_env("PG_USER","PGUSER","POSTGRES_USER","DB_USER","DATABASE_USER", default="it_user"),
  "password": _pg_env("PG_PASS","PGPASSWORD","PG_PASSWORD","POSTGRES_PASSWORD","DB_PASS","DB_PASSWORD","DATABASE_PASSWORD", default="it_pass"),
}
# Connection pool initialised in lifespan
pool: Optional[SimpleConnectionPool] = None

@contextmanager
def conn():
  if pool is None:
    raise RuntimeError("PG pool not ready")
  c = pool.getconn()
  try:
    yield c
  finally:
    pool.putconn(c)

def init():
  with conn() as c, c.cursor() as cur:
    cur.execute("""
      CREATE TABLE IF NOT EXISTS graph_views(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        owner TEXT,
        nodes JSONB NOT NULL,
        edges JSONB NOT NULL,
        positions JSONB,
        is_public BOOLEAN DEFAULT FALSE,
        share_token TEXT UNIQUE,
        created_at TIMESTAMPTZ DEFAULT now(),
        updated_at TIMESTAMPTZ DEFAULT now()
      );
      CREATE INDEX IF NOT EXISTS idx_graph_views_owner ON graph_views(owner);
    """)
def setup_pool():
  return SimpleConnectionPool(1, 5, **PG)

@asynccontextmanager
async def lifespan(app: FastAPI):
  global pool
  try:
    pool = setup_pool()
    app.state.pool = pool
    if os.getenv("INIT_DB_ON_STARTUP","1") == "1":
      init()
  except Exception:
    pool = None
    app.state.pool = None
  yield
  if pool:
    pool.closeall()
    app.state.pool = None


app = FastAPI(title="Graph Views API", version="0.1.0", lifespan=lifespan)
setup_logging(app, service_name="graph-views")
FastAPIInstrumentor().instrument_app(app)
setup_otel(app)
apply_cors(app, get_cors_settings_from_env())

if os.getenv("IT_ENABLE_METRICS") == "1" or os.getenv("IT_OBSERVABILITY") == "1":
  from starlette_exporter import PrometheusMiddleware, handle_metrics

  app.add_middleware(PrometheusMiddleware)
  app.add_route("/metrics", handle_metrics)
app.state.service_name = "graph-views"
app.state.start_ts = time.monotonic()
app.state.version = os.getenv("GIT_SHA", "dev")
@app.get("/healthz")
def healthz():
  return make_healthz(app.state.service_name, app.state.version, app.state.start_ts)

@app.get("/readyz")
def readyz(verbose: int = 0):
  checks: Dict[str, Dict[str, Any]] = {}
  if os.getenv("IT_FORCE_READY") != "1":
    pool = getattr(app.state, "pool", None)
    if pool:
      def _call():
        conn = pool.getconn()
        try:
          with conn.cursor() as cur:
            cur.execute("SELECT 1")
        finally:
          pool.putconn(conn)
      checks["postgres"] = probe_db(_call)
    else:
      checks["postgres"] = {"status": "skipped", "latency_ms": None, "error": None, "reason": "missing config"}
  payload, status = make_readyz(app.state.service_name, app.state.version, app.state.start_ts, checks)
  return JSONResponse(payload, status_code=status)




def user_from_header(x_user: Optional[str]):  # simple dev-mode
  return x_user or "dev"

@app.post("/views")
def create_view(payload: Dict[str, Any], x_user: Optional[str]=Header(None)):
  user = user_from_header(x_user)
  name = payload.get("name") or "Untitled"
  nodes=payload.get("nodes") or []
  edges=payload.get("edges") or []
  positions=payload.get("positions") or {}
  with conn() as c, c.cursor() as cur:
    cur.execute("INSERT INTO graph_views(name,owner,nodes,edges,positions) VALUES(%s,%s,%s,%s,%s) RETURNING id",
                (name,user,json.dumps(nodes),json.dumps(edges),json.dumps(positions)))
    vid = cur.fetchone()[0]
  return {"id": vid}

@app.get("/views")
def list_views(limit:int=50, x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  with conn() as c, c.cursor() as cur:
    cur.execute("SELECT id,name,is_public,created_at,updated_at FROM graph_views WHERE owner=%s ORDER BY updated_at DESC LIMIT %s",(user,limit))
    rows = cur.fetchall()
  return [{"id":r[0],"name":r[1],"is_public":r[2],"created_at":r[3].isoformat(),"updated_at":r[4].isoformat()} for r in rows]

@app.get("/views/{vid}")
def get_view(vid:int, token: Optional[str]=Query(None), x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  with conn() as c, c.cursor() as cur:
    cur.execute("SELECT owner,is_public,share_token,name,nodes,edges,positions FROM graph_views WHERE id=%s",(vid,))
    row = cur.fetchone()
    if not row: raise HTTPException(404,"not found")  # pragma: no branch
  owner,is_public,share_token,name,nodes,edges,positions = row
  if not (user==owner or is_public or (token and token==share_token)):
    raise HTTPException(403,"forbidden")
  return {"id":vid,"name":name,"owner":owner,"nodes":nodes,"edges":edges,"positions":positions,"is_public":is_public}

@app.put("/views/{vid}")
def update_view(vid:int, payload: Dict[str,Any], x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  with conn() as c, c.cursor() as cur:
    cur.execute("SELECT owner FROM graph_views WHERE id=%s",(vid,))
    row = cur.fetchone()
    if not row: raise HTTPException(404,"not found")  # pragma: no branch
    if row[0]!=user: raise HTTPException(403,"forbidden")  # pragma: no branch
    fields=["name","nodes","edges","positions","is_public"]
    sets=[]; vals=[]
    for f in fields:
      if f in payload:
        sets.append(f"{f}=%s"); vals.append(json.dumps(payload[f]) if f in ("nodes","edges","positions") else payload[f])
    if not sets: return {"updated":0}  # pragma: no branch
    vals.append(vid)
    cur.execute(f"UPDATE graph_views SET {', '.join(sets)}, updated_at=now() WHERE id=%s", vals)
  return {"updated":1}

@app.post("/views/{vid}/share")
def share_view(vid:int, x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  token = secrets.token_urlsafe(16)
  with conn() as c, c.cursor() as cur:
    cur.execute("UPDATE graph_views SET is_public=TRUE, share_token=%s WHERE id=%s AND owner=%s RETURNING id",(token,vid,user))
    if not cur.fetchone(): raise HTTPException(403,"forbidden")  # pragma: no branch
  return {"token": token, "share_url": f"/views/{vid}?token={token}"}

@app.delete("/views/{vid}")
def delete_view(vid:int, x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  with conn() as c, c.cursor() as cur:
    cur.execute("DELETE FROM graph_views WHERE id=%s AND owner=%s RETURNING id",(vid,user))
    if not cur.fetchone(): raise HTTPException(403,"forbidden")  # pragma: no branch
  return {"deleted":1}
