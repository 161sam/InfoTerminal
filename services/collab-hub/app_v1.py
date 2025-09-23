"""
Collaboration Hub Service v1 - Team Workspace and Task Management

Provides comprehensive collaboration features:
- Task and project management with Kanban boards
- Team workspaces with channels and permissions
- Real-time communication and activity feeds
- File sharing and comment discussions
- User presence and notification system
- Activity logging and audit trails
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import core_v1, collab_hub_v1
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
    logger.info("Starting Collaboration Hub Service v1")
    
    try:
        # Ensure data directories exist
        tasks_path = os.getenv("CH_TASKS_PATH", "/data/collab_tasks.json")
        audit_path = os.getenv("CH_AUDIT_PATH", "/data/collab_audit.jsonl")
        
        os.makedirs(os.path.dirname(tasks_path), exist_ok=True)
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        
        logger.info("Data directories initialized")
        
        # Initialize collaboration storage (done in router import)
        logger.info("Collaboration storage initialized")
        
        logger.info("Collaboration Hub Service v1 startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start collaboration hub: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down Collaboration Hub Service v1")
        
        try:
            # Gracefully disconnect all WebSocket connections
            from routers.collab_hub_v1 import storage
            
            for connection_id, websocket in list(storage.connections.items()):
                try:
                    await websocket.close()
                except Exception:
                    pass
            
            storage.connections.clear()
            storage.user_connections.clear()
            
            # Save final state
            storage._save_data()
            
            logger.info("Collaboration state saved and connections closed")
            
        except Exception as e:
            logger.warning(f"Error during shutdown: {e}")


# Create FastAPI app with lifespan management
app = FastAPI(
    title="Collaboration Hub Service",
    description="Team collaboration and workspace management platform for InfoTerminal",
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
app.include_router(collab_hub_v1.router, prefix="/v1", tags=["Collaboration Hub"])

# Legacy redirect endpoints with deprecation warnings
@app.get("/healthz", deprecated=True)
async def legacy_health_check():
    """Legacy endpoint - use /healthz (no prefix) instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /healthz instead.",
            "details": {"new_endpoint": "/healthz"}
        }
    }


@app.get("/tasks", deprecated=True)
async def legacy_list_tasks():
    """Legacy endpoint - use /v1/tasks instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/tasks instead.",
            "details": {"new_endpoint": "/v1/tasks"}
        }
    }


@app.post("/tasks", deprecated=True)
async def legacy_create_task():
    """Legacy endpoint - use /v1/tasks instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/tasks instead.",
            "details": {"new_endpoint": "/v1/tasks"}
        }
    }


@app.post("/tasks/{task_id}/move", deprecated=True)
async def legacy_move_task():
    """Legacy endpoint - use /v1/tasks/{task_id}/move instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/tasks/{task_id}/move instead.",
            "details": {"new_endpoint": "/v1/tasks/{task_id}/move"}
        }
    }


@app.delete("/tasks/{task_id}", deprecated=True)
async def legacy_delete_task():
    """Legacy endpoint - use /v1/tasks/{task_id} instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/tasks/{task_id} instead.",
            "details": {"new_endpoint": "/v1/tasks/{task_id}"}
        }
    }


@app.post("/tasks/{task_id}/update", deprecated=True)
async def legacy_update_task():
    """Legacy endpoint - use /v1/tasks/{task_id} (PUT) instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use PUT /v1/tasks/{task_id} instead.",
            "details": {"new_endpoint": "/v1/tasks/{task_id}", "method": "PUT"}
        }
    }


@app.get("/labels", deprecated=True)
async def legacy_list_labels():
    """Legacy endpoint - use /v1/labels instead"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "This endpoint is deprecated. Use /v1/labels instead.",
            "details": {"new_endpoint": "/v1/labels"}
        }
    }


@app.post("/audit", deprecated=True)
async def legacy_write_audit():
    """Legacy endpoint - activities are now automatically logged"""
    return {
        "error": {
            "code": "DEPRECATED_ENDPOINT",
            "message": "Manual audit logging is deprecated. Activities are automatically tracked.",
            "details": {"alternative": "Activities are automatically logged for all operations"}
        }
    }


@app.websocket("/ws", deprecated=True)
async def legacy_websocket_endpoint():
    """Legacy WebSocket endpoint - use /v1/ws/{connection_id} instead"""
    # Note: WebSocket endpoints can't return JSON responses like HTTP endpoints
    # The client would need to handle this at connection time
    pass


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8084"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting Collaboration Hub Service v1 on {host}:{port}")
    
    uvicorn.run(
        "app_v1:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )
