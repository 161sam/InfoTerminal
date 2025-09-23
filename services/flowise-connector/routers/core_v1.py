"""
Flowise Connector Core Router - v1 Standardized

Provides standardized health and info endpoints for the Flowise Connector service.
"""

import os
import sys
from pathlib import Path

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from fastapi import APIRouter
from typing import Dict, Any

from _shared.api_standards import (
    HealthResponse,
    ReadyResponse,
    HealthChecker,
    DependencyCheck
)

# Service configuration
SERVICE_NAME = "flowise-connector"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "AI Agent workflow orchestration for OSINT operations"

# Health checker instance
health_checker = HealthChecker(SERVICE_NAME, SERVICE_VERSION)

router = APIRouter()


def check_flowise_connection() -> DependencyCheck:
    """Check Flowise API connectivity."""
    try:
        import httpx
        
        flowise_url = os.getenv("AGENT_BASE_URL", "http://localhost:3417")
        
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{flowise_url}/api/v1/prediction")
            
        if response.status_code < 500:
            return DependencyCheck(
                status="healthy",
                latency_ms=response.elapsed.total_seconds() * 1000,
                details={"flowise_url": flowise_url}
            )
        else:
            return DependencyCheck(
                status="unhealthy",
                error=f"Flowise returned {response.status_code}",
                details={"flowise_url": flowise_url}
            )
            
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e),
            details={"flowise_url": os.getenv("AGENT_BASE_URL", "http://localhost:3417")}
        )


def check_internal_services() -> DependencyCheck:
    """Check connectivity to internal InfoTerminal services."""
    try:
        import httpx
        
        # Check key internal services
        services = {
            "search-api": f"http://localhost:{os.getenv('IT_PORT_SEARCH_API', '8611')}/healthz",
            "graph-api": f"http://localhost:{os.getenv('IT_PORT_GRAPH_API', '8612')}/healthz"
        }
        
        with httpx.Client(timeout=3.0) as client:
            for service_name, url in services.items():
                try:
                    response = client.get(url)
                    if response.status_code >= 400:
                        return DependencyCheck(
                            status="unhealthy",
                            error=f"{service_name} unhealthy: {response.status_code}",
                            details={"failed_service": service_name}
                        )
                except Exception as e:
                    return DependencyCheck(
                        status="unhealthy",
                        error=f"{service_name} unreachable: {str(e)}",
                        details={"failed_service": service_name}
                    )
        
        return DependencyCheck(
            status="healthy",
            latency_ms=10.0,
            details={"checked_services": list(services.keys())}
        )
        
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


# Add dependency checks
health_checker.add_dependency("flowise", check_flowise_connection)
health_checker.add_dependency("internal_services", check_internal_services)


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe endpoint - checks if flowise-connector is running"
)
def healthz() -> HealthResponse:
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    return health_checker.health_check()


@router.get(
    "/readyz", 
    response_model=ReadyResponse,
    summary="Readiness Check",
    description="Readiness probe endpoint - checks if service and dependencies are ready"
)
def readyz() -> ReadyResponse:
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including Flowise and internal service checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    return health_checker.ready_check()


@router.get(
    "/info",
    response_model=Dict[str, Any],
    summary="Service Information", 
    description="Returns flowise-connector service metadata and capabilities"
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "api_version": "v1",
        "status": "running",
        "configuration": {
            "flowise_url": os.getenv("AGENT_BASE_URL", "http://localhost:3417"),
            "n8n_enabled": bool(os.getenv("N8N_BASE_URL")),
            "metrics_enabled": os.getenv("IT_ENABLE_METRICS") == "1"
        },
        "endpoints": {
            "health": "/healthz",
            "readiness": "/readyz", 
            "documentation": "/docs",
            "openapi_spec": "/openapi.json",
            "agents": "/v1/agents",
            "metrics": "/metrics" if os.getenv("IT_ENABLE_METRICS") == "1" else None
        },
        "capabilities": {
            "error_envelope": True,
            "pagination": True,
            "standard_middleware": True,
            "openapi_documentation": True,
            "agent_orchestration": True,
            "tool_execution": True,
            "conversation_management": True
        }
    }
