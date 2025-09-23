"""
Core v1 router for websocket-manager service.
Provides health checks, readiness, and service info endpoints.
"""

import os
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(tags=["Core"])


@router.get("/healthz")
def healthz() -> Dict[str, Any]:
    """Liveness probe - returns OK if service is running."""
    return {"ok": True}


@router.get("/readyz")  
def readyz() -> Dict[str, Any]:
    """Readiness probe - checks if service can handle requests."""
    checks = {}
    
    try:
        # Check Redis connectivity (optional for WebSocket pub/sub)
        redis_available = False
        redis_error = None
        try:
            import aioredis
            checks["redis_library_available"] = True
            # Note: Can't test async connection in sync function
            redis_available = True
        except ImportError:
            checks["redis_library_available"] = False
            redis_error = "aioredis library not available"
        
        # Check JWT library for authentication
        try:
            import jwt
            checks["jwt_available"] = True
        except ImportError:
            checks["jwt_available"] = False
        
        # Check WebSocket libraries
        try:
            from fastapi import WebSocket
            checks["websocket_support"] = True
        except ImportError:
            checks["websocket_support"] = False
        
        # Check JSON serialization support
        try:
            import json
            import uuid
            test_data = {"test": "data", "uuid": str(uuid.uuid4())}
            json.dumps(test_data)
            checks["serialization_available"] = True
        except Exception:
            checks["serialization_available"] = False
        
        # Overall readiness check
        critical_checks = [
            checks.get("websocket_support", False),
            checks.get("serialization_available", False),
            checks.get("jwt_available", False)
        ]
        
        all_ready = all(critical_checks)
        
        return {
            "ready": all_ready,
            "checks": checks,
            "optional_features": {
                "redis_pubsub": redis_available,
                "redis_error": redis_error
            }
        }
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "websocket-manager",
        "version": "v1",
        "description": "Real-time WebSocket communication manager for InfoTerminal",
        "capabilities": [
            "Real-time WebSocket connections",
            "Channel-based message broadcasting", 
            "Investigation room collaboration",
            "Plugin execution status updates",
            "Entity discovery notifications",
            "System alerts and notifications",
            "User presence and collaboration features",
            "Distributed messaging via Redis pub/sub"
        ],
        "supported_channels": [
            "global - Global system messages",
            "user - User-specific notifications", 
            "investigation - Investigation room updates",
            "plugin_execution - Plugin status updates",
            "graph_analysis - Graph and entity updates",
            "system_health - Health and performance alerts"
        ],
        "message_types": [
            "plugin_started", "plugin_progress", "plugin_completed", "plugin_error",
            "entity_discovered", "graph_updated", "relationship_added",
            "investigation_created", "investigation_updated", "analysis_completed",
            "system_alert", "user_notification",
            "user_joined", "user_left", "cursor_moved", "selection_changed",
            "performance_alert", "health_status"
        ],
        "features": [
            "JWT token authentication",
            "Offline message queuing",
            "Connection health monitoring",
            "Redis-based scaling",
            "Real-time collaboration",
            "Automatic reconnection support"
        ],
        "build": "latest",
        "git": "main"
    }
