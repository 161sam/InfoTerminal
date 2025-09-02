import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch

OS_URL = os.getenv("OS_URL", "http://localhost:9200")

app = FastAPI(title="InfoTerminal Search API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenSearch(OS_URL)

def oidc_user():
    # TODO: validate Bearer token (Keycloak JWKS). For bootstrap we allow anonymous read.
    return {"sub": "dev-user", "roles": ["analyst"]}

@app.get("/healthz")
def health():
    return {"status":"ok"}

@app.get("/search")
def search(q: str, user=Depends(oidc_user)):
    try:
        res = client.search(index="docs", body={
            "query": {"multi_match": {"query": q, "fields": ["title^2","body","entities.name^3"]}},
            "size": 20
        })
        hits = res.get("hits", {}).get("hits", [])
        return [{"id": h["_id"], "score": h["_score"], **h["_source"]} for h in hits]
    except Exception as e:
        raise HTTPException(500, f"search error: {e}")
