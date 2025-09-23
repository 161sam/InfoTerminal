"""
Core v1 router for verification service.
Provides health checks, readiness, and service info endpoints.
"""

import os
import time
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(tags=["Core"])

# Service start time for uptime calculation
_start_time = time.monotonic()


@router.get("/healthz")
def healthz() -> Dict[str, Any]:
    """Liveness probe - returns OK if service is running."""
    return {"ok": True}


@router.get("/readyz")  
def readyz() -> Dict[str, Any]:
    """Readiness probe - checks if service can handle requests."""
    checks = {}
    
    try:
        # Check if Redis is available for caching
        redis_host = os.getenv("VERIFICATION_REDIS_HOST", "redis")
        redis_port = int(os.getenv("VERIFICATION_REDIS_PORT", "6379"))
        
        # Test Redis connection (optional dependency)
        try:
            import redis
            r = redis.Redis(host=redis_host, port=redis_port, socket_timeout=2)
            r.ping()
            checks["redis"] = {"status": "ok", "host": redis_host, "port": redis_port}
        except Exception as e:
            checks["redis"] = {"status": "optional", "error": str(e)}
        
        # Check if ML models can be loaded
        try:
            # Test import of verification service components
            from ..claim_extractor import ClaimExtractor
            from ..stance_classifier import StanceClassifier
            from ..evidence_retrieval import EvidenceRetriever
            checks["ml_models"] = {"status": "ok"}
        except Exception as e:
            checks["ml_models"] = {"status": "fail", "error": str(e)}
            
        # Check filesystem access for temp files
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b"test")
        checks["temp_file_access"] = {"status": "ok"}
        
        # Overall readiness
        critical_checks = ["ml_models", "temp_file_access"]
        all_ready = all(
            checks.get(check, {}).get("status") == "ok" 
            for check in critical_checks
        )
        
        return {"ready": all_ready, "checks": checks}
        
    except Exception as e:
        return {"ready": False, "checks": {"error": str(e)}}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    uptime = time.monotonic() - _start_time
    
    return {
        "service": "verification",
        "version": "v1",
        "description": "Claim extraction, evidence retrieval, stance classification, and credibility assessment for OSINT verification",
        "capabilities": [
            "Claim extraction from text",
            "Evidence retrieval from multiple sources", 
            "Stance classification (support/contradict/neutral)",
            "Source credibility assessment",
            "Media forensics analysis",
            "Image similarity comparison"
        ],
        "uptime_seconds": round(uptime, 2),
        "build": "latest",
        "git": "main"
    }
