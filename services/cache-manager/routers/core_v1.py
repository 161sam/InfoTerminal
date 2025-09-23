"""
Core v1 router for cache-manager service.
Provides health checks, readiness, and service info endpoints.
"""

import os
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
        # Check Redis connectivity (optional)
        redis_available = False
        redis_error = None
        try:
            import aioredis
            checks["redis_library_available"] = True
            # Note: Can't test async connection in sync function
            redis_available = True
        except ImportError:
            checks["redis_library_available"] = False
            redis_error = "aioredis library not available"
        
        # Check memory availability for L1 cache
        import psutil
        memory = psutil.virtual_memory()
        checks["memory_status"] = {
            "available_gb": round(memory.available / (1024**3), 2),
            "usage_percent": memory.percent,
            "sufficient_memory": memory.available > 1024**3  # At least 1GB available
        }
        
        # Check compression libraries
        try:
            import gzip
            import base64
            checks["compression_available"] = True
        except ImportError:
            checks["compression_available"] = False
        
        # Check serialization libraries
        try:
            import pickle
            import json
            checks["serialization_available"] = True
        except ImportError:
            checks["serialization_available"] = False
        
        # Overall readiness check
        critical_checks = [
            checks.get("compression_available", False),
            checks.get("serialization_available", False),
            checks.get("memory_status", {}).get("sufficient_memory", False)
        ]
        
        all_ready = all(critical_checks)
        
        return {
            "ready": all_ready,
            "checks": checks,
            "optional_features": {
                "redis_persistence": redis_available,
                "redis_error": redis_error
            }
        }
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "cache-manager",
        "version": "v1",
        "description": "Intelligent multi-level caching service with compression, warming, and automatic invalidation",
        "cache_levels": [
            "L1 (Memory) - Fast in-memory cache with LRU eviction",
            "L2 (Redis) - Shared persistent cache with compression", 
            "L3 (Database) - Long-term persistent storage"
        ],
        "cache_strategies": ["LRU", "LFU", "TTL", "Adaptive"],
        "capabilities": [
            "Multi-level intelligent caching",
            "Automatic compression and decompression",
            "Cache warming strategies",
            "Tag-based and pattern-based invalidation",
            "Automatic API response caching middleware",
            "Performance monitoring and statistics",
            "TTL management and expiration",
            "Size-based cache placement decisions"
        ],
        "features": [
            "Request-based cache key generation",
            "Compression threshold optimization",
            "Access pattern analysis",
            "Cache hit/miss statistics",
            "Intelligent cache level selection",
            "Background cache warming"
        ],
        "build": "latest",
        "git": "main"
    }
