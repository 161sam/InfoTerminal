"""
Pydantic models for Collaboration Hub Service v1.
"""

from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class WorkspaceRole(str, Enum):
    """User roles within a workspace."""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"
    GUEST = "guest"


class ActivityType(str, Enum):
    """Types of activities for audit logging."""
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_MOVED = "task_moved"
    TASK_ASSIGNED = "task_assigned"
    COMMENT_ADDED = "comment_added"
    COMMENT_UPDATED = "comment_updated"
    COMMENT_DELETED = "comment_deleted"
    FILE_UPLOADED = "file_uploaded"
    FILE_DELETED = "file_deleted"
    WORKSPACE_CREATED = "workspace_created"
    WORKSPACE_UPDATED = "workspace_updated"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    ROLE_CHANGED = "role_changed"


class NotificationType(str, Enum):
    """Notification types."""
    TASK_ASSIGNED = "task_assigned"
    TASK_DUE = "task_due"
    COMMENT_MENTION = "comment_mention"
    FILE_SHARED = "file_shared"
    WORKSPACE_INVITE = "workspace_invite"
    SYSTEM_ALERT = "system_alert"


class Task(BaseModel):
    """Task model with comprehensive properties."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique task identifier")
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description", max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.NORMAL, description="Task priority")
    labels: List[str] = Field(default_factory=list, description="Task labels/tags")
    assigned_to: Optional[str] = Field(None, description="Assigned user ID")
    created_by: str = Field(..., description="Creator user ID")
    workspace_id: str = Field(..., description="Workspace identifier")
    channel_id: Optional[str] = Field(None, description="Channel identifier")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    dependencies: List[str] = Field(default_factory=list, description="Dependent task IDs")
    subtasks: List[str] = Field(default_factory=list, description="Subtask IDs")
    estimated_hours: Optional[float] = Field(None, description="Estimated work hours", ge=0)
    actual_hours: Optional[float] = Field(None, description="Actual work hours", ge=0)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TaskCreate(BaseModel):
    """Request to create a new task."""
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description", max_length=2000)
    priority: TaskPriority = Field(default=TaskPriority.NORMAL, description="Task priority")
    labels: List[str] = Field(default_factory=list, description="Task labels")
    assigned_to: Optional[str] = Field(None, description="User ID to assign task to")
    workspace_id: str = Field(..., description="Workspace identifier")
    channel_id: Optional[str] = Field(None, description="Channel identifier")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    dependencies: List[str] = Field(default_factory=list, description="Dependent task IDs")
    estimated_hours: Optional[float] = Field(None, description="Estimated work hours", ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "priority": "high",
                "labels": ["backend", "security"],
                "workspace_id": "workspace_123",
                "due_date": "2025-10-01T00:00:00Z",
                "estimated_hours": 8.0
            }
        }


class TaskUpdate(BaseModel):
    """Request to update an existing task."""
    title: Optional[str] = Field(None, description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description", max_length=2000)
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")
    labels: Optional[List[str]] = Field(None, description="Task labels")
    assigned_to: Optional[str] = Field(None, description="User ID to assign task to")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    estimated_hours: Optional[float] = Field(None, description="Estimated work hours", ge=0)
    actual_hours: Optional[float] = Field(None, description="Actual work hours", ge=0)


class TaskMove(BaseModel):
    """Request to move task to different status."""
    status: TaskStatus = Field(..., description="New task status")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "in_progress"
            }
        }


class Comment(BaseModel):
    """Comment model for tasks and discussions."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Comment identifier")
    content: str = Field(..., description="Comment content", min_length=1, max_length=2000)
    author_id: str = Field(..., description="Author user ID")
    task_id: Optional[str] = Field(None, description="Associated task ID")
    workspace_id: str = Field(..., description="Workspace identifier")
    channel_id: Optional[str] = Field(None, description="Channel identifier")
    parent_id: Optional[str] = Field(None, description="Parent comment for threading")
    mentions: List[str] = Field(default_factory=list, description="Mentioned user IDs")
    attachments: List[str] = Field(default_factory=list, description="Attached file IDs")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    is_edited: bool = Field(default=False, description="Whether comment was edited")


class CommentCreate(BaseModel):
    """Request to create a new comment."""
    content: str = Field(..., description="Comment content", min_length=1, max_length=2000)
    task_id: Optional[str] = Field(None, description="Associated task ID")
    workspace_id: str = Field(..., description="Workspace identifier")
    channel_id: Optional[str] = Field(None, description="Channel identifier")
    parent_id: Optional[str] = Field(None, description="Parent comment for threading")
    mentions: List[str] = Field(default_factory=list, description="User IDs to mention")
    
    class Config:
        schema_extra = {
            "example": {
                "content": "This looks good to me! @john_doe please review the authentication logic.",
                "task_id": "task_123",
                "workspace_id": "workspace_456",
                "mentions": ["user_john_doe"]
            }
        }


