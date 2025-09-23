# Service Migration Guide - *_v1.py Standardization

This guide provides step-by-step instructions for migrating InfoTerminal services to the standardized *_v1.py pattern.

## Overview

**Goal:** Bring all InfoTerminal services to a consistent API standard with:
- `/v1` namespace for all new endpoints
- Standard error envelope format
- Consistent health/ready/info endpoints
- OpenAPI documentation
- Standard middleware (CORS, security, logging)
- Pagination for list endpoints

## Migration Process

### Step 1: Assess Current Service State

**Check if service has:**
- [ ] Existing `*_v1.py` files
- [ ] Health endpoints (`/healthz`, `/readyz`)
- [ ] Error handling patterns
- [ ] OpenAPI documentation
- [ ] Standard middleware

**Document:**
- Current endpoints and their purpose
- Dependencies (database, external services)
- Request/response models
- Port configuration

### Step 2: Create Service Structure

**Required files:**
```
service/
├── app_v1.py                 # Main FastAPI app (NEW)
├── routers/
│   ├── __init__.py
│   ├── core_v1.py           # Health/ready/info (NEW)
│   └── domain_v1.py         # Domain endpoints (NEW)
├── models/
│   ├── __init__.py
│   ├── requests.py          # Request schemas (NEW)
│   └── responses.py         # Response schemas (NEW)
├── deps.py                  # Dependencies (NEW/UPDATE)
├── config.py                # Configuration (UPDATE)
└── app.py                   # Legacy app (KEEP for backward compatibility)
```

### Step 3: Implement Core Infrastructure

**3.1 Create `app_v1.py` using the template:**
```python
# Copy from _shared/service_template.py
# Customize SERVICE_NAME, SERVICE_VERSION, SERVICE_DESCRIPTION
# Add service-specific dependencies
```

**3.2 Create `routers/core_v1.py`:**
```python
# Copy from _shared/routers/core_v1.py
# No changes needed - this is standard
```

**3.3 Create `config.py` with environment handling:**
```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    service_name: str = "your-service"
    version: str = "1.0.0"
    port: int = 8000
    
    # Database settings (if applicable)
    database_url: str = "postgresql://..."
    
    # External service URLs (if applicable)
    external_service_url: str = "http://localhost:8080"
    
    # Feature flags
    enable_metrics: bool = True
    enable_auth: bool = False
    
    class Config:
        env_prefix = "IT_"
        
settings = Settings()
```

### Step 4: Implement Domain Endpoints

**4.1 Create request/response models:**
```python
# models/requests.py
from pydantic import BaseModel, Field
from typing import Optional

class CreateItemRequest(BaseModel):
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Item description")

# models/responses.py  
from pydantic import BaseModel
from typing import Optional

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: str
```

**4.2 Create domain router:**
```python
# routers/domain_v1.py
from fastapi import APIRouter, Depends
from typing import List

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes
)
from ..models.requests import CreateItemRequest
from ..models.responses import ItemResponse

router = APIRouter()

@router.get("/items", response_model=PaginatedResponse[ItemResponse])
def list_items(pagination: PaginationParams = Depends()):
    # Implementation here
    pass

@router.post("/items", response_model=ItemResponse, status_code=201)
def create_item(request: CreateItemRequest):
    # Implementation here
    pass
```

### Step 5: Add Dependency Checks

**Update `app_v1.py` with service-specific dependency checks:**

```python
# Add after health_checker initialization
def check_database() -> DependencyCheck:
    try:
        # Replace with actual database check
        # db.execute("SELECT 1")
        return DependencyCheck(status="healthy", latency_ms=5.0)
    except Exception as e:
        return DependencyCheck(status="unhealthy", error=str(e))

health_checker.add_dependency("database", check_database)
```

### Step 6: Preserve Legacy Endpoints

**Keep existing `app.py` for backward compatibility:**
- Add deprecation warnings to legacy endpoints
- Proxy to new v1 endpoints where possible
- Plan deprecation timeline

### Step 7: Add Tests

**Create `test_v1.py`:**
```python
import pytest
from fastapi.testclient import TestClient
from .app_v1 import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_check():
    response = client.get("/readyz")
    assert response.status_code == 200
    
def test_service_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert "service" in response.json()
```

