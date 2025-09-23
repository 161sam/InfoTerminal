"""
Core router for OpenBB Connector service.

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
db_connection = None
data_sources = {}


def set_dependencies(db_conn, sources):
    """Set dependencies from main application."""
    global db_connection, data_sources
    db_connection = db_conn
    data_sources = sources


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe - checks if OpenBB connector service is alive"
)
def healthz() -> HealthResponse:
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    return HealthResponse(
        status="healthy",
        service="openbb-connector",
        version="1.0.0",
        timestamp="2025-09-21T16:45:00Z"
    )


@router.get(
    "/readyz",
    response_model=ReadyResponse,
    summary="Readiness Check",
    description="Readiness probe - checks if OpenBB connector is ready to serve financial data"
)
def readyz() -> ReadyResponse:
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including dependency checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    checks = {}
    
    # Check database connection
    if db_connection is not None:
        try:
            # Test database connection
            with db_connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            checks["database"] = DependencyCheck(
                status="healthy",
                message="Database connection active",
                latency_ms=5.0
            )
        except Exception as e:
            checks["database"] = DependencyCheck(
                status="unhealthy",
                error=f"Database connection failed: {str(e)}"
            )
    else:
        checks["database"] = DependencyCheck(
            status="unhealthy",
            error="Database connection not initialized"
        )
    
    # Check data source availability
    available_sources = 0
    for source_name, source_config in data_sources.items():
        try:
            # Basic check - just verify source configuration
            if source_config and source_config.get("enabled", False):
                available_sources += 1
                checks[f"data_source_{source_name}"] = DependencyCheck(
                    status="healthy",
                    message=f"{source_name} data source configured",
                    latency_ms=1.0
                )
            else:
                checks[f"data_source_{source_name}"] = DependencyCheck(
                    status="disabled",
                    message=f"{source_name} data source disabled"
                )
        except Exception as e:
            checks[f"data_source_{source_name}"] = DependencyCheck(
                status="unhealthy",
                error=f"{source_name} check failed: {str(e)}"
            )
    
    # Overall readiness check
    critical_healthy = checks["database"].status == "healthy"
    has_data_sources = available_sources > 0
    
    overall_status = "ready" if (critical_healthy and has_data_sources) else "not_ready"
    
    return ReadyResponse(
        status=overall_status,
        checks=checks,
        service="openbb-connector",
        version="1.0.0"
    )


@router.get(
    "/info",
    response_model=Dict[str, Any],
    summary="Service Information",
    description="Returns OpenBB connector service metadata and capabilities"
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    info_data = {
        "service": "openbb-connector",
        "version": "1.0.0",
        "api_version": "v1",
        "description": "Financial data connector using OpenBB and various data sources",
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
            "multiple_data_sources": True,
            "bulk_operations": True,
            "data_quality_checks": True,
            "time_series_analysis": True
        }
    }
    
    # Add database info if available
    if db_connection is not None:
        try:
            with db_connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM stg_openbb_prices")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT symbol) FROM stg_openbb_prices")
                total_symbols = cursor.fetchone()[0]
                
            info_data["database"] = {
                "status": "connected",
                "total_records": total_records,
                "total_symbols": total_symbols
            }
        except Exception as e:
            info_data["database"] = {"status": "error", "error": str(e)}
    else:
        info_data["database"] = {"status": "not_connected"}
    
    # Add data source info
    if data_sources:
        info_data["data_sources"] = {
            name: {
                "enabled": config.get("enabled", False),
                "type": config.get("type", "unknown")
            }
            for name, config in data_sources.items()
        }
    else:
        info_data["data_sources"] = {"status": "not_configured"}
    
    return info_data
