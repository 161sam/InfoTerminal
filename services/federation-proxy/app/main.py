"""
DEPRECATED: federation-proxy legacy main.py

This file is deprecated and maintained only for backward compatibility.
All new development should use app_v1.py with the /v1 API endpoints.

⚠️  DEPRECATION NOTICE ⚠️
- This endpoint is deprecated and will be removed in a future version
- Please migrate to the v1 API endpoints at /v1/*
- See /docs for the new API documentation
- Contact the development team for migration assistance

Legacy endpoints still supported:
- GET /healthz -> Use GET /v1/healthz instead
- GET /remotes -> Use GET /v1/federation/endpoints instead

Migration timeline:
- Current: Legacy endpoints respond with deprecation warnings
- Next release: Legacy endpoints return 410 Gone status
- Future release: Legacy endpoints removed entirely
"""

import warnings
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import yaml
import os

# Configure deprecation warnings
warnings.filterwarnings("always", category=DeprecationWarning)
logger = logging.getLogger(__name__)

CONFIG_PATH = os.getenv("FEDERATION_CONFIG", "/app/remotes.yaml")

# Create legacy app for backward compatibility only
app = FastAPI(
    title="Federation Proxy Service (DEPRECATED)",
    description="⚠️ **DEPRECATED VERSION** - Use /v1/* endpoints instead",
    version="0.9.0-deprecated",
    deprecated=True
)

# Deprecation notice for all legacy endpoints
DEPRECATION_MESSAGE = {
    "deprecated": True,
    "message": "This endpoint is deprecated. Please use the v1 API endpoints.",
    "migration_guide": "/docs",
    "new_base_url": "/v1",
    "sunset_date": "2025-12-31"
}


@app.middleware("http")
async def add_deprecation_warnings(request, call_next):
    """Add deprecation headers to all responses."""
    response = await call_next(request)
    
    # Add deprecation headers
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Tue, 31 Dec 2025 23:59:59 GMT"
    response.headers["Link"] = '</v1>; rel="successor-version"'
    response.headers["Warning"] = '299 - "Deprecated API version"'
    
    # Log deprecation usage
    logger.warning(
        f"DEPRECATED ENDPOINT ACCESSED: {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )
    
    return response


def load_config() -> Dict[str, Any]:
    """Load legacy configuration format."""
    if not os.path.exists(CONFIG_PATH):
        return {"remotes": []}
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f) or {"remotes": []}
    except Exception as e:
        logger.error(f"Failed to load legacy config: {e}")
        return {"remotes": []}


@app.get("/")
async def deprecated_root():
    """Deprecated root endpoint with migration information."""
    return {
        **DEPRECATION_MESSAGE,
        "service": "federation-proxy",
        "current_version": "legacy",
        "recommended_version": "v1",
        "migration_actions": [
            "Update API client to use /v1/* endpoints",
            "Review new federation configuration format",
            "Update endpoint management to use /v1/federation/endpoints",
            "Update proxy requests to use /v1/federation/proxy/*",
            "Migrate health checks to /v1/healthz and /v1/readyz"
        ]
    }


@app.get("/healthz")
def deprecated_healthz():
    """Deprecated health endpoint."""
    return {
        **DEPRECATION_MESSAGE,
        "status": "ok",
        "service": "federation-proxy",
        "new_endpoint": "/v1/healthz",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/remotes")
def deprecated_list_remotes():
    """Deprecated remotes list endpoint."""
    # Still provide basic functionality for backward compatibility
    cfg = load_config()
    
    response_data = {
        **DEPRECATION_MESSAGE,
        "remotes": cfg.get("remotes", []),
        "new_endpoint": "/v1/federation/endpoints",
        "migration_note": "New endpoint provides enhanced federation management with health monitoring, load balancing, and security policies"
    }
    
    return response_data


@app.post("/remotes")
async def deprecated_add_remote():
    """Deprecated add remote endpoint."""
    return JSONResponse(
        status_code=410,
        content={
            **DEPRECATION_MESSAGE,
            "error": "Endpoint permanently moved",
            "new_endpoint": "POST /v1/federation/endpoints",
            "error_code": "ENDPOINT_MOVED",
            "migration_guide": {
                "old_format": {"name": "string", "url": "string", "services": ["list"]},
                "new_format": {
                    "name": "string",
                    "url": "string", 
                    "region": "string",
                    "service_types": ["list"],
                    "weight": "integer",
                    "security_level": "enum",
                    "capabilities": "object"
                }
            }
        }
    )


@app.delete("/remotes/{remote_id}")
async def deprecated_delete_remote():
    """Deprecated delete remote endpoint."""
    return JSONResponse(
        status_code=410,
        content={
            **DEPRECATION_MESSAGE,
            "error": "Endpoint permanently moved",
            "new_endpoint": "DELETE /v1/federation/endpoints/{endpoint_id}",
            "error_code": "ENDPOINT_MOVED"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Show prominent deprecation warning
    print("=" * 80)
    print("⚠️  WARNING: RUNNING DEPRECATED FEDERATION-PROXY VERSION")
    print("=" * 80)
    print("This is the legacy version of the federation-proxy service.")
    print("Please migrate to app_v1.py for production use.")
    print("")
    print("To run the current version:")
    print("  python app_v1.py")
    print("  # OR")
    print("  uvicorn app_v1:app --reload")
    print("")
    print("Legacy API documentation: http://localhost:8000/docs")
    print("New v1 API documentation: http://localhost:8621/docs")
    print("=" * 80)
    
    # Log deprecation warning
    logger.warning("Starting DEPRECATED federation-proxy main.py - migrate to app_v1.py")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
