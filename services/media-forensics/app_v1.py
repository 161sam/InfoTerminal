"""
Media Forensics Service v1 - Image and Video Analysis for OSINT

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Image forensic analysis capabilities
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
from routers.media_forensics_v1 import router as media_forensics_router

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
    title="Media Forensics Service",
    description="Image and video analysis for OSINT investigations with EXIF extraction, perceptual hashing, and forensic analysis",
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
app.add_middleware(PrometheusMiddleware, app_name="media_forensics")
app.add_route("/metrics", handle_metrics)

# Apply legacy CORS if available
if HAS_LEGACY_CORS:
    try:
        apply_cors(app)
    except Exception as e:
        logger.warning(f"Failed to apply legacy CORS: {e}")

# Include routers
app.include_router(core_router, prefix="")  # Core endpoints at root
app.include_router(media_forensics_router, prefix="")  # Media forensics endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.post("/image/analyze", tags=["Legacy"], deprecated=True)
async def legacy_image_analyze():
    """Legacy image analysis endpoint. Use /v1/images/analyze instead."""
    logger.warning("Legacy /image/analyze endpoint used. Use /v1/images/analyze")
    return {"error": "Legacy endpoint deprecated. Use /v1/images/analyze"}

@app.post("/image/compare", tags=["Legacy"], deprecated=True)
async def legacy_image_compare():
    """Legacy image comparison endpoint. Use /v1/images/compare instead."""
    logger.warning("Legacy /image/compare endpoint used. Use /v1/images/compare")
    return {"error": "Legacy endpoint deprecated. Use /v1/images/compare"}

@app.get("/image/hash/{hash_value}", tags=["Legacy"], deprecated=True)
async def legacy_find_similar(hash_value: str):
    """Legacy similar images endpoint. Use /v1/images/similar/{hash_value} instead."""
    logger.warning(f"Legacy /image/hash/{hash_value} endpoint used. Use /v1/images/similar/{hash_value}")
    return {"error": "Legacy endpoint deprecated. Use /v1/images/similar/{hash_value}"}

@app.get("/formats", tags=["Legacy"], deprecated=True)
async def legacy_formats():
    """Legacy formats endpoint. Use /v1/formats instead."""
    logger.warning("Legacy /formats endpoint used. Use /v1/formats")
    return {"error": "Legacy endpoint deprecated. Use /v1/formats"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    return {
        "service": "media-forensics",
        "version": "v1",
        "status": "operational",
        "description": "Image and video analysis for OSINT investigations",
        "capabilities": [
            "EXIF metadata extraction",
            "Perceptual hashing", 
            "Forensic analysis",
            "Image comparison",
            "Reverse image search",
            "Batch processing"
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
    logger.info("Media Forensics service v1 starting up...")
    
    # Check dependencies
    try:
        from PIL import Image
        import imagehash
        logger.info("Image processing dependencies verified: PIL, imagehash")
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        raise
    
    # Check optional dependencies
    import os
    if os.getenv("REVERSE_SEARCH_ENABLED") == "1":
        if not os.getenv("BING_SEARCH_API_KEY"):
            logger.warning("Reverse search enabled but BING_SEARCH_API_KEY not configured")
        else:
            logger.info("Reverse image search configured and enabled")
    
    logger.info("Media Forensics service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("Media Forensics service v1 shutting down...")
    logger.info("Media Forensics service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
