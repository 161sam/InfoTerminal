"""
Core v1 router for xai service.
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
        # Check if structlog is available
        try:
            import structlog
            checks["structlog"] = {"status": "ok"}
        except ImportError:
            checks["structlog"] = {"status": "optional", "error": "structlog not available"}
        
        # Check if optional ML libraries are available
        ml_libraries = []
        try:
            import transformers
            ml_libraries.append("transformers")
        except ImportError:
            pass
            
        try:
            import torch
            ml_libraries.append("torch")
        except ImportError:
            pass
            
        try:
            import shap
            ml_libraries.append("shap")
        except ImportError:
            pass
            
        checks["ml_libraries"] = {
            "status": "ok" if ml_libraries else "limited",
            "available": ml_libraries,
            "message": "Advanced explainability available" if ml_libraries else "Basic heuristic explainability only"
        }
        
        # Test basic text processing
        test_text = "This is a test sentence."
        tokens = test_text.split()
        if len(tokens) > 0:
            checks["text_processing"] = {"status": "ok"}
        else:
            checks["text_processing"] = {"status": "fail", "error": "Text tokenization failed"}
        
        # Overall readiness
        critical_checks = ["text_processing"]
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
    return {
        "service": "xai",
        "version": "v1",
        "description": "Explainable AI service for model interpretability and decision transparency",
        "capabilities": [
            "Text explanation with token highlighting",
            "Query-based relevance highlighting",
            "Heuristic pattern detection",
            "Model transparency reporting",
            "Confidence scoring"
        ],
        "explanation_methods": [
            "heuristic_highlighting",
            "query_matching", 
            "pattern_detection",
            "attention_visualization"
        ],
        "build": "latest",
        "git": "main"
    }
