"""
Federation Proxy Service v1 - Distributed InfoTerminal Federation Platform.

Migration to standardized *_v1.py pattern with:
- /v1 namespace for all endpoints
- Standard error envelope and pagination
- Health/Ready endpoints with dependency checks
- OpenAPI documentation with comprehensive schemas
- Shared middleware integration
- Backward compatibility with legacy endpoints
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import shared standards
from _shared.api_standards.middleware import setup_standard_middleware
from _shared.api_standards.error_schemas import StandardError, ErrorCodes, create_error_response

# Import v1 routers
from routers.core_v1 import router as core_router
from routers.federation_proxy_v1 import router as federation_router

# Import service classes  
from service import FederationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
federation_service: FederationService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    global federation_service
    
    # Startup
    logger.info("Starting federation-proxy service v1...")
    try:
        # Initialize federation service
        federation_service = FederationService()
        await federation_service.initialize()
        
        # Store in app state for access in routers
        app.state.federation_service = federation_service
        
        logger.info("Federation proxy service v1 startup completed successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start federation-proxy service: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down federation-proxy service v1...")
        if federation_service:
            await federation_service.cleanup()
        logger.info("Federation proxy service v1 shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="Federation Proxy Service",
    description="""
    **Distributed InfoTerminal Federation Platform**
    
    This service provides comprehensive federation capabilities for distributed InfoTerminal deployments:
    
    ## Core Features
    - **Multi-Instance Federation** - Connect multiple InfoTerminal deployments across regions
    - **Intelligent Request Routing** - Smart load balancing and failover across federated endpoints
    - **Real-time Health Monitoring** - Continuous endpoint health checks and circuit breakers
    - **Security Policy Enforcement** - mTLS, authentication, and authorization for federation
    - **Service Discovery** - Automatic discovery and capability detection across federation
    - **Configuration Synchronization** - Centralized configuration management and distribution
    
    ## Federation Capabilities
    - **Cross-Regional Deployment** - Geographic distribution with latency optimization
    - **High Availability** - Automatic failover and redundancy across endpoints
    - **Load Balancing** - Multiple strategies including geographic and health-based routing
    - **Circuit Breaker Pattern** - Automatic failure detection and recovery
    - **Connection Pooling** - Efficient connection management and reuse
    - **Request Transformation** - Header manipulation and protocol adaptation
    
    ## Security Features
    - **Mutual TLS (mTLS)** - Certificate-based endpoint authentication
    - **JWT Token Propagation** - Secure token forwarding across federation
    - **IP Allowlisting** - Network-level access control
    - **Rate Limiting** - Per-endpoint request throttling
    - **Audit Logging** - Comprehensive request and security event logging
    - **Policy Enforcement** - Centralized security policy management
    
    ## Monitoring & Observability
    - **Real-time Metrics** - Response times, error rates, and throughput
    - **Federation Topology** - Visual representation of network topology
    - **Performance Analytics** - Load distribution and efficiency metrics
    - **Alert Generation** - Proactive alerting for health and performance issues
    - **SLA Monitoring** - Service level agreement tracking and reporting
    
    ## API Standards
    All endpoints follow InfoTerminal v1 API standards:
    - Standard error envelope with error codes and details
    - Paginated responses for list endpoints
    - Comprehensive OpenAPI documentation
    - Health and readiness probes
    - Structured logging and observability
    """,
    version="1.0.0",
    contact={
        "name": "InfoTerminal Team",
        "url": "https://github.com/InfoTerminal/InfoTerminal",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Core",
            "description": "Health checks, service information, and operational endpoints"
        },
        {
            "name": "Federation Proxy", 
            "description": "Federation management, request proxying, and distributed deployment operations"
        }
    ]
)

# Setup standard middleware (CORS, logging, tracing, etc.)
setup_standard_middleware(app, service_name="federation-proxy")

# Add CORS middleware with appropriate origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3411,http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler with standard error format."""
    logger.error(f"Unhandled exception in federation-proxy: {exc}", exc_info=True)
    
    error_response = create_error_response(
        ErrorCodes.INTERNAL_ERROR,
        "Internal service error",
        {
            "service": "federation-proxy",
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


# Include v1 routers with /v1 prefix
app.include_router(core_router, prefix="/v1")
app.include_router(federation_router, prefix="/v1")


# Legacy compatibility endpoints with deprecation warnings
@app.get("/healthz", deprecated=True, tags=["Legacy"])
async def legacy_health():
    """Legacy health endpoint. Use /v1/healthz instead."""
    logger.warning("DEPRECATED: /healthz endpoint called. Use /v1/healthz instead.")
    return {"status": "healthy", "service": "federation-proxy", "deprecated": True}


@app.get("/remotes", deprecated=True, tags=["Legacy"])
async def legacy_remotes():
    """Legacy remotes endpoint. Use /v1/federation/endpoints instead."""
    logger.warning("DEPRECATED: /remotes endpoint called. Use /v1/federation/endpoints instead.")
    error_response = create_error_response(
        "ENDPOINT_DEPRECATED", 
        "This endpoint is deprecated. Use /v1/federation/endpoints instead.",
        {"new_endpoint": "/v1/federation/endpoints", "documentation": "/docs"}
    )
    return JSONResponse(
        status_code=410,
        content=error_response.dict()
    )


# Root endpoint with service information
@app.get("/", tags=["Service Info"])
async def root():
    """Service information and available endpoints."""
    return {
        "service": "federation-proxy",
        "version": "1.0.0",
        "description": "Distributed InfoTerminal federation platform for multi-instance deployments",
        "api_version": "v1",
        "endpoints": {
            "health": "/v1/healthz",
            "readiness": "/v1/readyz", 
            "info": "/v1/info",
            "federation": "/v1/federation",
            "documentation": "/docs",
            "openapi": "/openapi.json"
        },
        "features": [
            "Multi-instance federation",
            "Intelligent request routing",
            "Real-time health monitoring",
            "Security policy enforcement",
            "Service discovery",
            "Configuration synchronization",
            "Load balancing",
            "Circuit breaker pattern"
        ],
        "deprecation_notice": "Legacy endpoints (/healthz, /remotes) are deprecated. Use /v1/* endpoints."
    }


if __name__ == "__main__":
    import uvicorn
    
    # Configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8621"))
    log_level = os.getenv("LOG_LEVEL", "info")
    
    logger.info(f"Starting federation-proxy service on {host}:{port}")
    
    uvicorn.run(
        "app_v1:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=os.getenv("RELOAD", "false").lower() == "true"
    )
