"""
DEPRECATED: feedback-aggregator legacy main.py

This file is deprecated and maintained only for backward compatibility.
All new development should use app_v1.py with the /v1 API endpoints.

⚠️  DEPRECATION NOTICE ⚠️
- This endpoint is deprecated and will be removed in a future version
- Please migrate to the v1 API endpoints at /v1/*
- See /docs for the new API documentation
- Contact the development team for migration assistance

Legacy endpoints still supported:
- GET /health -> Use GET /v1/healthz instead
- GET /feedback -> Use GET /v1/feedback instead  
- POST /feedback -> Use POST /v1/feedback instead
- POST /feedback/{id}/vote -> Use POST /v1/feedback/{id}/vote instead
- GET /feedback/stats -> Use GET /v1/feedback/stats instead

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

# Configure deprecation warnings
warnings.filterwarnings("always", category=DeprecationWarning)
logger = logging.getLogger(__name__)

# Create legacy app for backward compatibility only
app = FastAPI(
    title="Feedback Aggregator Service (DEPRECATED)",
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


@app.get("/")
async def deprecated_root():
    """Deprecated root endpoint with migration information."""
    return {
        **DEPRECATION_MESSAGE,
        "service": "feedback-aggregator",
        "current_version": "legacy",
        "recommended_version": "v1",
        "migration_actions": [
            "Update API client to use /v1/* endpoints",
            "Review new authentication requirements", 
            "Update error handling for standard error envelope",
            "Test pagination changes for list endpoints",
            "Update health check URLs (/health -> /v1/healthz)"
        ]
    }


@app.get("/health")
async def deprecated_health():
    """Deprecated health endpoint."""
    return {
        **DEPRECATION_MESSAGE,
        "status": "healthy", 
        "service": "feedback-aggregator",
        "new_endpoint": "/v1/healthz",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/feedback")
async def deprecated_feedback_list():
    """Deprecated feedback list endpoint."""
    return JSONResponse(
        status_code=410,
        content={
            **DEPRECATION_MESSAGE,
            "error": "Endpoint permanently moved",
            "new_endpoint": "/v1/feedback",
            "error_code": "ENDPOINT_MOVED"
        }
    )


@app.post("/feedback")
async def deprecated_feedback_create():
    """Deprecated feedback creation endpoint."""
    return JSONResponse(
        status_code=410,
        content={
            **DEPRECATION_MESSAGE,
            "error": "Endpoint permanently moved",
            "new_endpoint": "POST /v1/feedback",
            "error_code": "ENDPOINT_MOVED"
        }
    )


@app.post("/feedback/{feedback_id}/vote")
async def deprecated_vote():
    """Deprecated vote endpoint."""
    return JSONResponse(
        status_code=410,
        content={
            **DEPRECATION_MESSAGE,
            "error": "Endpoint permanently moved",
            "new_endpoint": "POST /v1/feedback/{feedback_id}/vote",
            "error_code": "ENDPOINT_MOVED"
        }
    )


@app.get("/feedback/stats")
async def deprecated_stats():
    """Deprecated stats endpoint.""" 
    return JSONResponse(
        status_code=410,
        content={
            **DEPRECATION_MESSAGE,
            "error": "Endpoint permanently moved",
            "new_endpoint": "/v1/feedback/stats",
            "error_code": "ENDPOINT_MOVED"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Show prominent deprecation warning
    print("=" * 80)
    print("⚠️  WARNING: RUNNING DEPRECATED FEEDBACK-AGGREGATOR VERSION")
    print("=" * 80)
    print("This is the legacy version of the feedback-aggregator service.")
    print("Please migrate to app_v1.py for production use.")
    print("")
    print("To run the current version:")
    print("  python app_v1.py")
    print("  # OR")
    print("  uvicorn app_v1:app --reload")
    print("")
    print("Legacy API documentation: http://localhost:8080/docs")
    print("New v1 API documentation: http://localhost:8620/docs")
    print("=" * 80)
    
    # Log deprecation warning
    logger.warning("Starting DEPRECATED feedback-aggregator main.py - migrate to app_v1.py")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
