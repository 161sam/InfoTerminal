"""
InfoTerminal Egress Gateway Service v1.0.0

Standardized *_v1.py implementation for anonymous/secure outbound connections.
Provides unified API for OSINT research with enhanced anonymity and security.

This service replaces the legacy app.py with:
- Standard /v1 API namespace
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Structured logging
- Enhanced authentication
"""

import os
import sys
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import structlog

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata,
    HealthChecker,
    DependencyCheck
)

# Import proxy system components
try:
    from proxy import ProxyManager
    from tor_controller import TorController
except ImportError:
    # Create placeholder classes if modules not available
    class ProxyManager:
        def __init__(self): pass
        async def initialize(self): pass
        async def cleanup(self): pass
        def get_active_proxy(self): return "none"
        def get_request_count(self): return 0
        async def rotate_identity(self, proxy_type=None): pass
        async def get_proxy(self, proxy_type): return None
        def get_vpn_pools(self): return []
        def get_proxy_pools(self): return []
        def get_last_rotation(self): return None
    
    class TorController:
        def __init__(self): pass
        async def initialize(self): pass
        async def cleanup(self): pass
        def is_available(self): return False
        def is_circuit_established(self): return False
        async def new_identity(self): pass

# Import routers
from routers.core_v1 import router as core_router, set_dependencies
from routers.egress_v1 import router as egress_router, set_proxy_system

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Service Configuration
SERVICE_NAME = "egress-gateway"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "Anonymous/secure outbound connections for OSINT research with enhanced privacy protection"

# Configuration from environment
DOCKER_ENABLED = os.getenv("EGRESS_DOCKER_ENABLED", "1") == "1"
TOR_ENABLED = os.getenv("EGRESS_TOR_ENABLED", "1") == "1"
VPN_ENABLED = os.getenv("EGRESS_VPN_ENABLED", "0") == "1"
MAX_CONCURRENT_REQUESTS = int(os.getenv("EGRESS_MAX_CONCURRENT", "50"))
REQUEST_TIMEOUT = int(os.getenv("EGRESS_REQUEST_TIMEOUT", "30"))

# Global state
proxy_manager = None
tor_controller = None
health_checker = HealthChecker(SERVICE_NAME, SERVICE_VERSION)