class CommentUpdate(BaseModel):
    """Request to update a comment."""
    content: str = Field(..., description="Updated comment content", min_length=1, max_length=2000)


class Workspace(BaseModel):
    """Workspace model for team collaboration."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Workspace identifier")
    name: str = Field(..., description="Workspace name", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Workspace description", max_length=500)
    owner_id: str = Field(..., description="Workspace owner user ID")
    members: List[str] = Field(default_factory=list, description="Member user IDs")
    channels: List[str] = Field(default_factory=list, description="Channel IDs")
    is_public: bool = Field(default=False, description="Whether workspace is publicly accessible")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Workspace settings")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class WorkspaceCreate(BaseModel):
    """Request to create a new workspace."""
    name: str = Field(..., description="Workspace name", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Workspace description", max_length=500)
    is_public: bool = Field(default=False, description="Whether workspace is publicly accessible")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "InfoTerminal Development",
                "description": "Collaboration space for InfoTerminal development team",
                "is_public": False
            }
        }


class WorkspaceUpdate(BaseModel):
    """Request to update workspace details."""
    name: Optional[str] = Field(None, description="Workspace name", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Workspace description", max_length=500)
    is_public: Optional[bool] = Field(None, description="Whether workspace is publicly accessible")


class WorkspaceMember(BaseModel):
    """Workspace member with role information."""
    user_id: str = Field(..., description="User identifier")
    role: WorkspaceRole = Field(..., description="User role in workspace")
    joined_at: datetime = Field(default_factory=datetime.now, description="Join timestamp")
    invited_by: Optional[str] = Field(None, description="User who sent the invite")


class WorkspaceInvite(BaseModel):
    """Request to invite user to workspace."""
    user_id: str = Field(..., description="User ID to invite")
    role: WorkspaceRole = Field(default=WorkspaceRole.MEMBER, description="Role to assign")
    message: Optional[str] = Field(None, description="Invitation message", max_length=500)


class Channel(BaseModel):
    """Channel model for workspace organization."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Channel identifier")
    name: str = Field(..., description="Channel name", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="Channel description", max_length=200)
    workspace_id: str = Field(..., description="Parent workspace ID")
    is_private: bool = Field(default=False, description="Whether channel is private")
    members: List[str] = Field(default_factory=list, description="Channel member user IDs")
    created_by: str = Field(..., description="Creator user ID")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class ChannelCreate(BaseModel):
    """Request to create a new channel."""
    name: str = Field(..., description="Channel name", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="Channel description", max_length=200)
    workspace_id: str = Field(..., description="Parent workspace ID")
    is_private: bool = Field(default=False, description="Whether channel is private")


class FileUpload(BaseModel):
    """File upload information."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="File identifier")
    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME content type")
    size_bytes: int = Field(..., description="File size in bytes", ge=0)
    uploaded_by: str = Field(..., description="Uploader user ID")
    workspace_id: str = Field(..., description="Workspace identifier")
    channel_id: Optional[str] = Field(None, description="Channel identifier")
    task_id: Optional[str] = Field(None, description="Associated task ID")
    comment_id: Optional[str] = Field(None, description="Associated comment ID")
    storage_path: str = Field(..., description="Storage backend path")
    download_url: Optional[str] = Field(None, description="Download URL")
    upload_date: datetime = Field(default_factory=datetime.now, description="Upload timestamp")


class Activity(BaseModel):
    """Activity log entry."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Activity identifier")
    type: ActivityType = Field(..., description="Activity type")
    user_id: str = Field(..., description="User who performed the activity")
    workspace_id: str = Field(..., description="Workspace identifier")
    target_id: Optional[str] = Field(None, description="Target resource ID (task, comment, etc.)")
    target_type: Optional[str] = Field(None, description="Target resource type")
    description: str = Field(..., description="Human-readable activity description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional activity data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Activity timestamp")


