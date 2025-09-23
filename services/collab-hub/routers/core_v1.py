"""
Core v1 router for collab-hub service.
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
        # Check file system access for task storage
        tasks_path = os.getenv("CH_TASKS_PATH", "/data/collab_tasks.json")
        try:
            os.makedirs(os.path.dirname(tasks_path), exist_ok=True)
            # Try to write a test file
            test_file = os.path.join(os.path.dirname(tasks_path), ".write_test")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            checks["file_system_writable"] = True
        except Exception as e:
            checks["file_system_writable"] = False
            checks["file_system_error"] = str(e)
        
        # Check WebSocket support
        try:
            from fastapi import WebSocket
            checks["websocket_support"] = True
        except ImportError:
            checks["websocket_support"] = False
        
        # Check JSON serialization support
        try:
            import json
            test_data = {"test": "data", "timestamp": "2025-01-01T00:00:00Z"}
            json.dumps(test_data)
            json.loads(json.dumps(test_data))
            checks["json_support"] = True
        except Exception:
            checks["json_support"] = False
        
        # Check audit log directory
        audit_path = os.getenv("CH_AUDIT_PATH", "/data/collab_audit.jsonl")
        try:
            os.makedirs(os.path.dirname(audit_path), exist_ok=True)
            checks["audit_directory_accessible"] = True
        except Exception as e:
            checks["audit_directory_accessible"] = False
            checks["audit_error"] = str(e)
        
        # Overall readiness check
        critical_checks = [
            checks.get("file_system_writable", False),
            checks.get("websocket_support", False),
            checks.get("json_support", False)
        ]
        
        all_ready = all(critical_checks)
        
        return {
            "ready": all_ready,
            "checks": checks
        }
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "collab-hub",
        "version": "v1",
        "description": "Collaborative workspace and team coordination hub for InfoTerminal",
        "capabilities": [
            "Task and project management",
            "Real-time team collaboration",
            "File sharing and document management",
            "Team workspaces and channels",
            "Comments and discussions",
            "User presence and notifications",
            "Activity feeds and audit logs",
            "Role-based permissions"
        ],
        "collaboration_features": [
            "Kanban-style task boards",
            "Real-time updates via WebSocket",
            "Team workspaces with channels",
            "File upload and sharing",
            "Comment threads and discussions",
            "User mentions and notifications",
            "Activity timeline tracking",
            "Team member presence indicators"
        ],
        "task_management": [
            "Task creation, editing, and deletion",
            "Status tracking (todo, in-progress, done, archived)",
            "Priority levels (low, normal, high, critical)",
            "Label and tag system",
            "Due dates and time tracking",
            "Task assignments and ownership",
            "Subtasks and dependencies",
            "Bulk operations and filtering"
        ],
        "real_time_features": [
            "Live task updates",
            "User presence indicators",
            "Typing indicators in comments",
            "Real-time notifications",
            "Collaborative cursors",
            "Live activity feed"
        ],
        "integrations": [
            "WebSocket manager integration",
            "File storage backend",
            "Notification service",
            "User authentication",
            "Audit logging system"
        ],
        "build": "latest",
        "git": "main"
    }
