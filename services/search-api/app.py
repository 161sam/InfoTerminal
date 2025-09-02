import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch
from typing import Optional
from auth import user_from_token
from opa import allow

OS_URL = os.getenv("OS_URL", "http://localhost:9200")
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "0") == "1"

app = FastAPI(title="InfoTerminal Search API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenSearch(OS_URL)

def oidc_user(authorization: Optional[str] = Header(None)):
    if not REQUIRE_AUTH:
        return {"sub":"dev","roles":["analyst"]}
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    token = authorization.split(" ",1)[1]
    try:
        return user_from_token(token)
    except Exception as e:
        raise HTTPException(401, f"auth failed: {e}")

@app.get("/healthz")
def health():
    return {"status":"ok"}

@app.get("/search")
def search(q: str, user=Depends(oidc_user)):
    # Policy: read public resources
    if not allow(user, "read", {"classification":"public"}):
        raise HTTPException(403, "forbidden")
    try:
        res = client.search(index="docs", body={
            "query": {"multi_match": {"query": q, "fields": ["title^2","body","entities.name^3"]}},
            "size": 20
        })
        hits = res.get("hits", {}).get("hits", [])
        return [{"id": h["_id"], "score": h["_score"], **h["_source"]} for h in hits]
    except Exception as e:
        raise HTTPException(500, f"search error: {e}")
