"""
Cache Manager Service v1 - Multi-Level Intelligent Caching

Provides sophisticated caching with:
- Multi-level caching (L1 memory, L2 Redis, L3 database)
- Intelligent compression and cache placement
- Cache warming and pattern-based invalidation
- Performance analytics and optimization recommendations
- Automatic API response caching middleware
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import core_v1, cache_manager_v1
from main import cache_manager, CacheMiddleware
from _shared.api_standards.middleware import setup_standard_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events"""
    # Startup
    logger.info("Starting Cache Manager Service v1")
    
    try:
        # Initialize cache manager
        await cache_manager.initialize()
        logger.info("Cache manager initialized successfully")
        
        # Start cache warming in background
        if os.getenv("CACHE_WARMING_ENABLED", "true").lower() == "true":
            asyncio.create_task(cache_manager.warm_cache())
            logger.info("Cache warming initiated")
        
        logger.info("Cache Manager Service v1 startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start cache manager: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down Cache Manager Service v1")
        
        try:
            # Clean shutdown of cache connections
            if cache_manager.redis:
                await cache_manager.redis.close()
                logger.info("Redis connection closed")
        except Exception as e:
            logger.warning(f"Error during shutdown: {e}")


# Create FastAPI app with lifespan management
app = FastAPI(
    title="Cache Manager Service",
    description="Multi-level intelligent caching service with compression, warming, and automatic invalidation",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup standard middleware (CORS, logging, metrics)
setup_standard_middleware(app)

# Add intelligent caching middleware
if os.getenv("CACHE_MIDDLEWARE_ENABLED", "true").lower() == "true":
    app.add_middleware(CacheMiddleware, cache_manager=cache_manager)
    logger.info("Cache middleware enabled")

# Include routers
app.include_router(core_v1.router, prefix="", tags=["Core"])
app.include_router(cache_manager_v1.router, prefix="/v1", tags=["Cache Management"])

# Legacy redirect endpoints with deprecation warnings
@app.post("/cache", deprecated=True)
async def legacy_set_cache_item():
    """Legacy endpoint - use /v1/cache instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/cache instead.",
            "details": {"new_endpoint": "/v1/cache"}
        }
    }


@app.get("/cache/{key}", deprecated=True)
async def legacy_get_cache_item():
    """Legacy endpoint - use /v1/cache/{key} instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT", 
            "message": "This endpoint is deprecated. Use /v1/cache/{key} instead.",
            "details": {"new_endpoint": "/v1/cache/{key}"}
        }
    }


@app.delete("/cache/{key}", deprecated=True)
async def legacy_delete_cache_item():
    """Legacy endpoint - use /v1/cache/{key} instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/cache/{key} instead.", 
            "details": {"new_endpoint": "/v1/cache/{key}"}
        }
    }


@app.post("/cache/invalidate", deprecated=True)
async def legacy_invalidate_cache():
    """Legacy endpoint - use /v1/cache/invalidate instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/cache/invalidate instead.",
            "details": {"new_endpoint": "/v1/cache/invalidate"}
        }
    }


@app.post("/cache/warm", deprecated=True)  
async def legacy_warm_cache():
    """Legacy endpoint - use /v1/cache/warm instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/cache/warm instead.",
            "details": {"new_endpoint": "/v1/cache/warm"}
        }
    }


@app.get("/cache/stats", deprecated=True)
async def legacy_get_cache_stats():
    """Legacy endpoint - use /v1/cache/stats instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/cache/stats instead.",
            "details": {"new_endpoint": "/v1/cache/stats"}
        }
    }


@app.get("/health", deprecated=True)
async def legacy_health_check():
    """Legacy endpoint - use /healthz instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /healthz instead.",
            "details": {"new_endpoint": "/healthz"}
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8082"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting Cache Manager Service v1 on {host}:{port}")
    
    uvicorn.run(
        "app_v1:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )
