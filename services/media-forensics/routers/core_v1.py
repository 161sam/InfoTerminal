"""
Core v1 router for media-forensics service.
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
        # Check if PIL/Pillow is available
        from PIL import Image
        checks["pil_available"] = True
        
        # Check if imagehash is available
        import imagehash
        checks["imagehash_available"] = True
        
        # Check optional reverse search capability
        bing_api_key = os.getenv("BING_SEARCH_API_KEY")
        checks["reverse_search_configured"] = bool(bing_api_key)
        
        # Check filesystem access for temp files
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b"test")
        checks["temp_file_access"] = True
        
        all_ready = all([
            checks.get("pil_available", False),
            checks.get("imagehash_available", False),
            checks.get("temp_file_access", False)
        ])
        
        return {"ready": all_ready, "checks": checks}
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "media-forensics",
        "version": "v1",
        "description": "Image and video analysis for OSINT investigations",
        "capabilities": [
            "EXIF metadata extraction",
            "Perceptual hashing",
            "Forensic analysis",
            "Image comparison",
            "Reverse image search"
        ],
        "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"],
        "build": "latest",
        "git": "main"
    }
