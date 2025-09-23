"""
InfoTerminal Service Template - Standard *_v1.py Pattern

This template provides the standardized structure for all InfoTerminal services.
Copy and customize this template for services that need *_v1.py migration.

Usage:
1. Copy this template to your service directory
2. Customize the service-specific details (name, description, dependencies)
3. Add domain-specific routers to the routers/ directory
4. Implement domain endpoints following the patterns shown
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
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
    HealthChecker,
    DependencyCheck
)


# Service Configuration - CUSTOMIZE FOR EACH SERVICE
SERVICE_NAME = "template-service"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "Template service demonstrating InfoTerminal API standards"

# Health checker instance
health_checker = HealthChecker(SERVICE_NAME, SERVICE_VERSION)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    print(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    # Add dependency checks here
    # health_checker.add_dependency("database", check_database)
    # health_checker.add_dependency("external_api", check_external_api)
    
    yield
    
    # Shutdown
    print(f"Shutting down {SERVICE_NAME}")


# FastAPI application with standardized configuration
app = FastAPI(
    title=f"InfoTerminal {SERVICE_NAME.title().replace('-', ' ')} API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply standard middleware and exception handlers
setup_standard_middleware(app, SERVICE_NAME)
setup_standard_exception_handlers(app)

# Set up standard OpenAPI documentation
setup_standard_openapi(
    app=app,
    title=f"InfoTerminal {SERVICE_NAME.title().replace('-', ' ')} API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    service_name=SERVICE_NAME,
    tags_metadata=get_service_tags_metadata(SERVICE_NAME)
)


# ===== CORE ENDPOINTS (REQUIRED FOR ALL SERVICES) =====

@app.get("/healthz", response_model=None, tags=["health"])
def healthz():
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    return health_checker.health_check()


@app.get("/readyz", response_model=None, tags=["health"])
def readyz():
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including dependency checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    return health_checker.ready_check()


@app.get("/info", response_model=None, tags=["health"])
def info():
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "api_version": "v1",
        "openapi_url": "/docs",
        "health_check_url": "/healthz",
        "readiness_check_url": "/readyz"
    }


# ===== V1 API ROUTER INCLUDES =====
# Add your domain-specific routers here following this pattern:

# from .routers import domain_v1
# app.include_router(
#     domain_v1.router,
#     prefix="/v1/domain",
#     tags=["domain"]
# )

# Example domain router structure:
"""
routers/
├── core_v1.py       # health/ready/info (if you want to separate from main)
├── domain_v1.py     # main domain endpoints
├── admin_v1.py      # admin endpoints (optional)
└── webhooks_v1.py   # webhook endpoints (optional)
"""


# ===== LEGACY ENDPOINTS (DEPRECATED) =====
# Keep legacy endpoints for backward compatibility with deprecation warnings

@app.get("/health", deprecated=True, tags=["legacy"])
def legacy_health():
    """
    DEPRECATED: Use /healthz instead.
    Legacy health endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"status": "healthy", "message": "Use /healthz instead"},
        headers={"X-Deprecated": "Use /healthz instead"}
    )


# ===== DEPENDENCY CHECK EXAMPLES =====
# Implement these functions based on your service dependencies

def check_database_connection() -> DependencyCheck:
    """
    Example database connection check.
    Customize this for your database type (PostgreSQL, Neo4j, etc.)
    """
    try:
        # Replace with actual database ping
        # db.execute("SELECT 1")
        
        return DependencyCheck(
            status="healthy",
            latency_ms=5.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


def check_external_service() -> DependencyCheck:
    """
    Example external service check.
    Customize this for your external dependencies.
    """
    try:
        # Replace with actual service check
        # response = requests.get("http://external-service/health", timeout=5)
        
        return DependencyCheck(
            status="healthy",
            latency_ms=10.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy", 
            error=str(e)
        )


# ===== ROUTER TEMPLATE =====
"""
Example router template for routers/domain_v1.py:

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    StandardError,
    APIError,
    ErrorCodes
)

router = APIRouter()

# Request/Response Models
class DomainRequest(BaseModel):
    name: str
    description: Optional[str] = None

class DomainResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: str

# Endpoints
@router.get(
    "/items",
    response_model=PaginatedResponse[DomainResponse],
    summary="List domain items",
    description="Get a paginated list of domain items with optional filtering."
)
def list_items(
    pagination: PaginationParams = Depends(),
    q: Optional[str] = Query(None, description="Search query")
) -> PaginatedResponse[DomainResponse]:
    try:
        # Implement your business logic here
        items = []  # Replace with actual data
        total = 0   # Replace with actual count
        
        return PaginatedResponse.create(items, total, pagination)
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve items",
            status_code=500,
            details={"error": str(e)}
        )

@router.post(
    "/items",
    response_model=DomainResponse,
    status_code=201,
    summary="Create domain item",
    description="Create a new domain item with the provided data."
)
def create_item(request: DomainRequest) -> DomainResponse:
    try:
        # Implement your business logic here
        # item = create_domain_item(request)
        
        return DomainResponse(
            id="example-id",
            name=request.name,
            description=request.description,
            created_at="2025-09-21T16:45:00Z"
        )
        
    except ValueError as e:
        raise APIError(
            code=ErrorCodes.VALIDATION_ERROR,
            message=str(e),
            status_code=400
        )
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to create item",
            status_code=500,
            details={"error": str(e)}
        )

@router.get(
    "/items/{item_id}",
    response_model=DomainResponse,
    summary="Get domain item",
    description="Retrieve a specific domain item by its ID."
)
def get_item(item_id: str) -> DomainResponse:
    try:
        # Implement your business logic here
        # item = get_domain_item(item_id)
        # if not item:
        #     raise APIError(
        #         code=ErrorCodes.RESOURCE_NOT_FOUND,
        #         message=f"Item with ID {item_id} not found",
        #         status_code=404
        #     )
        
        return DomainResponse(
            id=item_id,
            name="Example Item",
            description="Example description",
            created_at="2025-09-21T16:45:00Z"
        )
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve item",
            status_code=500,
            details={"error": str(e)}
        )
"""

if __name__ == "__main__":
    import uvicorn
    
    # Default port configuration (customize for each service)
    default_port = 8000
    port = int(os.getenv("PORT", default_port))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
