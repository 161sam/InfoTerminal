"""
XAI Service v1 - Explainable AI and Model Interpretability

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Text explanation capabilities
- Model transparency features
"""

import logging
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Add service and repo to path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Import routers
from routers.core_v1 import router as core_router
from routers.xai_v1 import router as xai_router

# Import shared standards
try:
    from _shared.api_standards.middleware import setup_standard_middleware
    from _shared.api_standards.error_schemas import StandardError
    from _shared.obs.metrics_boot import enable_prometheus_metrics
    HAS_SHARED_STANDARDS = True
except ImportError:
    HAS_SHARED_STANDARDS = False
    logging.warning("Shared API standards not available, using fallback")
    def enable_prometheus_metrics(app, **kwargs):
        return None

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
    title="XAI Service",
    description="Explainable AI service for model interpretability, decision transparency, and text explanation",
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

enable_prometheus_metrics(
    app,
    service_name="xai",
    service_version="1.0.0",
)

# Apply legacy CORS if available
if HAS_LEGACY_CORS:
    try:
        apply_cors(app)
    except Exception as e:
        logger.warning(f"Failed to apply legacy CORS: {e}")

# Include routers
app.include_router(core_router, prefix="")  # Core endpoints at root
app.include_router(xai_router, prefix="")  # XAI endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.post("/explain/text", tags=["Legacy"], deprecated=True)
async def legacy_explain_text():
    """Legacy text explanation endpoint. Use /v1/explain/text instead."""
    logger.warning("Legacy /explain/text endpoint used. Use /v1/explain/text")
    return {"error": "Legacy endpoint deprecated. Use /v1/explain/text"}

@app.get("/model-card", tags=["Legacy"], deprecated=True)
async def legacy_model_card():
    """Legacy model card endpoint. Use /v1/model-card instead."""
    logger.warning("Legacy /model-card endpoint used. Use /v1/model-card")
    return {"error": "Legacy endpoint deprecated. Use /v1/model-card"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    return {
        "service": "xai",
        "version": "v1",
        "status": "operational",
        "description": "Explainable AI service for model interpretability and decision transparency",
        "capabilities": [
            "Text explanation with token highlighting",
            "Query-based relevance highlighting", 
            "Multiple explanation methods",
            "Method comparison and analysis",
            "Model transparency reporting",
            "Batch processing",
            "Performance monitoring"
        ],
        "explanation_methods": [
            "heuristic",
            "attention",
            "comparison"
        ],
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
    logger.info("XAI service v1 starting up...")
    
    # Check dependencies
    try:
        import structlog
        logger.info("Structured logging available")
    except ImportError:
        logger.warning("Structlog not available, using standard logging")
    
    # Check optional ML libraries
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
    
    if ml_libraries:
        logger.info(f"Advanced ML libraries available: {', '.join(ml_libraries)}")
    else:
        logger.info("Basic explainability only - no advanced ML libraries detected")
    
    # Initialize service statistics
    from routers.xai_v1 import _stats
    _stats["total_explanations"] = 0
    _stats["explanations_by_method"] = {}
    _stats["processing_times"] = []
    
    logger.info("XAI service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("XAI service v1 shutting down...")
    
    # Log final statistics
    try:
        from routers.xai_v1 import _stats
        logger.info(f"Final statistics: {_stats['total_explanations']} explanations processed")
        if _stats["explanations_by_method"]:
            logger.info(f"Methods used: {_stats['explanations_by_method']}")
    except Exception as e:
        logger.warning(f"Error during statistics logging: {e}")
    
    logger.info("XAI service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
