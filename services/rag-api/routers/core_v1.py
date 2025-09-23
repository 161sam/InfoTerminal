"""
Core v1 router for rag-api service.
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
        # Check OpenSearch client
        from ..app.opensearch_client import OSClient
        os_url = os.getenv("OS_URL", "http://opensearch:9200")
        os_index = os.getenv("RAG_OS_INDEX", "laws")
        os_client = OSClient(os_url, os_index)
        checks["opensearch"] = os_client.ping()
        
    except Exception as e:
        checks["opensearch"] = {"status": "fail", "error": str(e)}
    
    try:
        # Check Neo4j client
        from ..app.neo4j_client import Neo4jClient
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4j")
        neo_client = Neo4jClient(neo4j_uri, neo4j_user, neo4j_password)
        ok = neo_client.ping()
        checks["neo4j"] = {"status": "ok" if ok else "fail"}
        
    except Exception as e:
        checks["neo4j"] = {"status": "fail", "error": str(e)}
    
    # Overall readiness
    all_ready = all(
        check.get("status") == "ok" 
        for check in checks.values() 
        if isinstance(check, dict)
    )
    
    return {
        "ready": all_ready,
        "checks": checks
    }


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "rag-api",
        "version": "v1", 
        "description": "Legal/Compliance retrieval and graph-based RAG API",
        "capabilities": [
            "Legal document retrieval",
            "Hybrid search (BM25 + KNN)",
            "Vector similarity search",
            "Graph-based context search",
            "Document indexing",
            "Event extraction", 
            "Feedback collection"
        ],
        "search_engines": ["OpenSearch", "Neo4j"],
        "build": "latest",
        "git": "main"
    }