class Notification(BaseModel):
    """User notification."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Notification identifier")
    type: NotificationType = Field(..., description="Notification type")
    user_id: str = Field(..., description="Target user ID")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    workspace_id: Optional[str] = Field(None, description="Related workspace ID")
    task_id: Optional[str] = Field(None, description="Related task ID")
    is_read: bool = Field(default=False, description="Whether notification was read")
    action_url: Optional[str] = Field(None, description="Action URL for notification")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class NotificationUpdate(BaseModel):
    """Request to update notification status."""
    is_read: bool = Field(..., description="Read status")


class TaskFilter(BaseModel):
    """Task filtering and search parameters."""
    status: Optional[List[TaskStatus]] = Field(None, description="Filter by status")
    priority: Optional[List[TaskPriority]] = Field(None, description="Filter by priority")
    assigned_to: Optional[str] = Field(None, description="Filter by assigned user")
    created_by: Optional[str] = Field(None, description="Filter by creator")
    labels: Optional[List[str]] = Field(None, description="Filter by labels")
    due_before: Optional[datetime] = Field(None, description="Due before date")
    due_after: Optional[datetime] = Field(None, description="Due after date")
    search: Optional[str] = Field(None, description="Search in title and description")


class TaskBulkOperation(BaseModel):
    """Bulk operation on multiple tasks."""
    task_ids: List[str] = Field(..., description="Task IDs to operate on", min_items=1, max_items=100)
    operation: str = Field(..., description="Operation type", regex="^(update_status|update_priority|assign|add_labels|delete)$")
    parameters: Dict[str, Any] = Field(..., description="Operation parameters")
    
    class Config:
        schema_extra = {
            "example": {
                "task_ids": ["task_1", "task_2", "task_3"],
                "operation": "update_status",
                "parameters": {"status": "done"}
            }
        }


class TaskBulkResult(BaseModel):
    """Result of bulk task operation."""
    total_tasks: int = Field(..., description="Total tasks processed", ge=0)
    successful: int = Field(..., description="Successfully processed tasks", ge=0)
    failed: int = Field(..., description="Failed tasks", ge=0)
    errors: List[Dict[str, str]] = Field(default_factory=list, description="Error details")


class CollabStats(BaseModel):
    """Collaboration hub statistics."""
    total_workspaces: int = Field(..., description="Total workspaces", ge=0)
    total_tasks: int = Field(..., description="Total tasks", ge=0)
    total_comments: int = Field(..., description="Total comments", ge=0)
    total_files: int = Field(..., description="Total uploaded files", ge=0)
    active_users: int = Field(..., description="Active users in last 24h", ge=0)
    tasks_by_status: Dict[str, int] = Field(..., description="Tasks grouped by status")
    tasks_by_priority: Dict[str, int] = Field(..., description="Tasks grouped by priority")
    recent_activity_count: int = Field(..., description="Recent activities in last 24h", ge=0)


class WorkspaceStats(BaseModel):
    """Statistics for a specific workspace."""
    workspace_id: str = Field(..., description="Workspace identifier")
    member_count: int = Field(..., description="Number of members", ge=0)
    channel_count: int = Field(..., description="Number of channels", ge=0)
    task_count: int = Field(..., description="Total tasks", ge=0)
    completed_tasks: int = Field(..., description="Completed tasks", ge=0)
    comment_count: int = Field(..., description="Total comments", ge=0)
    file_count: int = Field(..., description="Total files", ge=0)
    activity_count: int = Field(..., description="Recent activities", ge=0)
    completion_rate: float = Field(..., description="Task completion rate", ge=0, le=1)


class UserPresence(BaseModel):
    """User presence information."""
    user_id: str = Field(..., description="User identifier")
    status: str = Field(..., description="Presence status", regex="^(online|away|busy|offline)$")
    last_seen: datetime = Field(..., description="Last activity timestamp")
    current_workspace: Optional[str] = Field(None, description="Current workspace ID")
    current_channel: Optional[str] = Field(None, description="Current channel ID")


class WebSocketMessage(BaseModel):
    """WebSocket message structure for real-time updates."""
    type: str = Field(..., description="Message type")
    workspace_id: Optional[str] = Field(None, description="Target workspace")
    channel_id: Optional[str] = Field(None, description="Target channel")
    user_id: Optional[str] = Field(None, description="Target user")
    data: Dict[str, Any] = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")


class HealthStatus(BaseModel):
    """Collaboration hub health status."""
    status: str = Field(..., description="Overall health status")
    service: str = Field(..., description="Service name")
    active_connections: int = Field(..., description="Active WebSocket connections", ge=0)
    total_workspaces: int = Field(..., description="Total workspaces", ge=0)
    total_tasks: int = Field(..., description="Total tasks", ge=0)
    file_storage_available: bool = Field(..., description="File storage availability")
    database_healthy: bool = Field(..., description="Database health status")
    uptime_seconds: float = Field(..., description="Service uptime", ge=0)
