try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

import time
import logging
from typing import Optional, List

import numpy as np

from fastapi import FastAPI, Depends, HTTPException, Header, Query, Response
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation
except Exception:  # pragma: no cover - optional
    class FastAPIInstrumentation:  # type: ignore
        def instrument_app(self, app):
            return app

try:
    from prometheus_client import make_asgi_app
except Exception:  # pragma: no cover - optional
    def make_asgi_app():
        from fastapi import FastAPI
        return FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch

from auth import user_from_token
from opa import allow
from .config import Settings
from . import rerank as rr

settings = Settings()
logger = logging.getLogger(__name__)

app = FastAPI(title="InfoTerminal Search API", version="0.3.0")
FastAPIInstrumentation().instrument_app(app)
app.mount("/metrics", make_asgi_app())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenSearch(settings.os_url)


def oidc_user(authorization: Optional[str] = Header(None)):
    if not settings.require_auth:
        return {"sub": "dev", "roles": ["analyst"]}
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    return user_from_token(authorization.split(" ", 1)[1])


def _filters_query(entity_types: List[str] | None):
    must = []
    if entity_types:
        must.append(
            {
                "nested": {
                    "path": "entities",
                    "query": {"terms": {"entities.type": entity_types}},
                }
            }
        )
    return {"bool": {"must": must}} if must else {"match_all": {}}


def _aggs():
    return {
        "entity_types": {
            "nested": {"path": "entities"},
            "aggs": {"types": {"terms": {"field": "entities.type", "size": 20}}},
        }
    }


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(
    q: str,
    response: Response,
    entity_type: Optional[str] = Query(None, description="comma-separated entity types"),
    rerank: Optional[int] = Query(None),
    x_rerank: Optional[int] = Header(None, alias="X-Rerank"),
    user=Depends(oidc_user),
):
    if not allow(user, "read", {"classification": "public", "type": "search"}):
        raise HTTPException(403, "forbidden")
    try:
        entity_types = [s for s in (entity_type.split(",") if entity_type else []) if s]
        query_body = {
            "bool": {
                "must": [{"multi_match": {"query": q, "fields": ["title^2", "body", "entities.name^3"]}}],
                "filter": [_filters_query(entity_types)],
            }
        }
        res = client.search(index=settings.os_index, body={"query": query_body, "aggs": _aggs(), "size": 20})
        hits = res.get("hits", {}).get("hits", [])
        aggs = res.get("aggregations", {})
        facets = {
            "entity_types": [
                {"key": b["key"], "count": b["doc_count"]}
                for b in aggs.get("entity_types", {}).get("types", {}).get("buckets", [])
            ]
        }
        items = [{"id": h["_id"], "score": h["_score"], **h["_source"]} for h in hits]

        do_rerank = (
            settings.rerank_enabled
            and (rerank == 1 or x_rerank == 1)
            and len(items) > 1
            and q and len(q.strip()) > 2
        )
        if do_rerank:
            start = time.time()
            topk = min(settings.rerank_topk, len(items))
            provider = rr.EmbeddingProvider(settings.rerank_model)
            try:
                query_text = q
                query_vec = rr.get_query_embedding(provider, query_text)
                doc_texts = [
                    (items[i].get("snippet") or items[i].get("body") or items[i].get("title") or "")[:1024]
                    for i in range(topk)
                ]
                doc_vecs = np.vstack([
                    rr.get_doc_embedding(provider, items[i]["id"], doc_texts[i]) for i in range(topk)
                ])
                ranks = rr.cosine_rank(query_vec, doc_vecs)
                cos_scores = [r[1] for r in ranks]
                bm25_scores = [items[r[0]]["score"] for r in ranks]
                norm_cos = rr.normalize(cos_scores)
                norm_bm = rr.normalize(bm25_scores)
                blended = [0.7 * norm_cos[i] + 0.3 * norm_bm[i] for i in range(len(ranks))]
                scored = []
                for (idx, cos), final in zip(ranks, blended):
                    item = items[idx]
                    item.setdefault("meta", {})["rerank"] = {
                        "cosine": float(cos),
                        "blended": float(final),
                    }
                    item["score"] = float(final)
                    scored.append((idx, final))
                # reorder
                sorted_items = [items[i] for i, _ in sorted(scored, key=lambda x: x[1], reverse=True)]
                reranked_items = sorted_items + items[topk:]
                elapsed = int((time.time() - start) * 1000)
                if elapsed <= settings.rerank_timeout_ms:
                    items = reranked_items
                    response.headers["X-Reranked"] = "1"
                    response.headers["X-Rerank-TopK"] = str(topk)
                    response.headers["X-Rerank-Model"] = settings.rerank_model
                    response.headers["X-Rerank-TimeMs"] = str(elapsed)
                    logger.debug(
                        "rerank topk=%s elapsed=%sms cache=%s",
                        topk,
                        elapsed,
                        rr.cache_stats,
                    )
                else:
                    logger.warning("rerank timeout after %sms", elapsed)
            except Exception as e:
                logger.warning("rerank failed: %s", e)

        return {"results": items, "facets": facets}
    except Exception as e:
        raise HTTPException(500, f"search error: {e}")
