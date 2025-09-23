"""
Core v1 router for performance-monitor service.
Provides health checks, readiness, and service info endpoints.
"""

import os
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
    
    try:
        # Check system monitoring capabilities
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        checks["system_monitoring"] = {
            "cpu_accessible": True,
            "memory_accessible": True,
            "disk_accessible": True,
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "disk_usage_percent": round((disk.used / disk.total) * 100, 2)
        }
        
        # Check Redis connectivity (optional)
        redis_available = False
        try:
            import aioredis
            # Note: Can't test async connection in sync function,
            # so just check if library is available
            checks["redis_library_available"] = True
            redis_available = True
        except ImportError:
            checks["redis_library_available"] = False
        
        # Check numpy availability for analysis
        try:
            import numpy
            checks["numpy_available"] = True
        except ImportError:
            checks["numpy_available"] = False
        
        # Overall readiness check
        critical_checks = [
            checks["system_monitoring"]["cpu_accessible"],
            checks["system_monitoring"]["memory_accessible"],
            checks["system_monitoring"]["disk_accessible"],
            checks.get("numpy_available", False)
        ]
        
        all_ready = all(critical_checks)
        
        return {
            "ready": all_ready,
            "checks": checks,
            "optional_features": {
                "redis_persistence": redis_available
            }
        }
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "performance-monitor",
        "version": "v1",
        "description": "Real-time performance monitoring with metrics collection, analysis, and alerting",
        "capabilities": [
            "API response time monitoring",
            "System resource monitoring (CPU/Memory/Disk)",
            "Performance alert system",
            "Trend analysis and recommendations",
            "Memory leak detection",
            "Error rate tracking",
            "Service-specific performance summaries",
            "Automatic metric collection via middleware"
        ],
        "metric_types": [
            "response_time",
            "memory_usage", 
            "cpu_usage",
            "error_rate",
            "throughput",
            "database_latency"
        ],
        "alert_levels": ["info", "warning", "critical"],
        "build": "latest",
        "git": "main"
    }
