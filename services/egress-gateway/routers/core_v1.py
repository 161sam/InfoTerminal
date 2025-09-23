"""
Core router for Egress Gateway service.

Provides standard health check endpoints required by all InfoTerminal services.
"""

from fastapi import APIRouter
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
proxy_manager = None
tor_controller = None


def set_dependencies(proxy_mgr, tor_ctrl):
    """Set dependencies from main application."""
    global proxy_manager, tor_controller
    proxy_manager = proxy_mgr
    tor_controller = tor_ctrl


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe - checks if egress gateway service is alive"
)
def healthz() -> HealthResponse:
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    return HealthResponse(
        status="healthy",
        service="egress-gateway",
        version="1.0.0",
        timestamp="2025-09-21T16:45:00Z"
    )


@router.get(
    "/readyz",
    response_model=ReadyResponse,
    summary="Readiness Check",
    description="Readiness probe - checks if egress gateway is ready to process requests"
)
def readyz() -> ReadyResponse:
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including dependency checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    checks = {}
    
    # Check proxy manager
    if proxy_manager is not None:
        try:
            # Basic proxy manager health check
            active_proxy = getattr(proxy_manager, 'get_active_proxy', lambda: "unknown")()
            checks["proxy_manager"] = DependencyCheck(
                status="healthy",
                message=f"Active proxy: {active_proxy}",
                latency_ms=2.0
            )
        except Exception as e:
            checks["proxy_manager"] = DependencyCheck(
                status="unhealthy",
                error=str(e)
            )
    else:
        checks["proxy_manager"] = DependencyCheck(
            status="unhealthy",
            error="Proxy manager not initialized"
        )
    
    # Check Tor controller
    if tor_controller is not None:
        try:
            tor_available = getattr(tor_controller, 'is_available', lambda: False)()
            if tor_available:
                circuit_established = getattr(tor_controller, 'is_circuit_established', lambda: False)()
                checks["tor"] = DependencyCheck(
                    status="healthy" if circuit_established else "degraded",
                    message=f"Tor available, circuit: {'established' if circuit_established else 'not established'}",
                    latency_ms=10.0
                )
            else:
                checks["tor"] = DependencyCheck(
                    status="degraded",
                    message="Tor not available (optional)",
                    latency_ms=5.0
                )
        except Exception as e:
            checks["tor"] = DependencyCheck(
                status="degraded",
                error=f"Tor check failed: {str(e)}"
            )
    else:
        checks["tor"] = DependencyCheck(
            status="disabled",
            message="Tor controller not initialized"
        )
    
    # Determine overall readiness (only proxy_manager is critical)
    critical_healthy = checks["proxy_manager"].status == "healthy"
    overall_status = "ready" if critical_healthy else "not_ready"
    
    return ReadyResponse(
        status=overall_status,
        checks=checks,
        service="egress-gateway",
        version="1.0.0"
    )


@router.get(
    "/info",
    response_model=Dict[str, Any],
    summary="Service Information",
    description="Returns egress gateway service metadata and capabilities"
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    info_data = {
        "service": "egress-gateway",
        "version": "1.0.0",
        "api_version": "v1",
        "description": "Anonymous/secure outbound connections for OSINT research",
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
            "proxy_types": ["tor", "vpn", "proxy", "direct", "auto"],
            "anonymity_levels": ["none", "low", "medium", "high", "extreme"],
            "identity_rotation": True,
            "bulk_requests": True,
            "header_sanitization": True
        }
    }
    
    # Add proxy manager info if available
    if proxy_manager is not None:
        try:
            info_data["proxy_manager"] = {
                "status": "active",
                "active_proxy": getattr(proxy_manager, 'get_active_proxy', lambda: "unknown")(),
                "request_count": getattr(proxy_manager, 'get_request_count', lambda: 0)()
            }
        except Exception:
            info_data["proxy_manager"] = {"status": "error_loading_stats"}
    else:
        info_data["proxy_manager"] = {"status": "not_initialized"}
    
    # Add Tor info if available
    if tor_controller is not None:
        try:
            info_data["tor"] = {
                "available": getattr(tor_controller, 'is_available', lambda: False)(),
                "circuit_established": getattr(tor_controller, 'is_circuit_established', lambda: False)()
            }
        except Exception:
            info_data["tor"] = {"status": "error_loading_stats"}
    else:
        info_data["tor"] = {"status": "not_initialized"}
    
    return info_data
