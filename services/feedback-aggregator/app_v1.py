"""
Feedback Aggregator Service v1 - User Feedback Collection and Analysis Platform.

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
from routers.feedback_aggregator_v1 import router as feedback_router

# Import service classes  
from service import FeedbackService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
feedback_service: FeedbackService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    global feedback_service
    
    # Startup
    logger.info("Starting feedback-aggregator service v1...")
    try:
        # Initialize feedback service
        feedback_service = FeedbackService()
        await feedback_service.initialize()
        
        # Store in app state for access in routers
        app.state.feedback_service = feedback_service
        
        logger.info("Feedback aggregator service v1 startup completed successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start feedback-aggregator service: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down feedback-aggregator service v1...")
        if feedback_service:
            await feedback_service.cleanup()
        logger.info("Feedback aggregator service v1 shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="Feedback Aggregator Service",
    description="""
    **User Feedback Collection and Analysis Platform for InfoTerminal**
    
    This service provides comprehensive feedback management capabilities including:
    
    ## Core Features
    - **Intelligent Feedback Collection** - Structured feedback forms with automated analysis
    - **Sentiment & Urgency Detection** - AI-powered content analysis for prioritization
    - **Voting & Community Prioritization** - User voting system for feedback importance
    - **GitHub Integration** - Automated issue creation and ticket tracking
    - **Analytics & Reporting** - Comprehensive statistics and trend analysis
    - **Team Productivity Metrics** - Performance monitoring and optimization insights
    
    ## Analysis Capabilities
    - Automated sentiment analysis (positive/negative/neutral)
    - Urgency detection based on keyword patterns
    - Priority suggestions based on feedback type and content
    - Tag extraction and categorization
    - Development effort estimation
    - Similar feedback detection and duplicate prevention
    
    ## Integrations
    - **GitHub Issues** - Automated ticket creation with customizable templates
    - **Redis Caching** - Performance optimization for statistics and analytics
    - **PostgreSQL** - Persistent storage with full-text search capabilities
    - **Webhook Support** - External system integrations and notifications
    - **Email Notifications** - Automated alerts and escalation workflows
    
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
            "name": "Feedback Aggregator", 
            "description": "User feedback collection, analysis, and management operations"
        }
    ]
)

# Setup standard middleware (CORS, logging, tracing, etc.)
setup_standard_middleware(app, service_name="feedback-aggregator")

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
    logger.error(f"Unhandled exception in feedback-aggregator: {exc}", exc_info=True)
    
    error_response = create_error_response(
        ErrorCodes.INTERNAL_ERROR,
        "Internal service error",
        {
            "service": "feedback-aggregator",
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
app.include_router(feedback_router, prefix="/v1")


# Legacy compatibility endpoints with deprecation warnings
@app.get("/health", deprecated=True, tags=["Legacy"])
async def legacy_health():
    """Legacy health endpoint. Use /v1/healthz instead."""
    logger.warning("DEPRECATED: /health endpoint called. Use /v1/healthz instead.")
    return {"status": "healthy", "service": "feedback-aggregator", "deprecated": True}


@app.get("/feedback", deprecated=True, tags=["Legacy"])
async def legacy_feedback_list():
    """Legacy feedback list endpoint. Use /v1/feedback instead."""
    logger.warning("DEPRECATED: /feedback endpoint called. Use /v1/feedback instead.")
    error_response = create_error_response(
        "ENDPOINT_DEPRECATED", 
        "This endpoint is deprecated. Use /v1/feedback instead.",
        {"new_endpoint": "/v1/feedback", "documentation": "/docs"}
    )
    return JSONResponse(
        status_code=410,
        content=error_response.dict()
    )


@app.post("/feedback", deprecated=True, tags=["Legacy"])
async def legacy_feedback_create():
    """Legacy feedback creation endpoint. Use /v1/feedback instead."""
    logger.warning("DEPRECATED: POST /feedback endpoint called. Use POST /v1/feedback instead.")
    error_response = create_error_response(
        "ENDPOINT_DEPRECATED",
        "This endpoint is deprecated. Use POST /v1/feedback instead.",
        {"new_endpoint": "POST /v1/feedback", "documentation": "/docs"}
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
        "service": "feedback-aggregator",
        "version": "1.0.0",
        "description": "User feedback collection and analysis platform for InfoTerminal",
        "api_version": "v1",
        "endpoints": {
            "health": "/v1/healthz",
            "readiness": "/v1/readyz", 
            "info": "/v1/info",
            "feedback": "/v1/feedback",
            "documentation": "/docs",
            "openapi": "/openapi.json"
        },
        "features": [
            "Intelligent feedback analysis",
            "GitHub integration",
            "Community voting",
            "Real-time analytics",
            "Team productivity metrics",
            "Automated prioritization"
        ],
        "deprecation_notice": "Legacy endpoints (/health, /feedback) are deprecated. Use /v1/* endpoints."
    }


if __name__ == "__main__":
    import uvicorn
    
    # Configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8620"))
    log_level = os.getenv("LOG_LEVEL", "info")
    
    logger.info(f"Starting feedback-aggregator service on {host}:{port}")
    
    uvicorn.run(
        "app_v1:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=os.getenv("RELOAD", "false").lower() == "true"
    )
