"""
DEPRECATED: Legacy Egress Gateway Service

This file is DEPRECATED and will be removed in a future version.
Use app_v1.py instead which provides:

- Standard /v1 API namespace
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Enhanced authentication and security
- Improved proxy management

Migration Guide:
- Replace /healthz with /healthz (same, but use app_v1.py)
- Replace /proxy/request with /v1/proxy/request
- Replace /proxy/status with /v1/proxy/status
- Replace /proxy/rotate with /v1/proxy/rotate
- Add authentication headers for write operations
- Update response parsing for Error-Envelope format

For new integrations, use app_v1.py directly.
"""

import warnings
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Issue deprecation warning
warnings.warn(
    "egress-gateway/app.py is deprecated. Use app_v1.py for new integrations. "
    "This legacy service will be removed in the next major version.",
    DeprecationWarning,
    stacklevel=2
)

app = FastAPI(
    title="DEPRECATED - InfoTerminal Egress Gateway (Legacy)",
    description="This is the legacy egress gateway API. Use app_v1.py for new integrations.",
    version="0.2.0-deprecated"
)

# Standard deprecation response
def deprecation_response(new_endpoint: str, method: str = "GET"):
    return JSONResponse(
        content={
            "error": {
                "code": "DEPRECATED_ENDPOINT",
                "message": f"This endpoint is deprecated. Use {new_endpoint} instead.",
                "details": {
                    "migration_guide": "See app_v1.py for the standardized API",
                    "new_endpoint": new_endpoint,
                    "method": method,
                    "breaking_changes": [
                        "Authentication required for write operations",
                        "Error responses use Error-Envelope format",
                        "All endpoints moved to /v1 namespace",
                        "Enhanced request/response models"
                    ]
                }
            }
        },
        status_code=410,  # Gone
        headers={
            "X-Deprecated": f"Use {new_endpoint} instead",
            "X-Migration-Guide": "https://github.com/161sam/InfoTerminal/docs/egress-gateway-migration.md"
        }
    )

# Legacy endpoint redirects
@app.get("/healthz")
async def healthz():
    """Health check - redirects to new implementation."""
    return deprecation_response("/healthz (use app_v1.py)")

@app.get("/health")
async def legacy_health():
    """DEPRECATED: Use /healthz instead.""" 
    return deprecation_response("/healthz")

@app.post("/proxy/request")
async def proxy_request():
    """DEPRECATED: Use /v1/proxy/request instead."""
    return deprecation_response("/v1/proxy/request", "POST")

@app.get("/proxy/status")
async def get_proxy_status():
    """DEPRECATED: Use /v1/proxy/status instead."""
    return deprecation_response("/v1/proxy/status")

@app.post("/proxy/rotate")
async def rotate_proxy():
    """DEPRECATED: Use /v1/proxy/rotate instead."""
    return deprecation_response("/v1/proxy/rotate", "POST")

# Startup/shutdown event handlers for compatibility
@app.on_event("startup")
async def startup_event():
    """Startup event - warns about deprecation."""
    print("WARNING: Using deprecated egress gateway service.")
    print("Please migrate to app_v1.py for the standardized v1 API.")

@app.on_event("shutdown") 
async def shutdown_event():
    """Shutdown event."""
    print("Deprecated egress gateway service shutting down.")

# Root endpoint explaining the deprecation
@app.get("/")
def root():
    """Root endpoint explaining deprecation."""
    return {
        "status": "DEPRECATED",
        "message": "This legacy egress gateway API is deprecated.",
        "migration": {
            "new_service": "app_v1.py",
            "api_version": "v1",
            "documentation": "Use app_v1.py /docs for OpenAPI documentation",
            "authentication": "Basic auth required for write operations in v1",
            "breaking_changes": [
                "All endpoints now use /v1 prefix",
                "Standardized error responses with error envelope",
                "Enhanced proxy request/response models",
                "Authentication required for proxy operations",
                "Improved security and anonymity features",
                "Pagination for list endpoints",
                "Comprehensive statistics and monitoring"
            ]
        },
        "timeline": {
            "deprecation_date": "2025-09-21",
            "removal_date": "2025-12-21",
            "support_status": "Deprecated - use app_v1.py for new integrations"
        },
        "features_in_v1": {
            "enhanced_security": "Improved header sanitization and identity protection",
            "bulk_requests": "Support for batch proxy operations",
            "statistics": "Comprehensive usage and performance metrics",
            "health_monitoring": "Detailed component health checks",
            "rate_limiting": "Built-in rate limiting and throttling",
            "audit_logging": "Enhanced audit trails for compliance"
        }
    }

if __name__ == "__main__":
    print("WARNING: This is the deprecated egress gateway service.")
    print("Use 'python app_v1.py' for the standardized v1 API.")
    print("Legacy service starting with deprecation warnings...")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8615)
