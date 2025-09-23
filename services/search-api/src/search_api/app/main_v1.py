"""
InfoTerminal Search API - Standardized Implementation

This is the new standardized version of the Search API implementing all
InfoTerminal API standards:
- /v1 namespace
- Standard error handling  
- Pagination
- Health checks
- OpenAPI documentation
- Middleware setup
"""

import os
import sys
import time
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path

import numpy as np
from pydantic import BaseModel, Field

from fastapi import FastAPI, Depends, HTTPException, Header, Query, Response, APIRouter
from fastapi.responses import JSONResponse

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata,
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes
)
from _shared.health import make_healthz as legacy_make_healthz, make_readyz as legacy_make_readyz, probe_http as legacy_probe_http

try:
    from opensearchpy import OpenSearch
    OPENSEARCH_AVAILABLE = True
except ImportError:
    OPENSEARCH_AVAILABLE = False

from .it_logging import setup_logging
from search_api.auth import user_from_token
from search_api.opa import allow
from .config import Settings
from . import rerank as rr
from .metrics import (
    SEARCH_ERRORS,
    SEARCH_LATENCY,
    SEARCH_REQUESTS,
    RERANK_LATENCY,
    RERANK_REQS,
)

try:
    from search_api._shared.obs.otel_boot import setup_otel
except Exception:  # pragma: no cover - optional dependency
    def setup_otel(*args, **kwargs):
        return None

# Configuration
settings = Settings()
logger = logging.getLogger(__name__)

# FastAPI App with Standard Configuration
app = FastAPI(
    title="InfoTerminal Search API",
    description="Search and indexing service for InfoTerminal OSINT platform",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc"
)

# Set up logging
setup_logging(app, service_name="search-api")

# Set up standard middleware and exception handling
setup_standard_middleware(app, "search-api")
setup_standard_exception_handlers(app)
setup_standard_openapi(
    app=app,
    title="InfoTerminal Search API",
    description="Search and indexing service for InfoTerminal OSINT platform", 
    version="1.0.0",
    service_name="search-api",
    tags_metadata=get_service_tags_metadata("search-api")
)

# Application state
app.state.service_name = "search-api"
app.state.version = os.getenv("GIT_SHA", "1.0.0")
app.state.start_ts = time.monotonic()

# OpenTelemetry instrumentation (if available / enabled)
setup_otel(app, service_name=app.state.service_name, version=app.state.version)

# Initialize OpenSearch client
client = None
if OPENSEARCH_AVAILABLE:
    client = OpenSearch(settings.os_url)

# Legacy-style health helpers (retained for compatibility)


@app.get("/healthz", tags=["health"])
def healthz():
    """Health check endpoint (legacy response schema)."""
    return legacy_make_healthz(app.state.service_name, app.state.version, app.state.start_ts)


@app.get("/readyz", tags=["health"])
def readyz():
    """Readiness check endpoint with legacy response schema."""
    if os.getenv("IT_FORCE_READY") == "1":
        payload, status = legacy_make_readyz(app.state.service_name, app.state.version, app.state.start_ts, {})
        return JSONResponse(payload, status_code=status)

    checks: Dict[str, Dict[str, Any]] = {}

    opensearch_url = os.getenv("OPENSEARCH_URL") or getattr(settings, "os_url", None)
    if opensearch_url and OPENSEARCH_AVAILABLE and client:
        checks["opensearch"] = legacy_probe_http(f"{opensearch_url.rstrip('/')}/_cluster/health")
    else:
        checks["opensearch"] = {"status": "skipped", "latency_ms": None, "error": None, "reason": "missing config"}

    payload, status = legacy_make_readyz(app.state.service_name, app.state.version, app.state.start_ts, checks)
    return JSONResponse(payload, status_code=status)


# API Models
class SearchRequest(BaseModel):
    """Search request model."""
    q: str = Field(..., description="Search query string")
    filters: Optional[Dict[str, List[str]]] = Field(
        default_factory=dict,
        description="Search filters by field"
    )
    facets: List[str] = Field(
        default_factory=list,
        description="Fields to return facet counts for"
    )
    sort: Optional[Dict[str, str]] = Field(
        None,
        description="Sort configuration with field and order"
    )
    highlight: bool = Field(
        default=True,
        description="Whether to include search result highlighting"
    )


class SearchResult(BaseModel):
    """Individual search result."""
    id: str = Field(..., description="Document ID")
    score: float = Field(..., description="Relevance score")
    title: Optional[str] = Field(None, description="Document title")
    body: Optional[str] = Field(None, description="Document body content")
    snippet: Optional[str] = Field(None, description="Search result snippet")
    entities: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Extracted entities"
    )
    meta: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata"
    )


class FacetBucket(BaseModel):
    """Facet bucket with count."""
    key: str = Field(..., description="Facet value")
    doc_count: int = Field(..., description="Number of documents")


class SearchResponse(BaseModel):
    """Search response with results and metadata."""
    results: List[SearchResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of matching documents")
    took_ms: int = Field(..., description="Query execution time in milliseconds")
    facets: Dict[str, List[FacetBucket]] = Field(
        default_factory=dict,
        description="Facet aggregations"
    )
    reranked: bool = Field(
        default=False,
        description="Whether results were reranked"
    )


class IndexRequest(BaseModel):
    """Document indexing request."""
    documents: List[Dict[str, Any]] = Field(
        ...,
        description="List of documents to index"
    )
    index: Optional[str] = Field(
        None,
        description="Target index name (optional)"
    )


class IndexResponse(BaseModel):
    """Document indexing response."""
    indexed: int = Field(..., description="Number of documents indexed")
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Indexing errors"
    )
    took_ms: int = Field(..., description="Indexing time in milliseconds")


class DocumentResponse(BaseModel):
    """Single document response."""
    id: str = Field(..., description="Document ID")
    found: bool = Field(..., description="Whether document was found")
    source: Optional[Dict[str, Any]] = Field(
        None,
        description="Document source data"
    )


# Authentication dependency
def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current user from authorization header."""
    if not settings.require_auth:
        return {"sub": "dev", "roles": ["analyst"]}
    
    if not authorization or not authorization.startswith("Bearer "):
        raise APIError(
            code=ErrorCodes.UNAUTHORIZED,
            message="Missing or invalid authorization header",
            status_code=401,
            details={"expected": "Bearer <token>"}
        )
    
    try:
        token = authorization.split(" ", 1)[1]
        return user_from_token(token)
    except Exception as e:
        raise APIError(
            code=ErrorCodes.AUTH_ERROR,
            message="Invalid authentication token",
            status_code=401,
            details={"error": str(e)}
        )


# V1 API Router
v1_router = APIRouter(prefix="/v1", tags=["v1"])


@v1_router.post("/search", 
                response_model=PaginatedResponse[SearchResult],
                tags=["search"],
                summary="Search documents",
                description="Search across indexed documents with filters, sorting, and pagination")
def search_documents(
    request: SearchRequest,
    pagination: PaginationParams = Depends(),
    enable_rerank: bool = Query(
        default=False,
        description="Enable AI-powered result reranking"
    ),
    user=Depends(get_current_user)
):
    """
    Search documents in the index.
    
    Performs full-text search across indexed documents with support for:
    - Query string search
    - Field-based filtering  
    - Faceted search
    - Result sorting
    - Pagination
    - AI-powered reranking (optional)
    
    Requires read permissions on search resources.
    """
    
    if not OPENSEARCH_AVAILABLE or not client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Search service unavailable",
            status_code=503,
            details={"reason": "OpenSearch not configured"}
        )
    
    # Check permissions
    if not allow(user, "read", {"classification": "public", "type": "search"}):
        raise APIError(
            code=ErrorCodes.FORBIDDEN,
            message="Insufficient permissions for search operation",
            status_code=403,
            details={"required_permission": "search:read"}
        )
    
    try:
        with SEARCH_LATENCY.time():
            # Build OpenSearch query
            must_clauses = []
            if request.q:
                must_clauses.append({
                    "multi_match": {
                        "query": request.q,
                        "fields": ["title^2", "body", "entities.name^3"]
                    }
                })
            
            # Apply filters
            filter_clauses = []
            for field, values in (request.filters or {}).items():
                if values:
                    filter_clauses.append({"terms": {field: values}})
            
            # Construct query
            if must_clauses or filter_clauses:
                query = {
                    "bool": {
                        "must": must_clauses,
                        "filter": filter_clauses
                    }
                }
            else:
                query = {"match_all": {}}
            
            # Build request body
            body = {
                "query": query,
                "size": pagination.size,
                "from": pagination.offset
            }
            
            # Add facets
            if request.facets:
                body["aggs"] = {
                    f: {"terms": {"field": f, "size": 20}} 
                    for f in request.facets
                }
            
            # Add sorting
            if request.sort and request.sort.get("field"):
                body["sort"] = [{
                    request.sort["field"]: {
                        "order": request.sort.get("order", "asc")
                    }
                }]
            
            # Add highlighting
            if request.highlight:
                body["highlight"] = {
                    "fields": {
                        "title": {},
                        "body": {"fragment_size": 150}
                    }
                }
            
            # Execute search
            start_time = time.time()
            response = client.search(index=settings.os_index, body=body)
            search_time_ms = int((time.time() - start_time) * 1000)
            
            # Process results
            hits = response.get("hits", {})
            raw_hits = hits.get("hits", [])
            
            results = []
            for hit in raw_hits:
                result = SearchResult(
                    id=hit.get("_id"),
                    score=hit.get("_score", 0.0),
                    **hit.get("_source", {})
                )
                
                # Add highlighting
                if request.highlight and "highlight" in hit:
                    highlights = hit["highlight"]
                    if "body" in highlights:
                        result.snippet = highlights["body"][0]
                
                results.append(result)
            
            # Process facets
            facets = {}
            raw_aggs = response.get("aggregations", {}) or {}
            for facet_name in request.facets or []:
                if facet_name in raw_aggs:
                    buckets = raw_aggs[facet_name].get("buckets", [])
                    facets[facet_name] = [
                        FacetBucket(key=b.get("key"), doc_count=b.get("doc_count", 0))
                        for b in buckets
                    ]
            
            # Get total count
            total = hits.get("total", {})
            total_count = total.get("value") if isinstance(total, dict) else total or 0
            
            # Apply reranking if requested
            reranked = False
            if (enable_rerank and settings.rerank_enabled and 
                len(results) > 1 and request.q and len(request.q.strip()) > 2):
                
                try:
                    RERANK_REQS.inc()
                    with RERANK_LATENCY.time():
                        results = _apply_reranking(request.q, results)
                        reranked = True
                except Exception as e:
                    logger.warning(f"Reranking failed: {e}")
            
            # Create paginated response
            paginated_results = PaginatedResponse.create(
                items=results,
                total=total_count,
                pagination=pagination
            )
            
            # Add search metadata
            paginated_results.took_ms = search_time_ms
            paginated_results.facets = facets
            paginated_results.reranked = reranked
            
            SEARCH_REQUESTS.labels(rerank="1" if reranked else "0").inc()
            
            return paginated_results
            
    except Exception as e:
        SEARCH_ERRORS.labels(type=e.__class__.__name__).inc()
        
        if isinstance(e, APIError):
            raise
        
        raise APIError(
            code=ErrorCodes.SEARCH_ERROR,
            message=f"Search operation failed: {str(e)}",
            status_code=500,
            details={"query": request.q, "error_type": e.__class__.__name__}
        )


@v1_router.post("/index/documents",
                response_model=IndexResponse,
                tags=["indexing"],
                summary="Index documents",
                description="Index documents for search")
def index_documents(
    request: IndexRequest,
    user=Depends(get_current_user)
):
    """
    Index documents for search.
    
    Indexes a batch of documents into the search index with automatic
    ID generation and error handling.
    
    Requires write permissions on search resources.
    """
    
    if not OPENSEARCH_AVAILABLE or not client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Search service unavailable", 
            status_code=503,
            details={"reason": "OpenSearch not configured"}
        )
    
    # Check permissions
    if not allow(user, "write", {"classification": "public", "type": "search"}):
        raise APIError(
            code=ErrorCodes.FORBIDDEN,
            message="Insufficient permissions for indexing operation",
            status_code=403,
            details={"required_permission": "search:write"}
        )
    
    try:
        start_time = time.time()
        errors = []
        indexed_count = 0
        
        target_index = request.index or settings.os_index
        
        # Bulk index documents
        actions = []
        for i, doc in enumerate(request.documents):
            doc_id = doc.get("id") or f"doc_{int(time.time())}_{i}"
            
            actions.append({
                "_index": target_index,
                "_id": doc_id,
                "_source": doc
            })
        
        if actions:
            from opensearchpy.helpers import bulk
            
            success_count, failed_items = bulk(
                client,
                actions,
                index=target_index,
                raise_on_error=False
            )
            
            indexed_count = success_count
            
            for failed_item in failed_items:
                errors.append({
                    "action": "index",
                    "error": failed_item.get("index", {}).get("error", "Unknown error"),
                    "doc_id": failed_item.get("index", {}).get("_id")
                })
        
        took_ms = int((time.time() - start_time) * 1000)
        
        return IndexResponse(
            indexed=indexed_count,
            errors=errors,
            took_ms=took_ms
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.SEARCH_ERROR,
            message=f"Document indexing failed: {str(e)}",
            status_code=500,
            details={"document_count": len(request.documents), "error_type": e.__class__.__name__}
        )


@v1_router.get("/documents/{doc_id}",
               response_model=DocumentResponse,
               tags=["search"],
               summary="Get document by ID",
               description="Retrieve a specific document by ID")
def get_document(
    doc_id: str,
    user=Depends(get_current_user)
):
    """
    Get a specific document by ID.
    
    Retrieves a document from the search index by its unique identifier.
    
    Requires read permissions on search resources.
    """
    
    if not OPENSEARCH_AVAILABLE or not client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Search service unavailable",
            status_code=503,
            details={"reason": "OpenSearch not configured"}
        )
    
    # Check permissions
    if not allow(user, "read", {"classification": "public", "type": "search"}):
        raise APIError(
            code=ErrorCodes.FORBIDDEN,
            message="Insufficient permissions for document access",
            status_code=403,
            details={"required_permission": "search:read"}
        )
    
    try:
        response = client.get(
            index=settings.os_index,
            id=doc_id,
            ignore=[404]
        )
        
        if "found" in response and response["found"]:
            return DocumentResponse(
                id=doc_id,
                found=True,
                source=response.get("_source")
            )
        else:
            return DocumentResponse(
                id=doc_id,
                found=False,
                source=None
            )
            
    except Exception as e:
        raise APIError(
            code=ErrorCodes.SEARCH_ERROR,
            message=f"Failed to retrieve document: {str(e)}",
            status_code=500,
            details={"doc_id": doc_id, "error_type": e.__class__.__name__}
        )


@v1_router.delete("/documents/{doc_id}",
                  tags=["search"],
                  summary="Delete document by ID",
                  description="Delete a specific document by ID")
def delete_document(
    doc_id: str,
    user=Depends(get_current_user)
):
    """
    Delete a specific document by ID.
    
    Removes a document from the search index.
    
    Requires write permissions on search resources.
    """
    
    if not OPENSEARCH_AVAILABLE or not client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Search service unavailable",
            status_code=503,
            details={"reason": "OpenSearch not configured"}
        )
    
    # Check permissions
    if not allow(user, "write", {"classification": "public", "type": "search"}):
        raise APIError(
            code=ErrorCodes.FORBIDDEN,
            message="Insufficient permissions for document deletion",
            status_code=403,
            details={"required_permission": "search:write"}
        )
    
    try:
        response = client.delete(
            index=settings.os_index,
            id=doc_id,
            ignore=[404]
        )
        
        if response.get("result") == "deleted":
            return {"deleted": True, "doc_id": doc_id}
        elif response.get("result") == "not_found":
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message="Document not found",
                status_code=404,
                details={"doc_id": doc_id}
            )
        else:
            return {"deleted": False, "doc_id": doc_id, "result": response.get("result")}
            
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.SEARCH_ERROR,
            message=f"Failed to delete document: {str(e)}",
            status_code=500,
            details={"doc_id": doc_id, "error_type": e.__class__.__name__}
        )


def _apply_reranking(query: str, results: List[SearchResult]) -> List[SearchResult]:
    """Apply AI-powered reranking to search results."""
    if not settings.rerank_enabled or len(results) <= 1:
        return results
    
    topk = min(settings.rerank_topk, len(results))
    provider = rr.EmbeddingProvider(settings.rerank_model)
    
    # Get embeddings
    query_vec = rr.get_query_embedding(provider, query)
    doc_texts = [
        (results[i].snippet or results[i].body or results[i].title or "")[:1024]
        for i in range(topk)
    ]
    doc_vecs = np.vstack([
        rr.get_doc_embedding(provider, results[i].id, doc_texts[i]) 
        for i in range(topk)
    ])
    
    # Calculate similarity scores
    ranks = rr.cosine_rank(query_vec, doc_vecs)
    cos_scores = [r[1] for r in ranks]
    bm25_scores = [results[r[0]].score for r in ranks]
    
    # Normalize and blend scores
    norm_cos = rr.normalize(cos_scores)
    norm_bm = rr.normalize(bm25_scores)
    blended = [0.7 * norm_cos[i] + 0.3 * norm_bm[i] for i in range(len(ranks))]
    
    # Update results with reranking metadata
    reranked_results = []
    for (idx, cos), final in zip(ranks, blended):
        result = results[idx]
        if result.meta is None:
            result.meta = {}
        result.meta["rerank"] = {
            "cosine": float(cos),
            "blended": float(final)
        }
        result.score = float(final)
        reranked_results.append(result)
    
    # Sort by blended score and append remaining results
    reranked_results.sort(key=lambda x: x.score, reverse=True)
    return reranked_results + results[topk:]


# Include V1 router
app.include_router(v1_router)

# Legacy endpoints with deprecation warnings (temporary backward compatibility)
@app.get("/search", deprecated=True, tags=["legacy"])
@app.post("/search", deprecated=True, tags=["legacy"])
def legacy_search(
    response: Response,
    q: str = Query(..., description="Search query string"),
    entity_type: Optional[str] = Query(None, description="comma-separated entity types"),
    rerank: Optional[int] = Query(None),
    x_rerank: Optional[int] = Header(None, alias="X-Rerank"),
    limit: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    user=Depends(get_current_user)
):
    """
    DEPRECATED: Use /v1/search instead.
    
    Legacy search endpoint for backward compatibility.
    Will be removed in a future version.
    """
    # Convert to new format and call v1 endpoint
    request = SearchRequest(q=q)
    if entity_type:
        request.filters = {"entity_type": [s for s in entity_type.split(",") if s]}
    request.facets = ["entities.type"]

    pagination = PaginationParams(page=page, size=limit)
    enable_rerank = (rerank == 1) or (x_rerank == 1)

    search_response = search_documents(request, pagination, enable_rerank, user)

    # Re-shape into the legacy envelope
    items = [item.model_dump(mode="json") for item in search_response.items]

    raw_facets = getattr(search_response, "facets", {}) or {}
    legacy_facets: Dict[str, List[Dict[str, Any]]] = {}
    for name, buckets in raw_facets.items():
        bucket_rows: List[Dict[str, Any]] = []
        for bucket in buckets or []:
            if isinstance(bucket, FacetBucket):
                bucket_rows.append({"key": bucket.key, "count": bucket.doc_count})
            elif isinstance(bucket, dict):
                bucket_rows.append({
                    "key": bucket.get("key"),
                    "count": bucket.get("doc_count", bucket.get("count", 0)),
                })
        if name in {"entity_type", "entities.type", "entity_types"}:
            legacy_facets["entity_types"] = bucket_rows
        else:
            legacy_facets[name] = bucket_rows
    legacy_facets.setdefault("entity_types", [])

    if getattr(search_response, "reranked", False):
        response.headers["X-Reranked"] = "1"
        response.headers["X-Rerank-Model"] = settings.rerank_model
        response.headers["X-Rerank-TopK"] = str(min(settings.rerank_topk, len(items)))
        took_ms = getattr(search_response, "rerank_time_ms", None) or getattr(search_response, "took_ms", None)
        if took_ms is not None:
            response.headers["X-Rerank-TimeMs"] = str(took_ms)

    return {
        "results": items,
        "facets": legacy_facets,
    }


@app.post("/query", deprecated=True, tags=["legacy"])
def legacy_query(body: dict, user=Depends(get_current_user)):
    """
    DEPRECATED: Use /v1/search instead.
    
    Legacy query endpoint for backward compatibility.
    Will be removed in a future version.
    """
    # Convert legacy query format to new format
    request = SearchRequest(
        q=body.get("q", ""),
        filters=body.get("filters", {}),
        facets=body.get("facets", []),
        sort=body.get("sort")
    )
    
    pagination = PaginationParams(
        page=(body.get("offset", 0) // body.get("limit", 20)) + 1,
        size=body.get("limit", 20)
    )
    
    response = search_documents(request, pagination, False, user)
    
    # Convert to legacy format
    return {
        "items": response.items,
        "total": response.total,
        "aggregations": response.facets,
        "tookMs": getattr(response, "took_ms", 0)
    }


# Root endpoint
@app.get("/", tags=["root"])
def root():
    """Service information and available endpoints."""
    return {
        "service": "InfoTerminal Search API",
        "version": app.state.version,
        "status": "running",
        "api_version": "v1",
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz", 
            "docs": "/v1/docs",
            "search": "/v1/search",
            "index": "/v1/index/documents",
            "documents": "/v1/documents/{id}"
        },
        "legacy_endpoints": {
            "search": "/search (deprecated)",
            "query": "/query (deprecated)"
        }
    }
