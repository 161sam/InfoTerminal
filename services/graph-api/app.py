try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

import os
from typing import Optional
from fastapi import FastAPI, Depends, Header, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation
from prometheus_client import make_asgi_app
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase
from auth import user_from_token
from opa import allow

NEO4J_URI = os.getenv("NEO4J_URI","bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER","neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS","neo4jpass")
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH","0") == "1"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

app = FastAPI(title="InfoTerminal Graph API", version="0.1.0")
FastAPIInstrumentation().instrument_app(app)
app.mount("/metrics", make_asgi_app())
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
  allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

def oidc_user(authorization: Optional[str] = Header(None)):
    if not REQUIRE_AUTH: return {"sub":"dev","roles":["analyst"]}
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401,"missing bearer token")
    return user_from_token(authorization.split(" ",1)[1])

@app.get("/healthz")
def health():
    with driver.session() as s:
        s.run("RETURN 1").consume()
    return {"status":"ok"}

@app.get("/neighbors")
def neighbors(node_id: str, limit: int = 20, user=Depends(oidc_user)):
    if not allow(user,"read",{"classification":"public","type":"graph"}):
        raise HTTPException(403,"forbidden")
    q = """
    MATCH (n {id: $id})-[r]-(m)
    RETURN n, type(r) as rel, m
    LIMIT $limit
    """
    with driver.session() as s:
        recs = s.run(q, id=node_id, limit=limit)
        out=[]
        for r in recs:
            out.append({
              "from": dict(r["n"]),
              "rel": r["rel"],
              "to": dict(r["m"])
            })
        return out

@app.get("/shortest_path")
def shortest_path(src: str, dst: str, maxlen:int=6, user=Depends(oidc_user)):
    if not allow(user,"read",{"classification":"public","type":"graph"}):
        raise HTTPException(403,"forbidden")
    q = """
    MATCH (a {id:$src}), (b {id:$dst}),
    p = shortestPath((a)-[*..$maxlen]-(b))
    RETURN p
    """
    with driver.session() as s:
        rec = s.run(q, src=src, dst=dst, maxlen=maxlen).single()
        if not rec: return {"path":[]}
        p = rec["p"]
        return {
          "nodes":[dict(n) for n in p.nodes],
          "rels":[{"type": r.type, "start": p.nodes[p.relationships.index(r)].get("id"), "end": p.nodes[p.relationships.index(r)+1].get("id")} for r in p.relationships]
        }
