"""
WebSocket Manager Service v1 - Real-time Communication Hub

Provides comprehensive real-time communication features:
- WebSocket connections with authentication
- Channel-based message broadcasting  
- Investigation room collaboration
- Plugin execution status updates
- Entity discovery notifications
- System alerts and notifications
- Distributed messaging via Redis pub/sub
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import core_v1, websocket_manager_v1
from main import ws_manager
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
    logger.info("Starting WebSocket Manager Service v1")
    
    try:
        # Initialize WebSocket manager
        await ws_manager.initialize_redis()
        logger.info("WebSocket manager initialized successfully")
        
        # Start periodic ping task
        async def ping_task():
            while True:
                await asyncio.sleep(30)  # Ping every 30 seconds
                await ws_manager.ping_clients()
        
        ping_task_handle = asyncio.create_task(ping_task())
        logger.info("Client ping task started")
        
        # Store start time for uptime calculation
        import datetime
        ws_manager._start_time = datetime.datetime.now()
        
        logger.info("WebSocket Manager Service v1 startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start WebSocket manager: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down WebSocket Manager Service v1")
        
        try:
            # Cancel ping task
            if 'ping_task_handle' in locals():
                ping_task_handle.cancel()
                try:
                    await ping_task_handle
                except asyncio.CancelledError:
                    pass
            
            # Disconnect all clients gracefully
            for client_id in list(ws_manager.connections.keys()):
                await ws_manager.disconnect(client_id)
            
            # Close Redis connection
            if ws_manager.redis:
                await ws_manager.redis.close()
                logger.info("Redis connection closed")
                
        except Exception as e:
            logger.warning(f"Error during shutdown: {e}")


# Create FastAPI app with lifespan management
app = FastAPI(
    title="WebSocket Manager Service",
    description="Real-time communication hub for InfoTerminal with WebSocket management, collaboration features, and distributed messaging",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup standard middleware (CORS, logging, metrics)
setup_standard_middleware(app)

# Include routers
app.include_router(core_v1.router, prefix="", tags=["Core"])
app.include_router(websocket_manager_v1.router, prefix="/v1", tags=["WebSocket Management"])

# Legacy redirect endpoints with deprecation warnings
@app.websocket("/ws/{client_id}", deprecated=True)
async def legacy_websocket_endpoint():
    """Legacy WebSocket endpoint - use /v1/ws/{client_id} instead"""
    # Note: WebSocket endpoints can't return JSON responses like HTTP endpoints
    # The client would need to handle this at connection time
    pass


@app.post("/broadcast", deprecated=True)
async def legacy_broadcast_message():
    """Legacy endpoint - use /v1/broadcast instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/broadcast instead.",
            "details": {"new_endpoint": "/v1/broadcast"}
        }
    }


@app.post("/broadcast/plugin-status", deprecated=True)
async def legacy_broadcast_plugin_status():
    """Legacy endpoint - use /v1/broadcast/plugin-status instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/broadcast/plugin-status instead.",
            "details": {"new_endpoint": "/v1/broadcast/plugin-status"}
        }
    }


@app.post("/broadcast/entity-discovered", deprecated=True)
async def legacy_broadcast_entity_discovered():
    """Legacy endpoint - use /v1/broadcast/entity-discovered instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/broadcast/entity-discovered instead.",
            "details": {"new_endpoint": "/v1/broadcast/entity-discovered"}
        }
    }


@app.post("/broadcast/system-alert", deprecated=True)
async def legacy_broadcast_system_alert():
    """Legacy endpoint - use /v1/broadcast/system-alert instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/broadcast/system-alert instead.",
            "details": {"new_endpoint": "/v1/broadcast/system-alert"}
        }
    }


@app.get("/stats", deprecated=True)
async def legacy_get_websocket_stats():
    """Legacy endpoint - use /v1/stats instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/stats instead.",
            "details": {"new_endpoint": "/v1/stats"}
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
    
    port = int(os.getenv("PORT", "8083"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting WebSocket Manager Service v1 on {host}:{port}")
    
    uvicorn.run(
        "app_v1:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )
