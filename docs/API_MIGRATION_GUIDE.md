# InfoTerminal API Standards Migration Guide

This document explains how to migrate existing InfoTerminal services to use the new unified API standards.

## Overview

All InfoTerminal services must implement the following standards:

- **Error Handling**: Standard error envelope format
- **Pagination**: Consistent pagination patterns for list endpoints  
- **Health Checks**: Standard `/healthz` and `/readyz` endpoints
- **Middleware**: Security, CORS, metrics, and request ID middleware
- **OpenAPI**: Consistent API documentation
- **Versioning**: `/v1` namespace for all endpoints

## Migration Steps

### 1. Install Shared Standards Package

Add to your service's requirements.txt or pyproject.toml:

```python
# In your service's main.py or app.py
import sys
from pathlib import Path

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers, 
    setup_standard_openapi,
    HealthChecker,
    PaginatedResponse,
    StandardError
)
```

### 2. Update FastAPI App Configuration

Replace your existing FastAPI configuration:

```python
# OLD
app = FastAPI(title="My Service", version="0.1.0")

# NEW
from _shared.api_standards.openapi import get_service_tags_metadata

app = FastAPI(
    title="InfoTerminal Search API",
    description="Search and indexing service for InfoTerminal OSINT platform",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc"
)

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
```

### 3. Migrate Health Endpoints

Replace existing health endpoints:

```python
# OLD
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# NEW
from _shared.api_standards.health import HealthChecker, check_database_connection

health_checker = HealthChecker("search-api", "1.0.0")

# Add dependency checks
def check_opensearch():
    # Your OpenSearch health check logic
    client.cluster.health()

health_checker.add_dependency("opensearch", lambda: check_database_connection(check_opensearch))

@app.get("/healthz", response_model=HealthResponse, tags=["health"])
def healthz():
    return health_checker.health_check()

@app.get("/readyz", response_model=ReadyResponse, tags=["health"])  
def readyz():
    return health_checker.ready_check()
```

### 4. Migrate to /v1 Namespace

Create a new APIRouter for v1 endpoints:

```python
from fastapi import APIRouter

# Create v1 router
v1_router = APIRouter(prefix="/v1", tags=["v1"])

# Migrate endpoints to v1
@v1_router.post("/search", response_model=SearchResponse, tags=["search"])
def search_documents(request: SearchRequest):
    # Your search logic
    pass

@v1_router.post("/index/documents", response_model=IndexResponse, tags=["indexing"])
def index_documents(documents: List[Document]):
    # Your indexing logic  
    pass

# Include v1 router
app.include_router(v1_router)

# Keep legacy endpoints temporarily with deprecation warnings
@app.post("/search", deprecated=True)
def legacy_search(request: SearchRequest):
    """DEPRECATED: Use /v1/search instead"""
    return search_documents(request)
```

### 5. Update Error Handling

Replace custom error responses:

```python
# OLD
@app.get("/documents/{doc_id}")
def get_document(doc_id: str):
    if not document_exists(doc_id):
        raise HTTPException(404, "Document not found")
    return get_doc(doc_id)

# NEW
from _shared.api_standards.error_schemas import APIError, ErrorCodes

@app.get("/v1/documents/{doc_id}")
def get_document(doc_id: str):
    if not document_exists(doc_id):
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="Document not found",
            status_code=404,
            details={"doc_id": doc_id, "resource_type": "document"}
        )
    return get_doc(doc_id)
```

### 6. Add Pagination to List Endpoints

Convert list endpoints to use pagination:

```python
# OLD  
@app.get("/documents")
def list_documents():
    return {"documents": get_all_documents()}

# NEW
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from fastapi import Depends

@app.get("/v1/documents", response_model=PaginatedResponse[Document])
def list_documents(pagination: PaginationParams = Depends()):
    # Get paginated results
    total_count = count_documents()
    documents = get_documents_paginated(
        offset=pagination.offset,
        limit=pagination.limit
    )
    
    return PaginatedResponse.create(
        items=documents,
        total=total_count, 
        pagination=pagination
    )
```

### 7. Update Response Models

Ensure all response models follow standards:

```python
from pydantic import BaseModel
from typing import List, Optional
from _shared.api_standards.pagination import PaginatedResponse

class SearchRequest(BaseModel):
    q: str
    filters: Optional[Dict[str, Any]] = None
    sort: Optional[str] = None

class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    took_ms: int
    
# For paginated responses, use PaginatedResponse[T]
SearchResultsPage = PaginatedResponse[SearchResult]
```

### 8. Add OpenAPI Tags and Documentation

Tag your endpoints appropriately:

```python
@v1_router.post("/search", 
                response_model=SearchResponse,
                tags=["search"],
                summary="Search documents",
                description="Search across indexed documents with filters and sorting")
def search_documents(request: SearchRequest):
    """
    Search documents in the index.
    
    - **q**: Search query string
    - **filters**: Optional filters to apply
    - **sort**: Optional sort field and direction
    
    Returns list of matching documents with relevance scores.
    """
    pass
```

## Service-Specific Migration Notes

### Search API
- Migrate `/query` to `/v1/search`
- Migrate `/search` to `/v1/query` (for backward compatibility)
- Add `/v1/index/documents` endpoint
- Use pagination for search results

### Graph API  
- Migrate `/query` to `/v1/cypher`
- Migrate `/neighbors` to `/v1/nodes/{id}/neighbors`
- Add `/v1/algorithms/*` endpoints
- Use pagination for large result sets

### Doc-Entities
- Migrate `/annotate` to `/v1/documents/annotate`
- Migrate `/ner` to `/v1/extract/entities`
- Add `/v1/extract/relations` endpoint
- Use pagination for entity lists

### Graph Views
- Migrate `/graphs/view/ego` to `/v1/views/ego`
- Migrate `/graphs/view/shortest-path` to `/v1/views/shortest-path`
- Add `/v1/export/*` endpoints

## Testing Migration

1. **Test health endpoints**: `curl http://localhost:8401/healthz`
2. **Test v1 endpoints**: `curl http://localhost:8401/v1/search`
3. **Check OpenAPI docs**: Visit `http://localhost:8401/v1/docs`
4. **Verify error responses**: Test with invalid input
5. **Test pagination**: Use `?page=2&size=10` parameters

## Backward Compatibility

- Keep legacy endpoints for 2 releases with deprecation warnings
- Add `X-API-Version: v1` header to responses
- Document migration path in API documentation
- Use HTTP redirects where appropriate: `301 Moved Permanently`

## Validation

After migration, verify:

- [ ] All endpoints use `/v1` prefix
- [ ] Standard error format in all error responses
- [ ] Health endpoints return standard format
- [ ] Pagination on all list endpoints  
- [ ] OpenAPI documentation is complete
- [ ] All tags and descriptions are present
- [ ] Middleware is properly configured
- [ ] Legacy endpoints marked as deprecated
