"""
DEPRECATED: Legacy Plugin Runner Service

This file is DEPRECATED and will be removed in a future version.
Use app_v1.py instead which provides:

- Standard /v1 API namespace
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Background job processing

Migration Guide:
- Replace /health with /healthz
- Replace /plugins with /v1/plugins
- Replace /execute with /v1/plugins/{plugin_name}/execute
- Replace /jobs/{job_id} with /v1/jobs/{job_id}
- Replace /categories with /v1/categories
- Replace /statistics with /v1/statistics

For new integrations, use app_v1.py directly.
"""

import warnings
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Issue deprecation warning
warnings.warn(
    "plugin-runner/app.py is deprecated. Use app_v1.py for new integrations. "
    "This legacy service will be removed in the next major version.",
    DeprecationWarning,
    stacklevel=2
)

app = FastAPI(
    title="DEPRECATED - InfoTerminal Plugin Runner (Legacy)",
    description="This is the legacy plugin runner API. Use app_v1.py for new integrations.",
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
                    "method": method
                }
            }
        },
        status_code=410,  # Gone
        headers={
            "X-Deprecated": f"Use {new_endpoint} instead",
            "X-Migration-Guide": "https://github.com/161sam/InfoTerminal/docs/plugin-runner-migration.md"
        }
    )

# Legacy endpoint redirects
@app.get("/healthz")
def healthz():
    """Health check - redirects to new implementation."""
    return deprecation_response("/healthz (use app_v1.py)")

@app.get("/readyz") 
def readyz():
    """Readiness check - redirects to new implementation."""
    return deprecation_response("/readyz (use app_v1.py)")

@app.get("/health")
def legacy_health():
    """DEPRECATED: Use /healthz instead."""
    return deprecation_response("/healthz")

@app.get("/plugins")
def list_plugins():
    """DEPRECATED: Use /v1/plugins instead."""
    return deprecation_response("/v1/plugins")

@app.get("/plugins/{plugin_name}")
def get_plugin_info(plugin_name: str):
    """DEPRECATED: Use /v1/plugins/{plugin_name} instead."""
    return deprecation_response(f"/v1/plugins/{plugin_name}")

@app.post("/execute")
def execute_plugin():
    """DEPRECATED: Use /v1/plugins/{plugin_name}/execute instead."""
    return deprecation_response("/v1/plugins/{plugin_name}/execute", "POST")

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    """DEPRECATED: Use /v1/jobs/{job_id} instead."""
    return deprecation_response(f"/v1/jobs/{job_id}")

@app.get("/jobs")
def list_jobs():
    """DEPRECATED: Use /v1/jobs instead."""
    return deprecation_response("/v1/jobs")

@app.delete("/jobs/{job_id}")
def cancel_job(job_id: str):
    """DEPRECATED: Use /v1/jobs/{job_id} instead."""
    return deprecation_response(f"/v1/jobs/{job_id}", "DELETE")

@app.get("/categories")
def get_plugin_categories():
    """DEPRECATED: Use /v1/categories instead."""
    return deprecation_response("/v1/categories")

@app.get("/statistics")
def get_statistics():
    """DEPRECATED: Use /v1/statistics instead."""
    return deprecation_response("/v1/statistics")

# Root endpoint explaining the deprecation
@app.get("/")
def root():
    """Root endpoint explaining deprecation."""
    return {
        "status": "DEPRECATED",
        "message": "This legacy plugin runner API is deprecated.",
        "migration": {
            "new_service": "app_v1.py",
            "api_version": "v1",
            "documentation": "Use app_v1.py /docs for OpenAPI documentation",
            "breaking_changes": [
                "All endpoints now use /v1 prefix",
                "Standardized error responses with error envelope",
                "Pagination for list endpoints",
                "Enhanced health check endpoints"
            ]
        },
        "timeline": {
            "deprecation_date": "2025-09-21",
            "removal_date": "2025-12-21",
            "support_status": "Deprecated - use app_v1.py for new integrations"
        }
    }

if __name__ == "__main__":
    print("WARNING: This is the deprecated plugin runner service.")
    print("Use 'python app_v1.py' for the standardized v1 API.")
    print("Legacy service starting with deprecation warnings...")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