### Step 8: Update Port Configuration

**Add service to `scripts/patch_ports.sh`:**
```bash
# Add to HOST_PORTS_COMPOSE array
[your-service]=8617

# Add to dev ports in .env.dev.ports  
YOUR_SERVICE_URL="http://127.0.0.1:8407"
```

### Step 9: Update Docker Configuration

**Add to appropriate docker-compose file:**
```yaml
  your-service:
    build: ./services/your-service
    ports:
      - "8617:8080"
    environment:
      - IT_SERVICE_NAME=your-service
      - IT_ENABLE_METRICS=1
    depends_on:
      - database  # if applicable
```

## Service-Specific Migration Guides

### High-Priority Services

#### 1. flowise-connector
**Current State:** Basic FastAPI, no v1 structure
**Endpoints to migrate:**
- `POST /chat` → `POST /v1/agents/chat`
- `GET /tools` → `GET /v1/agents/tools` 
- `POST /tools/execute` → `POST /v1/agents/execute`
- `GET /workflows` → `GET /v1/agents/workflows`

**Dependencies:** Flowise API connection

#### 2. agent-connector  
**Current State:** Basic FastAPI, no v1 structure
**Endpoints to migrate:**
- `GET /plugins/registry` → `GET /v1/plugins`
- `POST /plugins/invoke/{plugin}/{tool}` → `POST /v1/plugins/{name}/execute`
- `GET /plugins/tools` → `GET /v1/plugins/tools`
- `POST /plugins/{name}/config` → `PUT /v1/plugins/{name}/config`

**Dependencies:** Plugin system, local registry

#### 3. media-forensics
**Current State:** Basic FastAPI, no v1 structure  
**Endpoints to migrate:**
- `POST /image/analyze` → `POST /v1/media/analyze`
- `POST /image/compare` → `POST /v1/media/compare`
- `GET /formats` → `GET /v1/media/formats`

**Dependencies:** Image processing libraries

#### 4. forensics  
**Current State:** Basic FastAPI, no v1 structure
**Endpoints to migrate:**
- `POST /ingest` → `POST /v1/forensics/ingest`
- `POST /verify` → `POST /v1/forensics/verify`
- `GET /receipt/{sha256}` → `GET /v1/forensics/receipts/{sha256}`

**Dependencies:** Blockchain/ledger system

## Validation Checklist

After migration, verify:

- [ ] **Health endpoints:** `/healthz`, `/readyz`, `/info` return proper responses
- [ ] **V1 endpoints:** All domain endpoints under `/v1/` namespace
- [ ] **Error envelope:** All errors use StandardError format
- [ ] **OpenAPI docs:** `/docs` shows complete API documentation
- [ ] **Pagination:** List endpoints use PaginatedResponse
- [ ] **Middleware:** CORS, security headers, logging enabled
- [ ] **Legacy support:** Old endpoints still work with deprecation warnings
- [ ] **Tests:** Core functionality tested
- [ ] **Port config:** Service in patch_ports.sh and docker-compose

## Common Issues & Solutions

### Issue: Import errors with _shared
**Solution:** Add to Python path:
```python
sys.path.insert(0, str(REPO_ROOT / "services"))
```

### Issue: Dependency check failures
**Solution:** Add forced ready mode:
```python
if os.getenv("IT_FORCE_READY") == "1":
    return ReadyResponse(status="ready", ...)
```

### Issue: Port conflicts
**Solution:** Check `scripts/patch_ports.sh` for assigned ports

### Issue: CORS errors in development
**Solution:** Verify CORS_ORIGINS environment variable

## Timeline Estimation

**Per service migration time:**
- Simple service (< 10 endpoints): 4-6 hours
- Medium service (10-20 endpoints): 1-2 days  
- Complex service (20+ endpoints): 2-3 days

**Total estimated time for all 21 services:** 4-6 weeks

## Next Steps

1. Start with highest priority services (flowise-connector, agent-connector)
2. Migrate 3-4 services per week
3. Update CLI commands to use v1 endpoints  
4. Plan deprecation timeline for legacy endpoints
5. Complete integration testing
