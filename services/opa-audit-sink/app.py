"""
DEPRECATED: Legacy OPA Audit Sink Service

This file is DEPRECATED and will be removed in a future version.
Use app_v1.py instead which provides:

- Standard /v1 API namespace
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Enhanced audit analytics
- Retention policy management
- Comprehensive statistics
- Audit health monitoring

Migration Guide:
- Replace POST /logs with POST /v1/logs
- Replace GET /healthz with /healthz (same endpoint, but use app_v1.py)
- Add authentication headers for write operations
- Update response parsing for Error-Envelope format
- Use new endpoints: /v1/statistics, /v1/health/comprehensive, /v1/capabilities

For new integrations, use app_v1.py directly.
"""

import warnings
import os
import datetime
import json
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Issue deprecation warning
warnings.warn(
    "opa-audit-sink/app.py is deprecated. Use app_v1.py for new integrations. "
    "This legacy service will be removed in the next major version.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy configuration (kept for compatibility)
CH = os.getenv("CH_URL", "http://clickhouse.clickhouse.svc.cluster.local:8123")
CH_DB = os.getenv("CH_DB", "logs")
CH_TABLE = os.getenv("CH_TABLE", "opa_decisions")

app = FastAPI(
    title="DEPRECATED - OPA Audit Sink (Legacy)",
    description="This is the legacy OPA audit sink API. Use app_v1.py for new integrations.",
    version="0.1.0-deprecated"
)


def deprecation_response(new_endpoint: str, method: str = "GET"):
    """Standard deprecation response."""
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
                        "All endpoints moved to /v1 namespace",
                        "Error responses use Error-Envelope format",
                        "Enhanced audit analytics and statistics",
                        "Retention policy management",
                        "Health monitoring endpoints",
                        "OpenAPI documentation available"
                    ]
                }
            }
        },
        status_code=410,  # Gone
        headers={
            "X-Deprecated": f"Use {new_endpoint} instead",
            "X-Migration-Guide": "https://github.com/161sam/InfoTerminal/docs/opa-audit-sink-migration.md"
        }
    )


def _row(e: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy row transformation (kept for compatibility)."""
    ts = e.get("timestamp") or datetime.datetime.utcnow().isoformat()
    path = e.get("path", "")
    decision_id = e.get("decision_id", "")
    inp = e.get("input", {}) or {}
    user = ((inp.get("user") or {}).get("username")) or ""
    roles = (inp.get("user") or {}).get("roles") or []
    tenant = (inp.get("user") or {}).get("tenant") or ""
    cls = (inp.get("resource") or {}).get("classification") or ""
    action = inp.get("action") or ""
    res = e.get("result", False)
    return {
        "ts": ts, "path": path, "decision_id": decision_id, "user": user,
        "roles": roles, "tenant": tenant, "classification": cls, "action": action,
        "allowed": 1 if bool(res) else 0,
        "policy_version": e.get("bundles", {}).get("main", {}).get("revision", ""),
        "raw": json.dumps(e, separators=(",", ":"))
    }


@app.get("/healthz")
def health():
    """DEPRECATED: Use /healthz in app_v1.py instead."""
    return deprecation_response("/healthz (use app_v1.py)")


@app.post("/logs")
async def logs():
    """DEPRECATED: Use /v1/logs instead."""
    return deprecation_response("/v1/logs", "POST")


@app.get("/metrics")
def metrics():
    """DEPRECATED: Use /v1/statistics instead."""
    return deprecation_response("/v1/statistics")


# Root endpoint explaining the deprecation
@app.get("/")
def root():
    """Root endpoint explaining deprecation."""
    return {
        "status": "DEPRECATED",
        "message": "This legacy OPA audit sink API is deprecated.",
        "migration": {
            "new_service": "app_v1.py",
            "api_version": "v1",
            "documentation": "Use app_v1.py /docs for OpenAPI documentation",
            "breaking_changes": [
                "All endpoints now use /v1 prefix",
                "Standardized error responses with error envelope",
                "Enhanced audit analytics and statistics",
                "Retention policy management",
                "Comprehensive health monitoring",
                "Real-time audit capabilities",
                "Audit system configuration management"
            ]
        },
        "timeline": {
            "deprecation_date": "2025-09-22",
            "removal_date": "2025-12-22",
            "support_status": "Deprecated - use app_v1.py for new integrations"
        },
        "features_in_v1": {
            "enhanced_analytics": "Comprehensive audit statistics and trending",
            "retention_management": "Automated log retention policies",
            "health_monitoring": "Detailed component health checks",
            "configuration_api": "Runtime configuration management",
            "bulk_operations": "Bulk log ingestion and processing",
            "audit_capabilities": "System capabilities and limits reporting"
        },
        "legacy_endpoints": {
            "/logs": "→ /v1/logs (POST - OPA decision log ingestion)",
            "/healthz": "→ /healthz (GET - basic health check, use app_v1.py)",
            "/metrics": "→ /v1/statistics (GET - comprehensive audit statistics)"
        },
        "new_endpoints": {
            "/v1/logs": "OPA decision log ingestion",
            "/v1/logs/bulk": "Bulk log ingestion",
            "/v1/logs/query": "Query audit logs",
            "/v1/statistics": "Comprehensive audit statistics", 
            "/v1/health/comprehensive": "Detailed health status",
            "/v1/capabilities": "System capabilities",
            "/v1/retention/policy": "Retention policy management",
            "/v1/config": "Configuration management"
        }
    }


if __name__ == "__main__":
    print("WARNING: This is the deprecated OPA audit sink service.", file=sys.stderr)
    print("Use 'python app_v1.py' for the standardized v1 API.", file=sys.stderr)
    print("Legacy service starting with deprecation warnings...", file=sys.stderr)
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
