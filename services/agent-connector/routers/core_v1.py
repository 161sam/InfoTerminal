"""
Core Router for Agent Connector Service

Provides standardized health, readiness, and info endpoints.
All InfoTerminal services must implement these endpoints.
"""

import sys
from pathlib import Path
from fastapi import APIRouter
from typing import Dict, Any

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    HealthResponse,
    ReadyResponse,
    HealthChecker,
    DependencyCheck
)

router = APIRouter()

# This will be set by the main application
health_checker: HealthChecker = None


def set_health_checker(hc: HealthChecker) -> None:
    """Set the health checker instance from the main application."""
    global health_checker
    health_checker = hc


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe endpoint - checks if service is running",
    tags=["Core"]
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
    description="Readiness probe endpoint - checks if service is ready to serve traffic",
    tags=["Core"]
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
    description="Returns service metadata and capabilities",
    tags=["Core"]
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    if not health_checker:
        return {
            "service": "agent-connector",
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
            "plugin_management": True,
            "plugin_registry": True,
            "plugin_state": True,
            "plugin_configuration": True,
            "plugin_health_checks": True,
            "tool_discovery": True,
            "tool_invocation": True,
            "user_scoped_settings": True,
            "global_settings": True,
            "audit_logging": True,
            "error_envelope": True,
            "pagination": True,
            "standard_middleware": True,
            "openapi_documentation": True
        }
    }
