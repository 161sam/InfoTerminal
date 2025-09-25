"""
Verification Service v1 - Claim Verification and Fact-Checking

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Comprehensive verification capabilities
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
from routers.verification_v1 import router as verification_router

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
    title="Verification Service",
    description="Claim extraction, evidence retrieval, stance classification, and credibility assessment for OSINT fact-checking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup middleware
if HAS_SHARED_STANDARDS:
    setup_standard_middleware(app, service_name="verification")
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
    service_name="verification",
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
app.include_router(verification_router, prefix="")  # Verification endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.post("/verify/extract-claims", tags=["Legacy"], deprecated=True)
async def legacy_extract_claims():
    """Legacy claim extraction endpoint. Use /v1/claims/extract instead."""
    logger.warning("Legacy /verify/extract-claims endpoint used. Use /v1/claims/extract")
    return {"error": "Legacy endpoint deprecated. Use /v1/claims/extract"}

@app.post("/verify/image", tags=["Legacy"], deprecated=True)
async def legacy_verify_image():
    """Legacy image verification endpoint. Use /v1/media/analyze instead."""
    logger.warning("Legacy /verify/image endpoint used. Use /v1/media/analyze")
    return {"error": "Legacy endpoint deprecated. Use /v1/media/analyze"}

@app.post("/verify/image-similarity", tags=["Legacy"], deprecated=True)
async def legacy_image_similarity():
    """Legacy image similarity endpoint. Use /v1/media/compare instead."""
    logger.warning("Legacy /verify/image-similarity endpoint used. Use /v1/media/compare")
    return {"error": "Legacy endpoint deprecated. Use /v1/media/compare"}

@app.get("/verify/stats", tags=["Legacy"], deprecated=True)
async def legacy_stats():
    """Legacy stats endpoint. Use /v1/stats instead."""
    logger.warning("Legacy /verify/stats endpoint used. Use /v1/stats")
    return {"error": "Legacy endpoint deprecated. Use /v1/stats"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    return {
        "service": "verification",
        "version": "v1",
        "status": "operational",
        "description": "Comprehensive fact-checking and verification service for OSINT investigations",
        "capabilities": [
            "Claim extraction from text",
            "Evidence retrieval from multiple sources",
            "Stance classification (support/contradict/neutral)",
            "Source credibility assessment", 
            "Media forensics analysis",
            "Image similarity detection",
            "Batch processing",
            "Complete verification pipeline"
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
    logger.info("Verification service v1 starting up...")
    
    # Check dependencies
    try:
        # Check if ML models can be loaded
        from claim_extractor import ClaimExtractor
        from stance_classifier import StanceClassifier
        from evidence_retrieval import EvidenceRetriever
        logger.info("Verification components loaded successfully")
    except ImportError as e:
        logger.warning(f"Some verification components not available: {e}")
    
    # Check optional dependencies
    import os
    redis_host = os.getenv("VERIFICATION_REDIS_HOST", "redis")
    redis_port = os.getenv("VERIFICATION_REDIS_PORT", "6379")
    
    try:
        import redis
        r = redis.Redis(host=redis_host, port=int(redis_port), socket_timeout=2)
        r.ping()
        logger.info(f"Redis cache available at {redis_host}:{redis_port}")
    except Exception as e:
        logger.warning(f"Redis cache not available: {e}")
    
    # Initialize service instance
    try:
        from service import VerificationService
        # Service will be initialized on first request (lazy loading)
        logger.info("Verification service ready for initialization")
    except ImportError as e:
        logger.error(f"Cannot load VerificationService: {e}")
    
    logger.info("Verification service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("Verification service v1 shutting down...")
    
    # Cleanup service resources
    try:
        from routers.verification_v1 import _verification_service
        if _verification_service:
            # Any cleanup needed for the service instance
            logger.info("Verification service cleaned up")
    except Exception as e:
        logger.warning(f"Error during service cleanup: {e}")
    
    logger.info("Verification service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
