"""
Collaboration Hub Service Models

Comprehensive Pydantic models for collaborative workspace management.
Includes models for tasks, workspaces, teams, comments, files, and real-time collaboration.
"""

from .requests import (
    # Enums
    TaskStatus,
    TaskPriority,
    WorkspaceRole,
    ActivityType,
    NotificationType,
    
    # Core models
    Task,
    Comment,
    Workspace,
    Channel,
    FileUpload,
    Activity,
    Notification,
    
    # Request/Response models
    TaskCreate,
    TaskUpdate,
    TaskMove,
    CommentCreate,
    CommentUpdate,
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceMember,
    WorkspaceInvite,
    ChannelCreate,
    NotificationUpdate,
    
    # Filtering and search
    TaskFilter,
    TaskBulkOperation,
    TaskBulkResult,
    
    # Statistics and monitoring
    CollabStats,
    WorkspaceStats,
    UserPresence,
    HealthStatus,
    
    # Real-time communication
    WebSocketMessage,
)

__all__ = [
    # Enums
    "TaskStatus",
    "TaskPriority", 
    "WorkspaceRole",
    "ActivityType",
    "NotificationType",
    
    # Core models
    "Task",
    "Comment",
    "Workspace",
    "Channel",
    "FileUpload",
    "Activity",
    "Notification",
    
    # Create/Update requests
    "TaskCreate",
    "TaskUpdate",
    "TaskMove",
    "CommentCreate",
    "CommentUpdate",
    "WorkspaceCreate",
    "WorkspaceUpdate",
    "WorkspaceMember",
    "WorkspaceInvite",
    "ChannelCreate",
    "NotificationUpdate",
    
    # Operations
    "TaskFilter",
    "TaskBulkOperation",
    "TaskBulkResult",
    
    # Statistics
    "CollabStats",
    "WorkspaceStats",
    "UserPresence",
    "HealthStatus",
    
    # Real-time
    "WebSocketMessage",
]
