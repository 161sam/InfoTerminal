"""
InfoTerminal Flowise Connector - Standardized v1 API

AI Agent workflow orchestration service with standardized InfoTerminal API patterns.
Provides agent chat, tool execution, and workflow management capabilities.
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata
)

from .routers import core_router, agents_router
from .app.it_logging import setup_logging

# Service Configuration
SERVICE_NAME = "flowise-connector"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "AI Agent workflow orchestration for OSINT operations"

# Tag metadata for OpenAPI documentation
TAGS_METADATA = [
    {
        "name": "Core",
        "description": "Health checks and service information"
    },
    {
        "name": "Agents",
        "description": "AI agent chat and workflow orchestration"
    },
    {
        "name": "Tools",
        "description": "Direct tool execution and management"
    },
    {
        "name": "Conversations",
        "description": "Conversation history and management"
    },
    {
        "name": "Legacy",
        "description": "Deprecated endpoints for backward compatibility"
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    print(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    # Initialize any required connections or resources
    # For example: database connections, ML model loading, etc.
    
    yield
    
    # Shutdown
    print(f"Shutting down {SERVICE_NAME}")
    
    # Cleanup resources
    # For example: close database connections, save state, etc.


# FastAPI application with standardized configuration
app = FastAPI(
    title=f"InfoTerminal {SERVICE_NAME.title().replace('-', ' ')} API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=TAGS_METADATA
)

# Set up logging
setup_logging(app, SERVICE_NAME)

# Apply standard middleware and exception handlers
setup_standard_middleware(app, SERVICE_NAME)
setup_standard_exception_handlers(app)

# Set up standard OpenAPI documentation
setup_standard_openapi(
    app=app,
    title=f"InfoTerminal {SERVICE_NAME.title().replace('-', ' ')} API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    service_name=SERVICE_NAME,
    tags_metadata=TAGS_METADATA
)

# Include routers
app.include_router(
    core_router,
    tags=["Core"]
)

app.include_router(
    agents_router,
    prefix="/v1/agents",
    tags=["Agents"]
)

# ===== LEGACY ENDPOINTS (DEPRECATED) =====
# Keep legacy endpoints for backward compatibility with deprecation warnings

@app.get("/healthz", deprecated=True, tags=["Legacy"])
async def legacy_healthz():
    """
    DEPRECATED: Use core health endpoint instead.
    Legacy health endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"status": "healthy", "message": "Use standardized health endpoint"},
        headers={"X-Deprecated": "Use /healthz from core router"}
    )


@app.get("/readyz", deprecated=True, tags=["Legacy"])
async def legacy_readyz():
    """
    DEPRECATED: Use core readiness endpoint instead.
    Legacy readiness endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"status": "ready", "message": "Use standardized readiness endpoint"},
        headers={"X-Deprecated": "Use /readyz from core router"}
    )


@app.get("/tools", deprecated=True, tags=["Legacy"])
async def legacy_tools():
    """
    DEPRECATED: Use /v1/agents/tools instead.
    Legacy tools endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"message": "Use /v1/agents/tools instead"},
        headers={"X-Deprecated": "Use /v1/agents/tools"}
    )


@app.post("/tools/execute", deprecated=True, tags=["Legacy"])
async def legacy_tools_execute():
    """
    DEPRECATED: Use /v1/agents/execute instead.
    Legacy tool execution endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"message": "Use /v1/agents/execute instead"},
        headers={"X-Deprecated": "Use /v1/agents/execute"}
    )


@app.post("/chat", deprecated=True, tags=["Legacy"])
async def legacy_chat():
    """
    DEPRECATED: Use /v1/agents/chat instead.
    Legacy chat endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"message": "Use /v1/agents/chat instead"},
        headers={"X-Deprecated": "Use /v1/agents/chat"}
    )


@app.get("/workflows", deprecated=True, tags=["Legacy"])
async def legacy_workflows():
    """
    DEPRECATED: Use /v1/agents/workflows instead.
    Legacy workflows endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"message": "Use /v1/agents/workflows instead"},
        headers={"X-Deprecated": "Use /v1/agents/workflows"}
    )


@app.get("/conversations/{conversation_id}/history", deprecated=True, tags=["Legacy"])
async def legacy_conversation_history(conversation_id: str):
    """
    DEPRECATED: Use /v1/agents/conversations/{conversation_id} instead.
    Legacy conversation history endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"message": f"Use /v1/agents/conversations/{conversation_id} instead"},
        headers={"X-Deprecated": f"Use /v1/agents/conversations/{conversation_id}"}
    )


@app.delete("/conversations/{conversation_id}", deprecated=True, tags=["Legacy"])
async def legacy_delete_conversation(conversation_id: str):
    """
    DEPRECATED: Use /v1/agents/conversations/{conversation_id} instead.
    Legacy conversation deletion endpoint for backward compatibility.
    """
    return JSONResponse(
        content={"message": f"Use /v1/agents/conversations/{conversation_id} instead"},
        headers={"X-Deprecated": f"Use /v1/agents/conversations/{conversation_id}"}
    )


# Root endpoint
@app.get("/", tags=["Core"])
async def root():
    """
    Service information and available endpoints.
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "api_version": "v1",
        "status": "running",
        "endpoints": {
            "health": "/healthz",
            "readiness": "/readyz",
            "info": "/info",
            "agents": "/v1/agents",
            "documentation": "/docs",
            "openapi_spec": "/openapi.json"
        },
        "capabilities": [
            "agent_orchestration",
            "tool_execution", 
            "conversation_management",
            "workflow_automation",
            "multi_agent_types",
            "error_envelope",
            "pagination",
            "openapi_documentation"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    # Port configuration from environment or default
    port = int(os.getenv("PORT", os.getenv("IT_PORT_FLOWISE_CONNECTOR", "8417")))
    
    uvicorn.run(
        "app_v1:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