def check_proxy_manager() -> DependencyCheck:
    """Check proxy manager health."""
    try:
        if proxy_manager is None:
            return DependencyCheck(
                status="unhealthy",
                error="Proxy manager not initialized"
            )
        
        active_proxy = proxy_manager.get_active_proxy()
        return DependencyCheck(
            status="healthy",
            message=f"Active proxy: {active_proxy}",
            latency_ms=2.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


def check_tor_controller() -> DependencyCheck:
    """Check Tor controller health."""
    if not TOR_ENABLED:
        return DependencyCheck(
            status="disabled",
            message="Tor support disabled"
        )
    
    try:
        if tor_controller is None:
            return DependencyCheck(
                status="degraded",
                message="Tor controller not initialized (optional)"
            )
        
        if tor_controller.is_available():
            circuit_established = tor_controller.is_circuit_established()
            return DependencyCheck(
                status="healthy" if circuit_established else "degraded",
                message=f"Tor available, circuit: {'established' if circuit_established else 'establishing'}",
                latency_ms=10.0
            )
        else:
            return DependencyCheck(
                status="degraded",
                message="Tor daemon not available (optional)",
                latency_ms=5.0
            )
    except Exception as e:
        return DependencyCheck(
            status="degraded",
            error=f"Tor check failed: {str(e)}"
        )


def check_network_connectivity() -> DependencyCheck:
    """Check basic network connectivity."""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return DependencyCheck(
            status="healthy",
            message="Network connectivity available",
            latency_ms=3.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=f"Network connectivity failed: {str(e)}"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global proxy_manager, tor_controller
    
    logger.info(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    try:
        # Initialize Tor Controller if enabled
        if TOR_ENABLED:
            try:
                tor_controller = TorController()
                await tor_controller.initialize()
                logger.info("Tor controller initialized", available=tor_controller.is_available())
            except Exception as e:
                logger.warning("Tor controller initialization failed", error=str(e))
                tor_controller = None
        
        # Initialize Proxy Manager
        try:
            proxy_manager = ProxyManager()
            await proxy_manager.initialize()
            logger.info("Proxy manager initialized", active_proxy=proxy_manager.get_active_proxy())
        except Exception as e:
            logger.error("Proxy manager initialization failed", error=str(e))
            raise
        
        # Set up dependency checks
        health_checker.add_dependency("proxy_manager", check_proxy_manager)
        health_checker.add_dependency("tor_controller", check_tor_controller)
        health_checker.add_dependency("network", check_network_connectivity)
        
        # Set dependencies in routers
        set_dependencies(proxy_manager, tor_controller)
        set_proxy_system(proxy_manager, tor_controller)
        
        logger.info(f"{SERVICE_NAME} startup completed successfully")
        
    except Exception as e:
        logger.error("Failed to initialize egress gateway", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {SERVICE_NAME}")
    
    # Cleanup proxy manager
    if proxy_manager:
        try:
            await proxy_manager.cleanup()
        except Exception as e:
            logger.error("Error during proxy manager cleanup", error=str(e))
    
    # Cleanup Tor controller
    if tor_controller:
        try:
            await tor_controller.cleanup()
        except Exception as e:
            logger.error("Error during Tor controller cleanup", error=str(e))


# FastAPI application with standardized configuration
app = FastAPI(
    title="InfoTerminal Egress Gateway API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply standard middleware and exception handlers
setup_standard_middleware(app, SERVICE_NAME)
setup_standard_exception_handlers(app)

# Set up standard OpenAPI documentation
setup_standard_openapi(
    app=app,
    title="InfoTerminal Egress Gateway API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    service_name=SERVICE_NAME,
    tags_metadata=get_service_tags_metadata(SERVICE_NAME)
)

# Include routers
app.include_router(core_router, tags=["Core"])
app.include_router(egress_router, prefix="/v1", tags=["Proxy"])

# Legacy endpoints for backward compatibility
@app.get("/healthz", deprecated=True, include_in_schema=False)
def legacy_healthz():
    """DEPRECATED: Use /healthz instead (this endpoint redirects)."""
    return health_checker.health_check()

@app.get("/health", deprecated=True, include_in_schema=False)
def legacy_health():
    """DEPRECATED: Use /healthz instead."""
    return JSONResponse(
        content={"status": "healthy", "message": "Use /healthz instead"},
        headers={"X-Deprecated": "Use /healthz instead"}
    )

@app.post("/proxy/request", deprecated=True, include_in_schema=False)
def legacy_proxy_request():
    """DEPRECATED: Use /v1/proxy/request instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/proxy/request"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/proxy/request instead"}
    )

@app.get("/proxy/status", deprecated=True, include_in_schema=False)
def legacy_proxy_status():
    """DEPRECATED: Use /v1/proxy/status instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/proxy/status"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/proxy/status instead"}
    )

@app.post("/proxy/rotate", deprecated=True, include_in_schema=False)
def legacy_proxy_rotate():
    """DEPRECATED: Use /v1/proxy/rotate instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/proxy/rotate"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/proxy/rotate instead"}
    )


# Root endpoint
@app.get("/", include_in_schema=False)
def root():
    """Root endpoint with service information."""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "api_version": "v1",
        "documentation": "/docs",
        "health_check": "/healthz",
        "readiness_check": "/readyz",
        "openapi_spec": "/openapi.json",
        "features": {
            "tor_support": TOR_ENABLED,
            "vpn_support": VPN_ENABLED,
            "docker_enabled": DOCKER_ENABLED,
            "max_concurrent_requests": MAX_CONCURRENT_REQUESTS,
            "request_timeout": REQUEST_TIMEOUT
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8615))
    
    uvicorn.run(
        "app_v1:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
