"""
Core router for Plugin Runner service.

Provides standard health check endpoints required by all InfoTerminal services.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any

import sys
from pathlib import Path

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import HealthResponse, ReadyResponse, DependencyCheck

router = APIRouter()

# Will be injected by main app
plugin_registry = None
docker_client = None


def set_dependencies(registry, docker):
    """Set dependencies from main application."""
    global plugin_registry, docker_client
    plugin_registry = registry
    docker_client = docker


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe - checks if plugin runner service is alive"
)
def healthz() -> HealthResponse:
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    return HealthResponse(
        status="healthy",
        service="plugin-runner",
        version="1.0.0",
        timestamp="2025-09-21T16:45:00Z"
    )


@router.get(
    "/readyz",
    response_model=ReadyResponse,
    summary="Readiness Check", 
    description="Readiness probe - checks if plugin runner is ready to execute plugins"
)
def readyz() -> ReadyResponse:
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including dependency checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    checks = {}
    
    # Check plugin registry
    if plugin_registry is not None:
        try:
            plugin_count = len(plugin_registry.plugins)
            checks["plugin_registry"] = DependencyCheck(
                status="healthy",
                message=f"{plugin_count} plugins loaded",
                latency_ms=1.0
            )
        except Exception as e:
            checks["plugin_registry"] = DependencyCheck(
                status="unhealthy",
                error=str(e)
            )
    else:
        checks["plugin_registry"] = DependencyCheck(
            status="unhealthy", 
            error="Plugin registry not initialized"
        )
    
    # Check Docker if enabled
    if docker_client is not None:
        try:
            docker_client.ping()
            checks["docker"] = DependencyCheck(
                status="healthy",
                message="Docker daemon accessible",
                latency_ms=5.0
            )
        except Exception as e:
            checks["docker"] = DependencyCheck(
                status="unhealthy",
                error=f"Docker unavailable: {str(e)}"
            )
    else:
        checks["docker"] = DependencyCheck(
            status="disabled",
            message="Docker execution disabled"
        )
    
    # Determine overall readiness
    all_critical_healthy = checks["plugin_registry"].status == "healthy"
    overall_status = "ready" if all_critical_healthy else "not_ready"
    
    return ReadyResponse(
        status=overall_status,
        checks=checks,
        service="plugin-runner",
        version="1.0.0"
    )


@router.get(
    "/info",
    response_model=Dict[str, Any],
    summary="Service Information",
    description="Returns plugin runner service metadata and capabilities"
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    info_data = {
        "service": "plugin-runner",
        "version": "1.0.0",
        "api_version": "v1",
        "description": "Secure execution of OSINT and security tools",
        "status": "running",
        "endpoints": {
            "health": "/healthz",
            "readiness": "/readyz",
            "documentation": "/docs",
            "openapi_spec": "/openapi.json"
        },
        "capabilities": {
            "error_envelope": True,
            "pagination": True,
            "background_jobs": True,
            "docker_execution": docker_client is not None,
            "batch_execution": True,
            "priority_queuing": True
        }
    }
    
    # Add plugin statistics if registry is available
    if plugin_registry is not None:
        try:
            info_data["plugins"] = {
                "total_loaded": len(plugin_registry.plugins),
                "categories": len(set(p.category for p in plugin_registry.plugins.values())),
                "registry_path": str(plugin_registry.plugins_dir)
            }
        except Exception:
            info_data["plugins"] = {"status": "error_loading_stats"}
    else:
        info_data["plugins"] = {"status": "not_initialized"}
    
    return info_data
