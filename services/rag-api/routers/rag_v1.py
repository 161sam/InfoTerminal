"""
RAG API v1 router for legal document retrieval and graph-based search.
Provides hybrid search, vector search, indexing, and event extraction.
"""

import json
import os
import re
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

# Import shared standards
import sys
from pathlib import Path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from _shared.api_standards.error_schemas import raise_http_error
    from _shared.api_standards.pagination import PaginatedResponse
except ImportError:
    # Fallback for legacy compatibility
    def raise_http_error(code: str, message: str, details: Optional[Dict] = None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail={"error": {"code": code, "message": message, "details": details or {}}})
    
    class PaginatedResponse(BaseModel):
        items: list
        total: int
        page: int = 1
        size: int = 10

# Import models
from ..models import (
    LawDoc,
    RetrieveResponse,
    ContextResponse,
    KNNVectorRequest,
    HybridRequest,
    EfSearchRequest,
    IndexResponse,
    GraphUpsertRequest,
    GraphUpsertResponse,
    ExtractEventsRequest,
    ExtractEventsResponse,
    FeedbackRequest,
    FeedbackResponse,
    SearchParameters,
    KNNSearchParameters,
    ContextSearchParameters
)

# Import clients
from ..app.opensearch_client import OSClient
from ..app.neo4j_client import Neo4jClient

router = APIRouter(tags=["RAG API"], prefix="/v1")

# Initialize clients
def get_opensearch_client():
    """Get OpenSearch client instance."""
    os_url = os.getenv("OS_URL", "http://opensearch:9200")
    os_index = os.getenv("RAG_OS_INDEX", "laws")
    return OSClient(os_url, os_index)

def get_neo4j_client():
    """Get Neo4j client instance."""
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4j")
    return Neo4jClient(neo4j_uri, neo4j_user, neo4j_password)


