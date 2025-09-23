"""
Standard Core Router for InfoTerminal Services

This router provides the standardized core endpoints that ALL services must implement:
- /healthz - Liveness probe
- /readyz - Readiness probe  
- /info - Service information

Usage:
Include this router in your main FastAPI app:

from .routers.core_v1 import router as core_router
app.include_router(core_router, tags=["Core"])
"""

from fastapi import APIRouter
from typing import Dict, Any

from _shared.api_standards import (
    HealthResponse,
    ReadyResponse,
    HealthChecker
)

# This will be set by the main application
health_checker: HealthChecker = None

router = APIRouter()


def set_health_checker(hc: HealthChecker) -> None:
    """Set the health checker instance from the main application."""
    global health_checker
    health_checker = hc


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe endpoint - checks if service is running"
)
def healthz() -> HealthResponse:
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    if not health_checker:
        raise RuntimeError("Health checker not initialized")
    
    return health_checker.health_check()


@router.get(
    "/readyz", 
    response_model=ReadyResponse,
    summary="Readiness Check",
    description="Readiness probe endpoint - checks if service is ready to serve traffic"
)
def readyz() -> ReadyResponse:
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including dependency checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    if not health_checker:
        raise RuntimeError("Health checker not initialized")
    
    return health_checker.ready_check()


@router.get(
    "/info",
    response_model=Dict[str, Any],
    summary="Service Information", 
    description="Returns service metadata and capabilities"
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    if not health_checker:
        return {
            "service": "unknown",
            "version": "unknown",
            "status": "health_checker_not_initialized"
        }
    
    return {
        "service": health_checker.service_name,
        "version": health_checker.version,
        "api_version": "v1",
        "status": "running",
        "uptime_seconds": health_checker.start_time,
        "endpoints": {
            "health": "/healthz",
            "readiness": "/readyz", 
            "documentation": "/docs",
            "openapi_spec": "/openapi.json"
        },
        "capabilities": {
            "error_envelope": True,
            "pagination": True,
            "standard_middleware": True,
            "openapi_documentation": True
        }
    }
