import os
import time
import logging
from typing import Any, Dict, List, Optional

import numpy as np
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException, Header, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .it_logging import setup_logging
from search_api._shared.health import make_healthz, make_readyz, probe_http
from starlette_exporter import PrometheusMiddleware, handle_metrics
from search_api.common.request_id import RequestIdMiddleware
try:
    from search_api._shared.obs.otel_boot import setup_otel
except Exception:
    def setup_otel(*args, **kwargs):
        return None

from .metrics import (
    SEARCH_ERRORS,
    SEARCH_LATENCY,
    SEARCH_REQUESTS,
    RERANK_LATENCY,
    RERANK_REQS,
)

from opensearchpy import OpenSearch

from search_api.auth import user_from_token
from search_api.opa import allow
from .config import Settings
from . import rerank as rr

settings = Settings()
logger = logging.getLogger(__name__)

app = FastAPI(title="InfoTerminal Search API", version="0.3.0")
setup_logging(app, service_name="search-api")
app.state.service_name = "search-api"
app.state.version = os.getenv("GIT_SHA", "dev")
app.state.start_ts = time.monotonic()
setup_otel(app, service_name=app.state.service_name, version=app.state.version)
app.add_middleware(RequestIdMiddleware)
if os.getenv("IT_ENABLE_METRICS") == "1":
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenSearch(settings.os_url)

@app.get("/healthz")
def healthz():
    return make_healthz(app.state.service_name, app.state.version, app.state.start_ts)

@app.get("/readyz")
def readyz(verbose: int = 0):
    checks: Dict[str, Dict[str, Any]] = {}
    if os.getenv("IT_FORCE_READY") != "1":
        os_url = os.getenv("OPENSEARCH_URL")
        if os_url:
            url = f"{os_url.rstrip('/')}/_cluster/health"
            checks["opensearch"] = probe_http(url)
        else:
            checks["opensearch"] = {"status": "skipped", "latency_ms": None, "error": None, "reason": "missing config"}
    payload, status = make_readyz(app.state.service_name, app.state.version, app.state.start_ts, checks)
    return JSONResponse(payload, status_code=status)




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


class QueryRequest(BaseModel):
    q: Optional[str] = None
    filters: Dict[str, List[str]] = {}
    facets: List[str] = []
    sort: Optional[Dict[str, str]] = None
    knn: Optional[Dict[str, Any]] = None
    limit: int = 20
    offset: int = 0


@app.post("/query")
def query_endpoint(body: QueryRequest, response: Response, x_rerank: Optional[int] = Header(None, alias="X-Rerank"), user=Depends(oidc_user)):
    if not allow(user, "read", {"classification": "public", "type": "search"}):
        raise HTTPException(403, "forbidden")

    must = []
    if body.q:
        must.append({"multi_match": {"query": body.q, "fields": ["title^2", "body", "entities.name^3"]}})

    filters = []
    for field, values in (body.filters or {}).items():
        if values:
            filters.append({"terms": {field: values}})

    if must or filters:
        bool_q: Dict[str, Any] = {}
        if must:
            bool_q["must"] = must
        if filters:
            bool_q["filter"] = filters
        query: Dict[str, Any] = {"bool": bool_q}
    else:
        query = {"match_all": {}}

    body_os: Dict[str, Any] = {"query": query, "size": body.limit, "from": body.offset}

    if body.facets:
        body_os["aggs"] = {f: {"terms": {"field": f, "size": 20}} for f in body.facets}

    if body.sort and body.sort.get("field"):
        body_os["sort"] = [{body.sort["field"]: {"order": body.sort.get("order", "asc")}}]

    if settings.knn_enabled and body.knn:
        body_os["knn"] = {
            "field": body.knn.get("field"),
            "query_vector": body.knn.get("vector"),
            "k": body.knn.get("k", 10),
            "num_candidates": body.knn.get("k", 10),
        }

    res = client.search(index=settings.os_index, body=body_os)
    hits = res.get("hits", {})
    raw_hits = hits.get("hits", [])
    items = [{"id": h.get("_id"), "score": h.get("_score"), **(h.get("_source") or {})} for h in raw_hits]

    raw_aggs = res.get("aggregations", {}) or {}
    facets: Dict[str, List[Dict[str, Any]]] = {}
    for f in body.facets or []:
        buckets = raw_aggs.get(f, {}).get("buckets", [])
        facets[f] = [{"key": b.get("key"), "doc_count": b.get("doc_count", 0)} for b in buckets]

    total = hits.get("total", {})
    total_val = total.get("value") if isinstance(total, dict) else total

    return {
        "items": items,
        "total": total_val or 0,
        "aggregations": facets,
        "tookMs": res.get("took", 0),
    }

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
    do_rerank = False
    try:
        entity_types = [s for s in (entity_type.split(",") if entity_type else []) if s]
        with SEARCH_LATENCY.time():
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
                RERANK_REQS.inc()
                with RERANK_LATENCY.time():
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
        SEARCH_ERRORS.labels(type=e.__class__.__name__).inc()
        raise HTTPException(500, f"search error: {e}")
    finally:
        SEARCH_REQUESTS.labels(rerank="1" if do_rerank else "0").inc()
