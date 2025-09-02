try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

import os
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Header, Query
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation
from prometheus_client import make_asgi_app
from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch
from auth import user_from_token
from opa import allow

OS_URL = os.getenv("OS_URL", "http://localhost:9200")
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "0") == "1"
INDEX = os.getenv("OS_INDEX", "docs")

app = FastAPI(title="InfoTerminal Search API", version="0.3.0")
FastAPIInstrumentation().instrument_app(app)
app.mount("/metrics", make_asgi_app())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
client = OpenSearch(OS_URL)

def oidc_user(authorization: Optional[str] = Header(None)):
    if not REQUIRE_AUTH: return {"sub":"dev","roles":["analyst"]}
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    return user_from_token(authorization.split(" ",1)[1])

def _filters_query(entity_types: List[str]|None):
    must = []
    if entity_types:
        must.append({
            "nested": {
              "path": "entities",
              "query": { "terms": { "entities.type": entity_types } }
            }
        })
    return {"bool": {"must": must}} if must else {"match_all": {}}

def _aggs():
    return {
      "entity_types": {
        "nested": { "path": "entities" },
        "aggs": { "types": { "terms": { "field": "entities.type", "size": 20 } } }
      }
    }

@app.get("/healthz")
def health(): return {"status":"ok"}

@app.get("/search")
def search(
    q: str,
    entity_type: Optional[str] = Query(None, description="comma-separated entity types"),
    user=Depends(oidc_user)
):
    if not allow(user, "read", {"classification":"public", "type":"search"}):
        raise HTTPException(403, "forbidden")
    try:
        entity_types = [s for s in (entity_type.split(",") if entity_type else []) if s]
        query = {
          "bool": {
            "must": [{"multi_match": {"query": q, "fields": ["title^2","body","entities.name^3"]}}],
            "filter": [_filters_query(entity_types)]
          }
        }
        res = client.search(index=INDEX, body={"query": query, "aggs": _aggs(), "size": 20})
        hits = res.get("hits", {}).get("hits", [])
        aggs = res.get("aggregations", {})
        facets = {
          "entity_types": [
            {"key": b["key"], "count": b["doc_count"]}
            for b in aggs.get("entity_types", {}).get("types", {}).get("buckets", [])
          ]
        }
        return {"results":[{"id":h["_id"], "score":h["_score"], **h["_source"]} for h in hits], "facets": facets}
    except Exception as e:
        raise HTTPException(500, f"search error: {e}")