def _basic_rerank(query: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Simple term-coverage reranker: boost items with more query token hits."""
    q_tokens = [t for t in query.lower().split() if len(t) > 1]
    
    def score_item(it: Dict[str, Any]) -> float:
        text = f"{it.get('title','')} {it.get('paragraph','')} {it.get('text','')}".lower()
        hits = sum(1 for t in q_tokens if t in text)
        return (it.get('score') or 0.0) + hits * 0.25
    
    return sorted(items, key=score_item, reverse=True)


def _dot(a: List[float], b: List[float]) -> float:
    """Calculate dot product of two vectors."""
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    return sum((a[i] or 0.0) * (b[i] or 0.0) for i in range(n))


# API Endpoints
@router.get("/documents/search", response_model=RetrieveResponse)
def search_documents(
    q: str = Query(..., min_length=2, description="Search query"),
    top_k: int = Query(10, ge=1, le=100, description="Number of results to return"),
    rerank: int = Query(0, ge=0, le=2, description="Reranking method (0=none, 1=term-coverage, 2=embedding)")
):
    """
    Search for relevant law documents using text search.
    
    Supports multiple reranking strategies:
    - 0: No reranking (default OpenSearch scoring)
    - 1: Term coverage reranking
    - 2: Embedding-based reranking
    """
    try:
        os_client = get_opensearch_client()
        res = os_client.search(q, top_k=top_k)
        items = res["items"]
        
        if rerank == 1:
            items = _basic_rerank(q, items)
        elif rerank == 2:
            # Embedding dot-product rerank (client-side)
            qvec = os_client._embed(q)
            items = sorted(items, key=lambda it: _dot(qvec, it.get('vector') or []), reverse=True)
        
        return RetrieveResponse(total=res["total"], items=items)
        
    except Exception as e:
        raise_http_error("SEARCH_FAILED", f"Document search failed: {str(e)}")


@router.get("/documents/knn", response_model=RetrieveResponse)
def search_documents_knn(
    q: str = Query(..., min_length=2, description="Query for embedding-based search"),
    k: int = Query(10, ge=1, le=100, description="Number of nearest neighbors")
):
    """
    Search for documents using K-nearest neighbor vector search.
    
    Uses query embedding to find semantically similar documents.
    """
    try:
        os_client = get_opensearch_client()
        res = os_client.knn_search(q, k)
        return RetrieveResponse(total=res["total"], items=res["items"])
        
    except Exception as e:
        raise_http_error("KNN_SEARCH_FAILED", f"KNN search failed: {str(e)}")


@router.post("/documents/knn/vector", response_model=RetrieveResponse)
def search_by_vector(body: KNNVectorRequest):
    """
    Search for documents using a provided vector.
    
    Allows direct vector search when you already have embeddings.
    """
    try:
        os_client = get_opensearch_client()
        res = os_client.knn_search_vector(body.vector, body.k, body.filters)
        return RetrieveResponse(total=res["total"], items=res["items"])
        
    except Exception as e:
        raise_http_error("VECTOR_SEARCH_FAILED", f"Vector search failed: {str(e)}")


@router.post("/documents/hybrid", response_model=RetrieveResponse)
def hybrid_search(req: HybridRequest):
    """
    Perform hybrid search combining BM25 text search and KNN vector search.
    
    Combines results from both search methods using configurable weighting.
    """
    try:
        os_client = get_opensearch_client()
        
        # Text search
        text_results = os_client.search(req.q, top_k=req.top_k, filters=req.filters)
        
        # KNN search
        knn_results = os_client.knn_search(req.q, k=req.k, filters=req.filters)
        
        # Normalize and combine scores
        bm = {it['id']: (it.get('score') or 0.0, it) for it in text_results['items']}
        km = {it['id']: (it.get('score') or 0.0, it) for it in knn_results['items']}
        
        max_b = max((v[0] for v in bm.values()), default=1.0)
        max_k = max((v[0] for v in km.values()), default=1.0)
        
        combined = {}
        for id_, (sc, it) in bm.items():
            combined.setdefault(id_, {'doc': it, 'b': 0.0, 'k': 0.0})
            combined[id_]['b'] = sc / (max_b or 1.0)
            
        for id_, (sc, it) in km.items():
            combined.setdefault(id_, {'doc': it, 'b': 0.0, 'k': 0.0})
            combined[id_]['k'] = sc / (max_k or 1.0)
        
        # Calculate hybrid scores
        alpha = max(0.0, min(1.0, req.alpha))
        items = []
        for id_, comp in combined.items():
            score = alpha * comp['b'] + (1 - alpha) * comp['k']
            doc = dict(comp['doc'])
            doc['hybrid_score'] = score
            items.append(doc)
        
        items.sort(key=lambda x: x.get('hybrid_score', 0.0), reverse=True)
        items = items[:req.top_k]
        
        return RetrieveResponse(total=len(items), items=items)
        
    except Exception as e:
        raise_http_error("HYBRID_SEARCH_FAILED", f"Hybrid search failed: {str(e)}")


@router.get("/entities/{entity}/context", response_model=ContextResponse)
def get_entity_context(
    entity: str,
    top_k: int = Query(10, ge=1, le=100, description="Maximum number of laws to return")
):
    """
    Get relevant laws for an entity using graph relationships.
    
    First tries graph links, falls back to text search by entity name.
    """
    try:
        neo_client = get_neo4j_client()
        
        # First try graph links
        linked = neo_client.get_laws_for_entity(entity, limit=top_k)
        if linked:
            return ContextResponse(entity=entity, laws=linked)
        
        # Fallback: search text by entity name
        os_client = get_opensearch_client()
        res = os_client.search(entity, top_k=top_k)
        return ContextResponse(entity=entity, laws=res["items"])
        
    except Exception as e:
        raise_http_error("CONTEXT_SEARCH_FAILED", f"Entity context search failed: {str(e)}")


@router.post("/documents", response_model=IndexResponse)
def index_document(doc: LawDoc):
    """
    Index a law document into the search index.
    
    Performs idempotent upsert operation.
    """
    try:
        os_client = get_opensearch_client()
        ok = os_client.index_doc(doc.model_dump())
        
        if not ok:
            raise_http_error("INDEXING_FAILED", "Document indexing failed")
        
        return IndexResponse(status="indexed", id=doc.id)
        
    except Exception as e:
        raise_http_error("INDEX_OPERATION_FAILED", f"Failed to index document: {str(e)}")


@router.post("/graph/documents", response_model=GraphUpsertResponse)
def upsert_document_graph(req: GraphUpsertRequest):
    """
    Upsert a law document and its relationships into the graph database.
    
    Creates law node and relationships to sectors and firms.
    """
    try:
        neo_client = get_neo4j_client()
        neo_client.ensure_schema()
        
        # Backwards compatibility: 'applies_to' is treated as sectors
        applies_to_sectors = req.sectors or req.applies_to or []
        applies_to_firms = req.firms or []
        
        neo_client.upsert_law(
            req.doc.model_dump(), 
            applies_to_sectors=applies_to_sectors, 
            applies_to_firms=applies_to_firms
        )
        
        return GraphUpsertResponse(
            status="upserted",
            law_id=req.doc.id,
            sectors=applies_to_sectors,
            firms=applies_to_firms
        )
        
    except Exception as e:
        raise_http_error("GRAPH_UPSERT_FAILED", f"Graph upsert failed: {str(e)}")


@router.post("/events/extract", response_model=ExtractEventsResponse)
def extract_events(req: ExtractEventsRequest):
    """
    Extract events from text using pattern matching.
    
    Detects dates, specific event types, and other temporal patterns.
    """
    try:
        text = req.text
        
        # Naive patterns for date-like tokens and verbs
        dates = re.findall(r"\\b\\d{1,2}[./-]\\d{1,2}[./-]\\d{2,4}\\b", text)
        verbs = [w for w in text.split() if w.endswith(('te', 'ten', 't'))]
        
        events = []
        
        if dates:
            from ..models.requests import Event
            events.append(Event(
                type="dated_event",
                date=dates[0],
                snippet=text[:200]
            ))
        
        if any(v.lower().startswith('explod') for v in verbs):
            from ..models.requests import Event
            events.append(Event(
                type="explosion",
                snippet=text[:200]
            ))
        
        return ExtractEventsResponse(events=events)
        
    except Exception as e:
        raise_http_error("EVENT_EXTRACTION_FAILED", f"Event extraction failed: {str(e)}")


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(req: FeedbackRequest):
    """
    Submit feedback/labels for improving search quality.
    
    Stores feedback for later analysis and model improvement.
    """
    try:
        # Ensure feedback directory exists
        os.makedirs("/data/feedback", exist_ok=True)
        
        # Append feedback to JSONL file
        feedback_data = req.model_dump()
        path = "/data/feedback/labels.jsonl"
        
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_data, ensure_ascii=False) + "\\n")
        
        return FeedbackResponse(status="ok")
        
    except Exception as e:
        raise_http_error("FEEDBACK_FAILED", f"Failed to record feedback: {str(e)}")


@router.post("/index/knn/ef_search")
def update_ef_search(req: EfSearchRequest):
    """
    Update ef_search parameter for HNSW index optimization.
    
    Controls search quality vs speed tradeoff in vector search.
    """
    try:
        os_client = get_opensearch_client()
        res = os_client.set_ef_search(req.ef_search)
        
        code = 200 if res.get('status') == 'ok' else 500
        return res
        
    except Exception as e:
        raise_http_error("EF_SEARCH_UPDATE_FAILED", f"Failed to update ef_search: {str(e)}")


@router.get("/documents", response_model=PaginatedResponse)
def list_documents(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    domain: Optional[str] = Query(None, description="Filter by legal domain"),
    source: Optional[str] = Query(None, description="Filter by source")
):
    """
    List indexed documents with pagination and filtering.
    
    Supports filtering by domain and source.
    """
    try:
        os_client = get_opensearch_client()
        
        # Build filters
        filters = {}
        if domain:
            filters["domain"] = domain
        if source:
            filters["source"] = source
        
        # Calculate offset
        offset = (page - 1) * size
        
        # Perform search with filters
        if filters:
            # Use filtered search
            query = "*"  # Match all with filters
            res = os_client.search(query, top_k=size, filters=filters)
        else:
            # Simple pagination query
            res = os_client.search("*", top_k=size)
        
        return PaginatedResponse(
            items=res["items"],
            total=res["total"],
            page=page,
            size=size
        )
        
    except Exception as e:
        raise_http_error("LIST_DOCUMENTS_FAILED", f"Failed to list documents: {str(e)}")


@router.get("/stats")
def get_statistics():
    """
    Get service statistics and index information.
    """
    try:
        os_client = get_opensearch_client()
        neo_client = get_neo4j_client()
        
        # Get basic stats (placeholder - implement based on client capabilities)
        stats = {
            "opensearch": {
                "status": "connected",
                "index": os.getenv("RAG_OS_INDEX", "laws")
            },
            "neo4j": {
                "status": "connected" if neo_client.ping() else "disconnected"
            },
            "features": {
                "text_search": True,
                "vector_search": True,
                "hybrid_search": True,
                "graph_context": True,
                "event_extraction": True,
                "feedback_collection": True
            }
        }
        
        return stats
        
    except Exception as e:
        raise_http_error("STATS_FAILED", f"Failed to get statistics: {str(e)}")
