"""
Forensics Service v1 - Chain of Custody for Digital Evidence

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Audit logging
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
from routers.forensics_v1 import router as forensics_router

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
    title="Forensics Service",
    description="Digital evidence chain of custody service with immutable ledger",
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
app.add_middleware(PrometheusMiddleware, app_name="forensics")
app.add_route("/metrics", handle_metrics)

# Apply legacy CORS if available
if HAS_LEGACY_CORS:
    try:
        apply_cors(app)
    except Exception as e:
        logger.warning(f"Failed to apply legacy CORS: {e}")

# Include routers
app.include_router(core_router, prefix="")  # Core endpoints at root
app.include_router(forensics_router, prefix="")  # Forensics endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.post("/ingest", tags=["Legacy"], deprecated=True)
async def legacy_ingest():
    """Legacy ingest endpoint. Use /v1/evidence/ingest instead."""
    logger.warning("Legacy /ingest endpoint used. Use /v1/evidence/ingest")
    return {"error": "Legacy endpoint deprecated. Use /v1/evidence/ingest"}

@app.post("/verify", tags=["Legacy"], deprecated=True)
async def legacy_verify():
    """Legacy verify endpoint. Use /v1/evidence/verify instead."""
    logger.warning("Legacy /verify endpoint used. Use /v1/evidence/verify")
    return {"error": "Legacy endpoint deprecated. Use /v1/evidence/verify"}

@app.get("/receipt/{sha256}", tags=["Legacy"], deprecated=True)
async def legacy_receipt(sha256: str):
    """Legacy receipt endpoint. Use /v1/evidence/{sha256}/receipt instead."""
    logger.warning(f"Legacy /receipt/{sha256} endpoint used. Use /v1/evidence/{sha256}/receipt")
    return {"error": "Legacy endpoint deprecated. Use /v1/evidence/{sha256}/receipt"}

@app.get("/chain/report", tags=["Legacy"], deprecated=True)
async def legacy_chain_report():
    """Legacy chain report endpoint. Use /v1/chain/report instead."""
    logger.warning("Legacy /chain/report endpoint used. Use /v1/chain/report")
    return {"error": "Legacy endpoint deprecated. Use /v1/chain/report"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    return {
        "service": "forensics",
        "version": "v1",
        "status": "operational",
        "description": "Digital evidence chain of custody service",
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
    logger.info("Forensics service v1 starting up...")
    
    # Ensure ledger directory exists
    import os
    ledger_path = os.getenv("FORENSICS_LEDGER", "/data/forensics_ledger.jsonl")
    ledger_dir = os.path.dirname(ledger_path)
    os.makedirs(ledger_dir, exist_ok=True)
    
    logger.info(f"Forensics ledger initialized at: {ledger_path}")
    logger.info("Forensics service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("Forensics service v1 shutting down...")
    logger.info("Forensics service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
