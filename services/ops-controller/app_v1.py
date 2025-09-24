"""
Ops Controller Service v1 - Service Orchestration and Security Management

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Comprehensive ops management
- Security operations
- Performance monitoring
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
from routers.ops_controller_v1 import router as ops_router, initialize_security_manager

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
    title="Ops Controller Service",
    description="Service orchestration, security management, and performance monitoring for InfoTerminal",
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
    service_name="ops-controller",
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
app.include_router(ops_router, prefix="")  # Ops endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.get("/ops/stacks", tags=["Legacy"], deprecated=True)
async def legacy_ops_stacks():
    """Legacy ops stacks endpoint. Use /v1/stacks instead."""
    logger.warning("Legacy /ops/stacks endpoint used. Use /v1/stacks")
    return {"error": "Legacy endpoint deprecated. Use /v1/stacks"}

@app.get("/ops/stacks/{name}/status", tags=["Legacy"], deprecated=True)
async def legacy_stack_status(name: str):
    """Legacy stack status endpoint. Use /v1/stacks/{name}/status instead."""
    logger.warning(f"Legacy /ops/stacks/{name}/status endpoint used. Use /v1/stacks/{name}/status")
    return {"error": "Legacy endpoint deprecated. Use /v1/stacks/{name}/status"}

@app.post("/ops/stacks/{name}/up", tags=["Legacy"], deprecated=True)
async def legacy_stack_up(name: str):
    """Legacy stack up endpoint. Use /v1/stacks/{name}/up instead."""
    logger.warning(f"Legacy /ops/stacks/{name}/up endpoint used. Use /v1/stacks/{name}/up")
    return {"error": "Legacy endpoint deprecated. Use /v1/stacks/{name}/up"}

@app.post("/ops/stacks/{name}/down", tags=["Legacy"], deprecated=True)
async def legacy_stack_down(name: str):
    """Legacy stack down endpoint. Use /v1/stacks/{name}/down instead."""
    logger.warning(f"Legacy /ops/stacks/{name}/down endpoint used. Use /v1/stacks/{name}/down")
    return {"error": "Legacy endpoint deprecated. Use /v1/stacks/{name}/down"}

@app.post("/ops/stacks/{name}/restart", tags=["Legacy"], deprecated=True)
async def legacy_stack_restart(name: str):
    """Legacy stack restart endpoint. Use /v1/stacks/{name}/restart instead."""
    logger.warning(f"Legacy /ops/stacks/{name}/restart endpoint used. Use /v1/stacks/{name}/restart")
    return {"error": "Legacy endpoint deprecated. Use /v1/stacks/{name}/restart"}

@app.get("/security/incognito/status", tags=["Legacy"], deprecated=True)
async def legacy_incognito_status():
    """Legacy incognito status endpoint. Use /v1/security/incognito/status instead."""
    logger.warning("Legacy /security/incognito/status endpoint used. Use /v1/security/incognito/status")
    return {"error": "Legacy endpoint deprecated. Use /v1/security/incognito/status"}

@app.get("/health/comprehensive", tags=["Legacy"], deprecated=True)
async def legacy_comprehensive_health():
    """Legacy comprehensive health endpoint. Use /v1/health/comprehensive instead."""
    logger.warning("Legacy /health/comprehensive endpoint used. Use /v1/health/comprehensive")
    return {"error": "Legacy endpoint deprecated. Use /v1/health/comprehensive"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    import os
    enabled = os.getenv("IT_OPS_ENABLE", "0") == "1"
    
    return {
        "service": "ops-controller",
        "version": "v1",
        "status": "operational" if enabled else "disabled",
        "description": "Service orchestration, security management, and performance monitoring",
        "enabled": enabled,
        "capabilities": [
            "Docker Compose stack management",
            "Service scaling and orchestration",
            "Security incognito sessions",
            "Data wiping and cleanup",
            "Performance monitoring",
            "Comprehensive health checks",
            "Log streaming",
            "Container operations",
            "Emergency shutdown"
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
    logger.info("Ops Controller service v1 starting up...")
    
    import os
    enabled = os.getenv("IT_OPS_ENABLE", "0") == "1"
    
    if enabled:
        logger.info("Ops Controller is ENABLED")
        
        # Check dependencies
        try:
            import docker
            import yaml
            import psutil
            logger.info("Required dependencies verified: docker, yaml, psutil")
        except ImportError as e:
            logger.error(f"Missing required dependency: {e}")
            raise
        
        # Initialize security manager
        try:
            await initialize_security_manager()
            logger.info("Security manager initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize security manager: {e}")
        
        # Check stacks configuration
        stacks_file = os.getenv("IT_OPS_STACKS_FILE", "infra/ops/stacks.yaml")
        if os.path.exists(stacks_file):
            logger.info(f"Stacks configuration found: {stacks_file}")
        else:
            logger.warning(f"Stacks configuration not found: {stacks_file}")
    else:
        logger.info("Ops Controller is DISABLED (set IT_OPS_ENABLE=1 to enable)")
    
    logger.info("Ops Controller service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("Ops Controller service v1 shutting down...")
    
    # Cleanup security manager
    from routers.ops_controller_v1 import security_manager
    if security_manager:
        try:
            await security_manager.cleanup()
            logger.info("Security manager cleaned up")
        except Exception as e:
            logger.warning(f"Security manager cleanup failed: {e}")
    
    logger.info("Ops Controller service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
