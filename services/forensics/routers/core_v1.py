"""
Core v1 router for forensics service.
Provides health checks, readiness, and service info endpoints.
"""

import os
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(tags=["Core"])


@router.get("/healthz")
def healthz() -> Dict[str, Any]:
    """Liveness probe - returns OK if service is running."""
    return {"ok": True}


@router.get("/readyz")  
def readyz() -> Dict[str, Any]:
    """Readiness probe - checks if service can handle requests."""
    # Check if ledger directory is accessible
    ledger_path = os.getenv("FORENSICS_LEDGER", "/data/forensics_ledger.jsonl")
    ledger_dir = os.path.dirname(ledger_path)
    
    try:
        os.makedirs(ledger_dir, exist_ok=True)
        # Test write access
        test_file = os.path.join(ledger_dir, ".write_test")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        return {"ready": True, "ledger_dir": ledger_dir}
    except Exception as e:
        return {"ready": False, "error": str(e)}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and version."""
    return {
        "service": "forensics",
        "version": "v1",
        "description": "Digital evidence chain of custody service",
        "build": "latest",
        "git": "main"
    }
