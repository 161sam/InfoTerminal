"""
Agent Connector Service - Standardized v1 Application

This service provides plugin management, discovery, and execution capabilities
for the InfoTerminal platform. All endpoints follow InfoTerminal API standards.

Features:
- Plugin registry management
- Plugin state and configuration management
- Tool discovery and invocation
- Health monitoring
- User and global scoped settings
- Audit logging
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent
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

from .routers import core_v1, plugins_v1

# Service Configuration
SERVICE_NAME = "agent-connector"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "Plugin management and tool execution service for InfoTerminal agents"

# Health checker instance
health_checker = HealthChecker(SERVICE_NAME, SERVICE_VERSION)


def check_plugins_directory() -> DependencyCheck:
    """Check if plugins directory is accessible."""
    try:
        plugins_dir = Path(os.getenv("IT_PLUGINS_DIR", "plugins"))
        if plugins_dir.exists() and plugins_dir.is_dir():
            return DependencyCheck(
                status="healthy",
                latency_ms=1.0
            )
        else:
            return DependencyCheck(
                status="unhealthy",
                error=f"Plugins directory not found: {plugins_dir}"
            )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=f"Failed to check plugins directory: {str(e)}"
        )


def check_audit_service() -> DependencyCheck:
    """Check if audit logging service is available."""
    try:
        # This is a basic check - in production, you might ping an actual service
        from services.common.audit import audit_log
        
        # Test audit logging
        audit_log("system.health_check", "system", "default", {"service": SERVICE_NAME}, "test")
        
        return DependencyCheck(
            status="healthy",
            latency_ms=2.0
        )
    except Exception as e:
        return DependencyCheck(
            status="degraded",  # Audit logging is not critical for core functionality
            error=f"Audit service unavailable: {str(e)}"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    print(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    # Add dependency checks
    health_checker.add_dependency("plugins_directory", check_plugins_directory)
    health_checker.add_dependency("audit_service", check_audit_service)
    
    # Set health checker for routers
    core_v1.set_health_checker(health_checker)
    
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

# Include core endpoints (healthz, readyz, info)
app.include_router(
    core_v1.router,
    tags=["Core"]
)

# Include v1 plugin management endpoints
app.include_router(
    plugins_v1.router,
    prefix="/v1/plugins",
    tags=["Plugins"]
)

# =============================================================================
# LEGACY ENDPOINTS (DEPRECATED)
# =============================================================================
# Keep legacy endpoints for backward compatibility with deprecation warnings

@app.get("/healthz", deprecated=True, tags=["Legacy"])
def legacy_healthz():
    """
    DEPRECATED: Use /healthz instead.
    Legacy health endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"status": "healthy", "message": "Use /healthz instead"},
        headers={"X-Deprecated": "Use /healthz instead"}
    )


@app.get("/readyz", deprecated=True, tags=["Legacy"])
def legacy_readyz():
    """
    DEPRECATED: Use /readyz instead.
    Legacy readiness endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"status": "ready", "message": "Use /readyz instead"},
        headers={"X-Deprecated": "Use /readyz instead"}
    )


# Legacy plugin endpoints with deprecation warnings
@app.get("/plugins/registry", deprecated=True, tags=["Legacy"])
def legacy_plugin_registry():
    """
    DEPRECATED: Use /v1/plugins/registry instead.
    Legacy plugin registry endpoint.
    """
    return JSONResponse(
        content={
            "error": "This endpoint is deprecated",
            "message": "Use /v1/plugins/registry instead",
            "new_endpoint": "/v1/plugins/registry"
        },
        status_code=410,
        headers={"X-Deprecated": "Use /v1/plugins/registry instead"}
    )


@app.get("/plugins/state", deprecated=True, tags=["Legacy"])
def legacy_plugin_state():
    """
    DEPRECATED: Use /v1/plugins/state instead.
    Legacy plugin state endpoint.
    """
    return JSONResponse(
        content={
            "error": "This endpoint is deprecated",
            "message": "Use /v1/plugins/state instead",
            "new_endpoint": "/v1/plugins/state"
        },
        status_code=410,
        headers={"X-Deprecated": "Use /v1/plugins/state instead"}
    )


@app.get("/plugins/tools", deprecated=True, tags=["Legacy"])
def legacy_plugin_tools():
    """
    DEPRECATED: Use /v1/plugins/tools instead.
    Legacy tools discovery endpoint.
    """
    return JSONResponse(
        content={
            "error": "This endpoint is deprecated",
            "message": "Use /v1/plugins/tools instead",
            "new_endpoint": "/v1/plugins/tools"
        },
        status_code=410,
        headers={"X-Deprecated": "Use /v1/plugins/tools instead"}
    )


@app.post("/plugins/invoke/{plugin}/{tool}", deprecated=True, tags=["Legacy"])
def legacy_plugin_invoke(plugin: str, tool: str):
    """
    DEPRECATED: Use /v1/plugins/invoke/{plugin}/{tool} instead.
    Legacy tool invocation endpoint.
    """
    return JSONResponse(
        content={
            "error": "This endpoint is deprecated",
            "message": f"Use /v1/plugins/invoke/{plugin}/{tool} instead",
            "new_endpoint": f"/v1/plugins/invoke/{plugin}/{tool}"
        },
        status_code=410,
        headers={"X-Deprecated": f"Use /v1/plugins/invoke/{plugin}/{tool} instead"}
    )


if __name__ == "__main__":
    import uvicorn
    
    # Port configuration from environment or default
    default_port = 8617  # Agent connector port from patch_ports.sh
    port = int(os.getenv("PORT", default_port))
    
    uvicorn.run(
        "app_v1:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
