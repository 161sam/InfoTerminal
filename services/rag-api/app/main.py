import os
from typing import List, Optional, Dict, Any

import structlog
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .opensearch_client import OSClient
from .neo4j_client import Neo4jClient
import re
from typing import Optional


logger = structlog.get_logger()


class LawDoc(BaseModel):
    id: str
    title: Optional[str] = None
    paragraph: Optional[str] = None
    text: str
    domain: Optional[str] = None
    source: Optional[str] = None
    effective_date: Optional[str] = None


class RetrieveResponse(BaseModel):
    total: int
    items: List[Dict[str, Any]]


class ContextResponse(BaseModel):
    entity: str
    laws: List[Dict[str, Any]]


def get_env(name: str, default: str) -> str:
    return os.getenv(name, default)


app = FastAPI(title="RAG API", version="0.1.0", description="Legal/Compliance retrieval and graph helpers")

OS_URL = get_env("OS_URL", "http://opensearch:9200")
OS_INDEX = get_env("RAG_OS_INDEX", "laws")

NEO4J_URI = get_env("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = get_env("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = get_env("NEO4J_PASSWORD", "neo4j")

os_client = OSClient(OS_URL, OS_INDEX)
neo = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    checks = {}
    try:
        checks["opensearch"] = os_client.ping()
    except Exception as e:
        checks["opensearch"] = {"status": "fail", "error": str(e)}
    try:
        ok = neo.ping()
        checks["neo4j"] = {"status": "ok" if ok else "fail"}
    except Exception as e:
        checks["neo4j"] = {"status": "fail", "error": str(e)}
    status = all(v.get("status") == "ok" for v in checks.values())
    return {"status": "ready" if status else "not_ready", "checks": checks}, (200 if status else 503)


def _basic_rerank(query: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Simple term-coverage reranker: boost items with more query token hits."""
    q_tokens = [t for t in query.lower().split() if len(t) > 1]
    def score_item(it: Dict[str, Any]) -> float:
        text = f"{it.get('title','')} {it.get('paragraph','')} {it.get('text','')}".lower()
        hits = sum(1 for t in q_tokens if t in text)
        return (it.get('score') or 0.0) + hits * 0.25
    return sorted(items, key=score_item, reverse=True)


def _dot(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    return sum((a[i] or 0.0) * (b[i] or 0.0) for i in range(n))


@app.get("/law/retrieve", response_model=RetrieveResponse)
def retrieve_laws(q: str = Query(..., min_length=2), top_k: int = 10, rerank: int = 0):
    """Retrieve relevant law paragraphs from OpenSearch index."""
    res = os_client.search(q, top_k=top_k)
    items = res["items"]
    if rerank == 1:
        items = _basic_rerank(q, items)
    elif rerank == 2:
        # embedding dot-product rerank (client-side)
        qvec = os_client._embed(q)
        items = sorted(items, key=lambda it: _dot(qvec, it.get('vector') or []), reverse=True)
    return {"total": res["total"], "items": items}


@app.get("/law/knn", response_model=RetrieveResponse)
def retrieve_laws_knn(q: str = Query(..., min_length=2), k: int = 10):
    res = os_client.knn_search(q, k)
    return {"total": res["total"], "items": res["items"]}


class KNNVectorRequest(BaseModel):
    vector: list[float]
    k: int = 10
    filters: Optional[dict] = None


@app.post("/law/knn_vector", response_model=RetrieveResponse)
def knn_by_vector(body: KNNVectorRequest):
    res = os_client.knn_search_vector(body.vector, body.k, body.filters)
    return {"total": res["total"], "items": res["items"]}


class HybridRequest(BaseModel):
    q: str
    top_k: int = 10
    k: int = 10
    alpha: float = 0.5  # weight for BM25 vs kNN
    filters: Optional[dict] = None


@app.post("/law/hybrid", response_model=RetrieveResponse)
def hybrid_search(req: HybridRequest):
    # text search
    s = os_client.search(req.q, top_k=req.top_k, filters=req.filters)
    # knn
    k = os_client.knn_search(req.q, k=req.k, filters=req.filters)
    # normalize and combine
    bm = {it['id']: (it.get('score') or 0.0, it) for it in s['items']}
    km = {it['id']: (it.get('score') or 0.0, it) for it in k['items']}
    max_b = max((v[0] for v in bm.values()), default=1.0)
    max_k = max((v[0] for v in km.values()), default=1.0)
    combined = {}
    for id_, (sc, it) in bm.items():
        combined.setdefault(id_, {'doc': it, 'b': 0.0, 'k': 0.0})
        combined[id_]['b'] = sc / (max_b or 1.0)
    for id_, (sc, it) in km.items():
        combined.setdefault(id_, {'doc': it, 'b': 0.0, 'k': 0.0})
        combined[id_]['k'] = sc / (max_k or 1.0)
    alpha = max(0.0, min(1.0, req.alpha))
    items = []
    for id_, comp in combined.items():
        score = alpha * comp['b'] + (1 - alpha) * comp['k']
        doc = comp['doc']
        doc = dict(doc)
        doc['hybrid_score'] = score
        items.append(doc)
    items.sort(key=lambda x: x.get('hybrid_score', 0.0), reverse=True)
    items = items[: req.top_k]
    return {"total": len(items), "items": items}


@app.get("/law/context", response_model=ContextResponse)
def law_context(entity: str = Query(..., min_length=2), top_k: int = 10):
    """Return relevant laws for an entity. Tries graph links; falls back to text retrieval by entity name."""
    # First try graph links
    linked = neo.get_laws_for_entity(entity, limit=top_k)
    if linked:
        return {"entity": entity, "laws": linked}
    # Fallback: search text by entity name
    res = os_client.search(entity, top_k=top_k)
    return {"entity": entity, "laws": res["items"]}


@app.post("/law/index")
def index_law(doc: LawDoc):
    """Index a law paragraph into OpenSearch (idempotent upsert)."""
    ok = os_client.index_doc(doc.model_dump())
    if not ok:
        raise HTTPException(500, "Indexing failed")
    return {"status": "indexed", "id": doc.id}


@app.post("/graph/law/upsert")
def upsert_law_graph(
    doc: LawDoc,
    applies_to: Optional[List[str]] = None,
    sectors: Optional[List[str]] = None,
    firms: Optional[List[str]] = None,
):
    """Upsert a Law node and optional relations in Neo4j (LEGAL-2)."""
    neo.ensure_schema()
    # Backwards compat: 'applies_to' is treated as sectors
    applies_to_sectors = sectors or applies_to or []
    applies_to_firms = firms or []
    neo.upsert_law(doc.model_dump(), applies_to_sectors=applies_to_sectors, applies_to_firms=applies_to_firms)
    return {"status": "upserted", "law_id": doc.id, "sectors": applies_to_sectors, "firms": applies_to_firms}


@app.post("/events/extract")
def extract_events(body: Dict[str, Any]):
    text = (body.get("text") or "")
    # naive patterns for date-like tokens and verbs
    dates = re.findall(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b", text)
    verbs = [w for w in text.split() if w.endswith(('te', 'ten', 't'))]
    events = []
    if dates:
        events.append({"type": "dated_event", "date": dates[0], "snippet": text[:200]})
    if any(v.lower().startswith('explod') for v in verbs):
        events.append({"type": "explosion", "snippet": text[:200]})
    return {"events": events}


@app.post("/feedback/label")
def feedback_label(body: Dict[str, Any]):
    os.makedirs("/data/feedback", exist_ok=True)
    path = "/data/feedback/labels.jsonl"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(body, ensure_ascii=False) + "\n")
    return {"status": "ok"}
