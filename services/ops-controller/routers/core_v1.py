"""
Core v1 router for ops-controller service.
Provides health checks, readiness, and service info endpoints.
"""

import os
import time
import psutil
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(tags=["Core"])


@router.get("/healthz")
def healthz() -> Dict[str, Any]:
    """Liveness probe - returns OK if service is running."""
    return {"ok": True}


@router.get("/readyz")  
def readyz() -> Dict[str, Any]:
    """Readiness probe - checks if service can handle requests."""
    checks = {}
    enabled = os.getenv("IT_OPS_ENABLE", "0") == "1"
    
    try:
        # Check if ops is enabled
        checks["ops_enabled"] = enabled
        
        # Check system resources
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        checks["system_resources"] = {
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_usage, 
            "disk_usage_percent": disk_usage,
            "high_resource_usage": cpu_usage > 90 or memory_usage > 90 or disk_usage > 90
        }
        
        # Check Docker availability if enabled
        if enabled:
            try:
                import docker
                client = docker.from_env()
                client.ping()
                checks["docker_available"] = True
            except Exception as e:
                checks["docker_available"] = False
                checks["docker_error"] = str(e)
        
        # Check stacks file if enabled
        if enabled:
            stacks_file = os.getenv("IT_OPS_STACKS_FILE", "infra/ops/stacks.yaml")
            checks["stacks_file_exists"] = os.path.exists(stacks_file)
        
        # Determine overall readiness
        critical_checks = [
            checks.get("system_resources", {}).get("high_resource_usage", True) == False,
            not enabled or checks.get("docker_available", False),
            not enabled or checks.get("stacks_file_exists", False)
        ]
        
        all_ready = all(critical_checks)
        
        return {"ready": all_ready, "checks": checks}
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    enabled = os.getenv("IT_OPS_ENABLE", "0") == "1"
    mode = os.getenv("IT_OPS_MODE", "docker")
    
    return {
        "service": "ops-controller",
        "version": "v1",
        "description": "Operations controller for service orchestration and security management",
        "enabled": enabled,
        "mode": mode,
        "capabilities": [
            "Stack management (up/down/restart/scale)",
            "Container operations",
            "Security incognito sessions",
            "Data wiping and cleanup",
            "Performance monitoring",
            "Health checks",
            "Log streaming",
            "Emergency shutdown"
        ],
        "rbac_required": True,
        "build": "latest",
        "git": "main"
    }
