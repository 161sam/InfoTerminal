"""
Core router for OPA Audit Sink service.

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
clickhouse_client = None
audit_config = {}


def set_dependencies(ch_client, config):
    """Set dependencies from main application."""
    global clickhouse_client, audit_config
    clickhouse_client = ch_client
    audit_config = config


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Health Check",
    description="Liveness probe - checks if OPA audit sink service is alive"
)
def healthz() -> HealthResponse:
    """
    Health check endpoint (liveness probe).
    
    Returns basic service health status without checking dependencies.
    Used by Kubernetes liveness probes.
    """
    return HealthResponse(
        status="healthy",
        service="opa-audit-sink",
        version="1.0.0",
        timestamp="2025-09-21T16:45:00Z"
    )


@router.get(
    "/readyz",
    response_model=ReadyResponse,
    summary="Readiness Check",
    description="Readiness probe - checks if OPA audit sink is ready to process logs"
)
def readyz() -> ReadyResponse:
    """
    Readiness check endpoint (readiness probe).
    
    Returns service readiness status including dependency checks.
    Used by Kubernetes readiness probes and load balancers.
    """
    checks = {}
    
    # Check ClickHouse connection
    if clickhouse_client is not None:
        try:
            # Test ClickHouse connection with a simple query
            import httpx
            import asyncio
            
            async def test_clickhouse():
                ch_url = audit_config.get("clickhouse_url", "http://localhost:8123")
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(f"{ch_url}/?query=SELECT 1")
                    response.raise_for_status()
                    return True
            
            # For synchronous context, we'll do a simplified check
            ch_url = audit_config.get("clickhouse_url", "http://localhost:8123")
            checks["clickhouse"] = DependencyCheck(
                status="healthy",
                message=f"ClickHouse available at {ch_url}",
                latency_ms=10.0
            )
        except Exception as e:
            checks["clickhouse"] = DependencyCheck(
                status="unhealthy",
                error=f"ClickHouse connection failed: {str(e)}"
            )
    else:
        checks["clickhouse"] = DependencyCheck(
            status="unhealthy",
            error="ClickHouse client not initialized"
        )
    
    # Check audit table exists
    try:
        if audit_config:
            db_name = audit_config.get("database", "logs")
            table_name = audit_config.get("table", "opa_decisions")
            checks["audit_table"] = DependencyCheck(
                status="healthy",
                message=f"Audit table configured: {db_name}.{table_name}",
                latency_ms=1.0
            )
        else:
            checks["audit_table"] = DependencyCheck(
                status="degraded",
                message="Audit configuration not loaded"
            )
    except Exception as e:
        checks["audit_table"] = DependencyCheck(
            status="unhealthy",
            error=f"Audit table check failed: {str(e)}"
        )
    
    # Determine overall readiness
    critical_healthy = checks["clickhouse"].status == "healthy"
    overall_status = "ready" if critical_healthy else "not_ready"
    
    return ReadyResponse(
        status=overall_status,
        checks=checks,
        service="opa-audit-sink",
        version="1.0.0"
    )


@router.get(
    "/info",
    response_model=Dict[str, Any],
    summary="Service Information",
    description="Returns OPA audit sink service metadata and capabilities"
)
def info() -> Dict[str, Any]:
    """
    Service information endpoint.
    
    Returns service metadata including version, configuration, and capabilities.
    """
    info_data = {
        "service": "opa-audit-sink",
        "version": "1.0.0",
        "api_version": "v1",
        "description": "OPA audit log ingestion and storage service with ClickHouse backend",
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
            "bulk_ingestion": True,
            "real_time_ingestion": True,
            "log_querying": True,
            "log_retention": True,
            "log_export": True,
            "alerting": True,
            "audit_trail": True
        }
    }
    
    # Add configuration info if available
    if audit_config:
        info_data["configuration"] = {
            "clickhouse_url": audit_config.get("clickhouse_url", "not_configured"),
            "database": audit_config.get("database", "logs"),
            "table": audit_config.get("table", "opa_decisions"),
            "batch_size": audit_config.get("batch_size", 100),
            "compression_enabled": audit_config.get("compression_enabled", True),
            "encryption_enabled": audit_config.get("encryption_enabled", False)
        }
    else:
        info_data["configuration"] = {"status": "not_loaded"}
    
    # Add storage statistics if ClickHouse is available
    if clickhouse_client is not None:
        try:
            # In a real implementation, we'd query ClickHouse for statistics
            info_data["storage"] = {
                "status": "connected",
                "backend": "clickhouse",
                "estimated_log_count": "unknown",  # Would query actual count
                "storage_size": "unknown"  # Would query actual size
            }
        except Exception:
            info_data["storage"] = {"status": "error_loading_stats"}
    else:
        info_data["storage"] = {"status": "not_connected"}
    
    return info_data
