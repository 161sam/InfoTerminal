try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

import os, json, secrets
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Query
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import make_asgi_app
import psycopg2

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
def conn():
  import psycopg2
  return psycopg2.connect(**PG)

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
import os as _gv_os
if _gv_os.getenv("INIT_DB_ON_STARTUP","1")=="1":
    init()

app = FastAPI(title="Graph Views API", version="0.1.0")
FastAPIInstrumentor().instrument_app(app)
app.mount("/metrics", make_asgi_app())

def user_from_header(x_user: Optional[str]):  # simple dev-mode
  return x_user or "dev"

@app.get("/healthz")
def health(): return {"ok": True}

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
    if not row: raise HTTPException(404,"not found")
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
    if not row: raise HTTPException(404,"not found")
    if row[0]!=user: raise HTTPException(403,"forbidden")
    fields=["name","nodes","edges","positions","is_public"]
    sets=[]; vals=[]
    for f in fields:
      if f in payload:
        sets.append(f"{f}=%s"); vals.append(json.dumps(payload[f]) if f in ("nodes","edges","positions") else payload[f])
    if not sets: return {"updated":0}
    vals.append(vid)
    cur.execute(f"UPDATE graph_views SET {', '.join(sets)}, updated_at=now() WHERE id=%s", vals)
  return {"updated":1}

@app.post("/views/{vid}/share")
def share_view(vid:int, x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  token = secrets.token_urlsafe(16)
  with conn() as c, c.cursor() as cur:
    cur.execute("UPDATE graph_views SET is_public=TRUE, share_token=%s WHERE id=%s AND owner=%s RETURNING id",(token,vid,user))
    if not cur.fetchone(): raise HTTPException(403,"forbidden")
  return {"token": token, "share_url": f"/views/{vid}?token={token}"}

@app.delete("/views/{vid}")
def delete_view(vid:int, x_user: Optional[str]=Header(None)):
  user=user_from_header(x_user)
  with conn() as c, c.cursor() as cur:
    cur.execute("DELETE FROM graph_views WHERE id=%s AND owner=%s RETURNING id",(vid,user))
    if not cur.fetchone(): raise HTTPException(403,"forbidden")
  return {"deleted":1}
