"""
RAG API Service v1 - Legal Document Retrieval and Graph-based Search

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Hybrid search capabilities
- Graph-based context search
"""

import logging
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

# Add service and repo to path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Import routers
from routers.core_v1 import router as core_router
from routers.rag_v1 import router as rag_router

# Import shared standards
try:
    from _shared.api_standards.middleware import setup_standard_middleware
    from _shared.api_standards.error_schemas import StandardError
    HAS_SHARED_STANDARDS = True
except ImportError:
    HAS_SHARED_STANDARDS = False
    logging.warning("Shared API standards not available, using fallback")

# Import legacy CORS if available
try:
    from _shared.cors import apply_cors, get_cors_settings_from_env
    HAS_LEGACY_CORS = True
except ImportError:
    HAS_LEGACY_CORS = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG API Service",
    description="Legal document retrieval and graph-based search with hybrid AI capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup middleware
if HAS_SHARED_STANDARDS:
    setup_standard_middleware(app)
else:
    # Fallback middleware setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add Prometheus metrics
app.add_middleware(PrometheusMiddleware, app_name="rag_api")
app.add_route("/metrics", handle_metrics)

# Apply legacy CORS if available
if HAS_LEGACY_CORS:
    try:
        apply_cors(app)
    except Exception as e:
        logger.warning(f"Failed to apply legacy CORS: {e}")

# Include routers
app.include_router(core_router, prefix="")  # Core endpoints at root
app.include_router(rag_router, prefix="")  # RAG endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.get("/law/retrieve", tags=["Legacy"], deprecated=True)
async def legacy_law_retrieve():
    """Legacy law retrieval endpoint. Use /v1/documents/search instead."""
    logger.warning("Legacy /law/retrieve endpoint used. Use /v1/documents/search")
    return {"error": "Legacy endpoint deprecated. Use /v1/documents/search"}

@app.get("/law/knn", tags=["Legacy"], deprecated=True)
async def legacy_law_knn():
    """Legacy KNN search endpoint. Use /v1/documents/knn instead."""
    logger.warning("Legacy /law/knn endpoint used. Use /v1/documents/knn")
    return {"error": "Legacy endpoint deprecated. Use /v1/documents/knn"}

@app.post("/law/knn_vector", tags=["Legacy"], deprecated=True)
async def legacy_knn_vector():
    """Legacy KNN vector search endpoint. Use /v1/documents/knn/vector instead."""
    logger.warning("Legacy /law/knn_vector endpoint used. Use /v1/documents/knn/vector")
    return {"error": "Legacy endpoint deprecated. Use /v1/documents/knn/vector"}

@app.post("/law/hybrid", tags=["Legacy"], deprecated=True)
async def legacy_hybrid():
    """Legacy hybrid search endpoint. Use /v1/documents/hybrid instead."""
    logger.warning("Legacy /law/hybrid endpoint used. Use /v1/documents/hybrid")
    return {"error": "Legacy endpoint deprecated. Use /v1/documents/hybrid"}

@app.get("/law/context", tags=["Legacy"], deprecated=True)
async def legacy_context():
    """Legacy context search endpoint. Use /v1/entities/{entity}/context instead."""
    logger.warning("Legacy /law/context endpoint used. Use /v1/entities/{entity}/context")
    return {"error": "Legacy endpoint deprecated. Use /v1/entities/{entity}/context"}

@app.post("/law/index", tags=["Legacy"], deprecated=True)
async def legacy_index():
    """Legacy indexing endpoint. Use /v1/documents instead."""
    logger.warning("Legacy /law/index endpoint used. Use /v1/documents")
    return {"error": "Legacy endpoint deprecated. Use /v1/documents"}

@app.post("/graph/law/upsert", tags=["Legacy"], deprecated=True)
async def legacy_graph_upsert():
    """Legacy graph upsert endpoint. Use /v1/graph/documents instead."""
    logger.warning("Legacy /graph/law/upsert endpoint used. Use /v1/graph/documents")
    return {"error": "Legacy endpoint deprecated. Use /v1/graph/documents"}

@app.post("/events/extract", tags=["Legacy"], deprecated=True)
async def legacy_events():
    """Legacy event extraction endpoint. Use /v1/events/extract instead."""
    logger.warning("Legacy /events/extract endpoint used. Use /v1/events/extract")
    return {"error": "Legacy endpoint deprecated. Use /v1/events/extract"}

@app.post("/feedback/label", tags=["Legacy"], deprecated=True)
async def legacy_feedback():
    """Legacy feedback endpoint. Use /v1/feedback instead."""
    logger.warning("Legacy /feedback/label endpoint used. Use /v1/feedback")
    return {"error": "Legacy endpoint deprecated. Use /v1/feedback"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    return {
        "service": "rag-api",
        "version": "v1",
        "status": "operational",
        "description": "Legal document retrieval and graph-based search with hybrid AI",
        "capabilities": [
            "Text search with BM25",
            "Vector search with embeddings",
            "Hybrid search combining BM25 + KNN",
            "Graph-based context search",
            "Document indexing",
            "Event extraction",
            "Feedback collection",
            "Real-time reranking"
        ],
        "search_engines": ["OpenSearch", "Neo4j"],
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz", 
            "info": "/info",
            "api_docs": "/docs",
            "metrics": "/metrics",
            "v1_api": "/v1/*"
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Service startup initialization."""
    logger.info("RAG API service v1 starting up...")
    
    # Check dependencies
    try:
        import structlog
        logger.info("Structured logging available")
    except ImportError:
        logger.warning("Structlog not available, using standard logging")
    
    # Check OpenSearch connection
    try:
        from app.opensearch_client import OSClient
        import os
        os_url = os.getenv("OS_URL", "http://opensearch:9200")
        os_index = os.getenv("RAG_OS_INDEX", "laws")
        os_client = OSClient(os_url, os_index)
        # Test connection on startup
        logger.info(f"OpenSearch configured: {os_url}, index: {os_index}")
    except Exception as e:
        logger.error(f"OpenSearch configuration issue: {e}")
    
    # Check Neo4j connection
    try:
        from app.neo4j_client import Neo4jClient
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4j")
        neo_client = Neo4jClient(neo4j_uri, neo4j_user, neo4j_password)
        logger.info(f"Neo4j configured: {neo4j_uri}")
    except Exception as e:
        logger.error(f"Neo4j configuration issue: {e}")
    
    logger.info("RAG API service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("RAG API service v1 shutting down...")
    logger.info("RAG API service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
