"""
Collaboration Hub v1 router - Team Collaboration and Workspace Management API.

Provides comprehensive collaboration features including task management,
team workspaces, real-time communication, file sharing, and activity tracking.
"""

import asyncio
import json
import logging
import os
import time
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File, Query, Path, Depends
from fastapi.responses import JSONResponse

from _shared.api_standards.error_schemas import StandardError, ErrorCodes, create_error_response
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from models.requests import (
    Task, TaskCreate, TaskUpdate, TaskMove, TaskFilter, TaskBulkOperation, TaskBulkResult,
    Comment, CommentCreate, CommentUpdate,
    Workspace, WorkspaceCreate, WorkspaceUpdate, WorkspaceMember, WorkspaceInvite,
    Channel, ChannelCreate,
    FileUpload, Activity, Notification, NotificationUpdate,
    CollabStats, WorkspaceStats, UserPresence, HealthStatus, WebSocketMessage,
    TaskStatus, TaskPriority, WorkspaceRole, ActivityType, NotificationType
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Collaboration Hub"])


# In-memory storage (in production, replace with proper database)
class CollaborationStorage:
    """Collaboration data storage and management"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.comments: Dict[str, Comment] = {}
        self.workspaces: Dict[str, Workspace] = {}
        self.channels: Dict[str, Channel] = {}
        self.files: Dict[str, FileUpload] = {}
        self.activities: List[Activity] = []
        self.notifications: Dict[str, Notification] = {}
        self.workspace_members: Dict[str, List[WorkspaceMember]] = {}
        self.user_presence: Dict[str, UserPresence] = {}
        
        # WebSocket connections
        self.connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, List[str]] = {}
        
        # Load data from files
        self._load_data()
    
    def _load_data(self):
        """Load existing data from storage files"""
        try:
            tasks_path = os.getenv("CH_TASKS_PATH", "/data/collab_tasks.json")
            if os.path.exists(tasks_path):
                with open(tasks_path, 'r', encoding='utf-8') as f:
                    legacy_tasks = json.load(f)
                    # Convert legacy tasks to new format
                    for legacy_task in legacy_tasks:
                        task = Task(
                            id=legacy_task.get("id", str(uuid.uuid4())),
                            title=legacy_task.get("text", "Untitled"),
                            status=TaskStatus(legacy_task.get("status", "todo")),
                            priority=TaskPriority(legacy_task.get("priority", "normal")),
                            labels=legacy_task.get("labels", []),
                            workspace_id="default",  # Assign to default workspace
                            created_by="system"  # Default creator
                        )
                        self.tasks[task.id] = task
        except Exception as e:
            logger.warning(f"Failed to load legacy tasks: {e}")
        
        # Create default workspace if none exist
        if not self.workspaces:
            default_workspace = Workspace(
                id="default",
                name="Default Workspace",
                description="Default collaboration workspace",
                owner_id="system"
            )
            self.workspaces[default_workspace.id] = default_workspace
    
    def _save_data(self):
        """Save data to storage files"""
        try:
            tasks_path = os.getenv("CH_TASKS_PATH", "/data/collab_tasks.json")
            os.makedirs(os.path.dirname(tasks_path), exist_ok=True)
            
            # Convert tasks to legacy format for backward compatibility
            legacy_tasks = []
            for task in self.tasks.values():
                legacy_tasks.append({
                    "id": task.id,
                    "text": task.title,
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "labels": task.labels
                })
            
            with open(tasks_path, 'w', encoding='utf-8') as f:
                json.dump(legacy_tasks, f, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to save tasks: {e}")
    
    async def add_activity(self, activity: Activity):
        """Add activity to log and broadcast"""
        self.activities.append(activity)
        
        # Keep only last 1000 activities
        if len(self.activities) > 1000:
            self.activities = self.activities[-1000:]
        
        # Broadcast activity to workspace members
        await self.broadcast_to_workspace(activity.workspace_id, WebSocketMessage(
            type="activity",
            workspace_id=activity.workspace_id,
            data={
                "activity": activity.dict(),
                "timestamp": activity.timestamp.isoformat()
            }
        ))
    
    async def broadcast_to_workspace(self, workspace_id: str, message: WebSocketMessage):
        """Broadcast message to all users in a workspace"""
        if workspace_id not in self.workspace_members:
            return
        
        workspace_users = [member.user_id for member in self.workspace_members[workspace_id]]
        message_data = json.dumps(message.dict(), default=str)
        
        for user_id in workspace_users:
            if user_id in self.user_connections:
                for connection_id in self.user_connections[user_id]:
                    if connection_id in self.connections:
                        try:
                            await self.connections[connection_id].send_text(message_data)
                        except Exception as e:
                            logger.warning(f"Failed to send message to {connection_id}: {e}")
    
    async def connect_user(self, connection_id: str, websocket: WebSocket, user_id: str):
        """Connect user via WebSocket"""
        await websocket.accept()
        self.connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        # Update user presence
        self.user_presence[user_id] = UserPresence(
            user_id=user_id,
            status="online",
            last_seen=datetime.now()
        )
    
    async def disconnect_user(self, connection_id: str, user_id: str):
        """Disconnect user WebSocket"""
        if connection_id in self.connections:
            del self.connections[connection_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id] = [
                cid for cid in self.user_connections[user_id] if cid != connection_id
            ]
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
                
                # Update presence to offline
                if user_id in self.user_presence:
                    self.user_presence[user_id].status = "offline"
                    self.user_presence[user_id].last_seen = datetime.now()


# Initialize storage
storage = CollaborationStorage()


# Dependency for error handling
def handle_collab_errors(func):
    """Decorator to handle collaboration operation errors with standard error format"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Collaboration validation error: {e}")
            error_response = create_error_response(
                ErrorCodes.VALIDATION_ERROR,
                str(e),
                {"service": "collab-hub"}
            )
            raise HTTPException(status_code=400, detail=error_response.dict())
        except Exception as e:
            logger.error(f"Collaboration operation failed: {e}")
            error_response = create_error_response(
                ErrorCodes.INTERNAL_ERROR,
                "Internal collaboration operation error",
                {"service": "collab-hub", "original_error": str(e)}
            )
            raise HTTPException(status_code=500, detail=error_response.dict())
    return wrapper


@router.websocket("/ws/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    connection_id: str = Path(..., description="Unique connection identifier"),
    user_id: str = Query(..., description="User identifier")
):
    """
    WebSocket endpoint for real-time collaboration.
    
    Supports:
    - Real-time task updates
    - Live comments and discussions  
    - User presence indicators
    - Activity feed streaming
    - File upload notifications
    """
    await storage.connect_user(connection_id, websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Handle different message types
                if message.get("type") == "presence_update":
                    if user_id in storage.user_presence:
                        storage.user_presence[user_id].status = message.get("status", "online")
                        storage.user_presence[user_id].current_workspace = message.get("workspace_id")
                        storage.user_presence[user_id].current_channel = message.get("channel_id")
                
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from {connection_id}")
            
    except WebSocketDisconnect:
        await storage.disconnect_user(connection_id, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for {connection_id}: {e}")
        await storage.disconnect_user(connection_id, user_id)


# Task Management Endpoints

@router.get("/tasks", response_model=PaginatedResponse[Task])
@handle_collab_errors
async def list_tasks(
    pagination: PaginationParams = Depends(),
    workspace_id: Optional[str] = Query(None, description="Filter by workspace"),
    status: Optional[List[TaskStatus]] = Query(None, description="Filter by status"),
    priority: Optional[List[TaskPriority]] = Query(None, description="Filter by priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user"),
    labels: Optional[List[str]] = Query(None, description="Filter by labels"),
    search: Optional[str] = Query(None, description="Search in title and description")
) -> PaginatedResponse[Task]:
    """
    List tasks with filtering, searching, and pagination.
    
    Supports comprehensive filtering by workspace, status, priority,
    assignments, labels, and text search across title/description.
    """
    # Apply filters
    filtered_tasks = list(storage.tasks.values())
    
    if workspace_id:
        filtered_tasks = [t for t in filtered_tasks if t.workspace_id == workspace_id]
    
    if status:
        status_values = [s.value for s in status]
        filtered_tasks = [t for t in filtered_tasks if t.status.value in status_values]
    
    if priority:
        priority_values = [p.value for p in priority]
        filtered_tasks = [t for t in filtered_tasks if t.priority.value in priority_values]
    
    if assigned_to:
        filtered_tasks = [t for t in filtered_tasks if t.assigned_to == assigned_to]
    
    if labels:
        filtered_tasks = [t for t in filtered_tasks if any(label in t.labels for label in labels)]
    
    if search:
        search_lower = search.lower()
        filtered_tasks = [
            t for t in filtered_tasks 
            if search_lower in t.title.lower() or 
            (t.description and search_lower in t.description.lower())
        ]
    
    # Sort by creation date (newest first)
    filtered_tasks.sort(key=lambda x: x.created_at, reverse=True)
    
    # Paginate
    total = len(filtered_tasks)
    start_idx = (pagination.page - 1) * pagination.size
    end_idx = start_idx + pagination.size
    page_tasks = filtered_tasks[start_idx:end_idx]
    
    return PaginatedResponse.create(page_tasks, total, pagination)


@router.post("/tasks", response_model=Task)
@handle_collab_errors
async def create_task(task_data: TaskCreate, created_by: str = Query(..., description="Creator user ID")) -> Task:
    """
    Create a new task with comprehensive properties.
    
    Automatically generates activity log entry and broadcasts
    creation event to workspace members.
    """
    # Validate workspace exists
    if task_data.workspace_id not in storage.workspaces:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Workspace not found: {task_data.workspace_id}",
            {"workspace_id": task_data.workspace_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    # Create task
    task = Task(
        **task_data.dict(),
        created_by=created_by
    )
    
    storage.tasks[task.id] = task
    storage._save_data()
    
    # Log activity
    activity = Activity(
        type=ActivityType.TASK_CREATED,
        user_id=created_by,
        workspace_id=task.workspace_id,
        target_id=task.id,
        target_type="task",
        description=f"Created task: {task.title}"
    )
    await storage.add_activity(activity)
    
    return task


@router.get("/tasks/{task_id}", response_model=Task)
@handle_collab_errors
async def get_task(task_id: str = Path(..., description="Task identifier")) -> Task:
    """Get task details by ID."""
    if task_id not in storage.tasks:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Task not found: {task_id}",
            {"task_id": task_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    return storage.tasks[task_id]


@router.put("/tasks/{task_id}", response_model=Task)
@handle_collab_errors
async def update_task(
    task_id: str = Path(..., description="Task identifier"),
    task_data: TaskUpdate = ...,
    updated_by: str = Query(..., description="User performing update")
) -> Task:
    """
    Update task properties with change tracking.
    
    Logs all changes and broadcasts updates to workspace members.
    """
    if task_id not in storage.tasks:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Task not found: {task_id}",
            {"task_id": task_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    task = storage.tasks[task_id]
    
    # Track changes for activity log
    changes = []
    update_data = task_data.dict(exclude_unset=True)
    
    for field, new_value in update_data.items():
        old_value = getattr(task, field)
        if old_value != new_value:
            changes.append(f"{field}: {old_value} → {new_value}")
            setattr(task, field, new_value)
    
    task.updated_at = datetime.now()
    
    # Mark as completed if status changed to done
    if task_data.status == TaskStatus.DONE and task.completed_at is None:
        task.completed_at = datetime.now()
    
    storage._save_data()
    
    # Log activity
    if changes:
        activity = Activity(
            type=ActivityType.TASK_UPDATED,
            user_id=updated_by,
            workspace_id=task.workspace_id,
            target_id=task.id,
            target_type="task",
            description=f"Updated task: {'; '.join(changes)}"
        )
        await storage.add_activity(activity)
    
    return task


@router.post("/tasks/{task_id}/move", response_model=Task)
@handle_collab_errors
async def move_task(
    task_id: str = Path(..., description="Task identifier"),
    move_data: TaskMove = ...,
    moved_by: str = Query(..., description="User performing move")
) -> Task:
    """
    Move task to different status (todo, in_progress, done, etc.).
    
    Provides dedicated endpoint for status changes with proper
    activity logging and real-time updates.
    """
    if task_id not in storage.tasks:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Task not found: {task_id}",
            {"task_id": task_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    task = storage.tasks[task_id]
    old_status = task.status
    task.status = move_data.status
    task.updated_at = datetime.now()
    
    # Mark completion time
    if move_data.status == TaskStatus.DONE:
        task.completed_at = datetime.now()
    elif old_status == TaskStatus.DONE:
        task.completed_at = None
    
    storage._save_data()
    
    # Log activity
    activity = Activity(
        type=ActivityType.TASK_MOVED,
        user_id=moved_by,
        workspace_id=task.workspace_id,
        target_id=task.id,
        target_type="task",
        description=f"Moved task from {old_status.value} to {move_data.status.value}"
    )
    await storage.add_activity(activity)
    
    return task


@router.delete("/tasks/{task_id}")
@handle_collab_errors
async def delete_task(
    task_id: str = Path(..., description="Task identifier"),
    deleted_by: str = Query(..., description="User performing deletion")
) -> Dict[str, Any]:
    """Delete task and associated comments/files."""
    if task_id not in storage.tasks:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Task not found: {task_id}",
            {"task_id": task_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    task = storage.tasks[task_id]
    
    # Delete associated comments
    task_comments = [c for c in storage.comments.values() if c.task_id == task_id]
    for comment in task_comments:
        del storage.comments[comment.id]
    
    # Delete task
    del storage.tasks[task_id]
    storage._save_data()
    
    # Log activity
    activity = Activity(
        type=ActivityType.TASK_DELETED,
        user_id=deleted_by,
        workspace_id=task.workspace_id,
        target_id=task_id,
        target_type="task",
        description=f"Deleted task: {task.title}"
    )
    await storage.add_activity(activity)
    
    return {"task_id": task_id, "message": "Task deleted successfully"}


@router.post("/tasks/bulk", response_model=TaskBulkResult)
@handle_collab_errors
async def bulk_task_operation(
    operation: TaskBulkOperation,
    performed_by: str = Query(..., description="User performing bulk operation")
) -> TaskBulkResult:
    """
    Perform bulk operations on multiple tasks.
    
    Supports bulk status updates, priority changes, assignments,
    label additions, and deletions with comprehensive error handling.
    """
    successful = 0
    errors = []
    
    for task_id in operation.task_ids:
        try:
            if task_id not in storage.tasks:
                errors.append({"task_id": task_id, "error": "Task not found"})
                continue
            
            task = storage.tasks[task_id]
            
            if operation.operation == "update_status":
                new_status = TaskStatus(operation.parameters["status"])
                old_status = task.status
                task.status = new_status
                task.updated_at = datetime.now()
                
                if new_status == TaskStatus.DONE:
                    task.completed_at = datetime.now()
                elif old_status == TaskStatus.DONE:
                    task.completed_at = None
                
            elif operation.operation == "update_priority":
                task.priority = TaskPriority(operation.parameters["priority"])
                task.updated_at = datetime.now()
                
            elif operation.operation == "assign":
                task.assigned_to = operation.parameters["user_id"]
                task.updated_at = datetime.now()
                
            elif operation.operation == "add_labels":
                new_labels = operation.parameters["labels"]
                task.labels = list(set(task.labels + new_labels))
                task.updated_at = datetime.now()
                
            elif operation.operation == "delete":
                del storage.tasks[task_id]
            
            successful += 1
            
        except Exception as e:
            errors.append({"task_id": task_id, "error": str(e)})
    
    storage._save_data()
    
    # Log bulk activity
    activity = Activity(
        type=ActivityType.TASK_UPDATED,
        user_id=performed_by,
        workspace_id="multiple",  # Bulk operations can span workspaces
        description=f"Bulk operation '{operation.operation}' on {successful} tasks"
    )
    await storage.add_activity(activity)
    
    return TaskBulkResult(
        total_tasks=len(operation.task_ids),
        successful=successful,
        failed=len(errors),
        errors=errors
    )


# Comments and Discussions

@router.get("/comments", response_model=PaginatedResponse[Comment])
@handle_collab_errors
async def list_comments(
    pagination: PaginationParams = Depends(),
    task_id: Optional[str] = Query(None, description="Filter by task ID"),
    workspace_id: Optional[str] = Query(None, description="Filter by workspace"),
    author_id: Optional[str] = Query(None, description="Filter by author")
) -> PaginatedResponse[Comment]:
    """List comments with filtering and pagination."""
    filtered_comments = list(storage.comments.values())
    
    if task_id:
        filtered_comments = [c for c in filtered_comments if c.task_id == task_id]
    
    if workspace_id:
        filtered_comments = [c for c in filtered_comments if c.workspace_id == workspace_id]
    
    if author_id:
        filtered_comments = [c for c in filtered_comments if c.author_id == author_id]
    
    # Sort by creation time
    filtered_comments.sort(key=lambda x: x.created_at, reverse=True)
    
    # Paginate
    total = len(filtered_comments)
    start_idx = (pagination.page - 1) * pagination.size
    end_idx = start_idx + pagination.size
    page_comments = filtered_comments[start_idx:end_idx]
    
    return PaginatedResponse.create(page_comments, total, pagination)


@router.post("/comments", response_model=Comment)
@handle_collab_errors
async def create_comment(
    comment_data: CommentCreate,
    author_id: str = Query(..., description="Comment author user ID")
) -> Comment:
    """
    Create new comment with mention support.
    
    Automatically creates notifications for mentioned users
    and broadcasts real-time updates to workspace members.
    """
    comment = Comment(
        **comment_data.dict(),
        author_id=author_id
    )
    
    storage.comments[comment.id] = comment
    
    # Create notifications for mentions
    for mentioned_user in comment.mentions:
        notification = Notification(
            type=NotificationType.COMMENT_MENTION,
            user_id=mentioned_user,
            title="You were mentioned in a comment",
            message=f"@{author_id} mentioned you: {comment.content[:100]}...",
            workspace_id=comment.workspace_id,
            task_id=comment.task_id
        )
        storage.notifications[notification.id] = notification
    
    # Log activity
    activity = Activity(
        type=ActivityType.COMMENT_ADDED,
        user_id=author_id,
        workspace_id=comment.workspace_id,
        target_id=comment.id,
        target_type="comment",
        description=f"Added comment: {comment.content[:50]}..."
    )
    await storage.add_activity(activity)
    
    return comment


@router.put("/comments/{comment_id}", response_model=Comment)
@handle_collab_errors
async def update_comment(
    comment_id: str = Path(..., description="Comment identifier"),
    comment_data: CommentUpdate = ...,
    updated_by: str = Query(..., description="User updating comment")
) -> Comment:
    """Update comment content with edit tracking."""
    if comment_id not in storage.comments:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Comment not found: {comment_id}",
            {"comment_id": comment_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    comment = storage.comments[comment_id]
    
    # Check if user can edit (author only, or admin)
    if comment.author_id != updated_by:
        error_response = create_error_response(
            ErrorCodes.FORBIDDEN,
            "Only comment author can edit comments",
            {"comment_id": comment_id, "author_id": comment.author_id}
        )
        raise HTTPException(status_code=403, detail=error_response.dict())
    
    comment.content = comment_data.content
    comment.updated_at = datetime.now()
    comment.is_edited = True
    
    # Log activity
    activity = Activity(
        type=ActivityType.COMMENT_UPDATED,
        user_id=updated_by,
        workspace_id=comment.workspace_id,
        target_id=comment.id,
        target_type="comment",
        description=f"Edited comment: {comment.content[:50]}..."
    )
    await storage.add_activity(activity)
    
    return comment


@router.delete("/comments/{comment_id}")
@handle_collab_errors
async def delete_comment(
    comment_id: str = Path(..., description="Comment identifier"),
    deleted_by: str = Query(..., description="User deleting comment")
) -> Dict[str, Any]:
    """Delete comment with permission checking."""
    if comment_id not in storage.comments:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Comment not found: {comment_id}",
            {"comment_id": comment_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    comment = storage.comments[comment_id]
    
    # Check permissions (author or workspace admin)
    if comment.author_id != deleted_by:
        # Would need to check workspace admin role here
        error_response = create_error_response(
            ErrorCodes.FORBIDDEN,
            "Only comment author can delete comments",
            {"comment_id": comment_id}
        )
        raise HTTPException(status_code=403, detail=error_response.dict())
    
    del storage.comments[comment_id]
    
    # Log activity
    activity = Activity(
        type=ActivityType.COMMENT_DELETED,
        user_id=deleted_by,
        workspace_id=comment.workspace_id,
        target_id=comment_id,
        target_type="comment",
        description=f"Deleted comment: {comment.content[:50]}..."
    )
    await storage.add_activity(activity)
    
    return {"comment_id": comment_id, "message": "Comment deleted successfully"}


# Workspace Management

@router.get("/workspaces", response_model=PaginatedResponse[Workspace])
@handle_collab_errors
async def list_workspaces(
    pagination: PaginationParams = Depends(),
    user_id: str = Query(..., description="User ID to filter accessible workspaces")
) -> PaginatedResponse[Workspace]:
    """List workspaces accessible to user."""
    # Filter workspaces where user is member or public workspaces
    accessible_workspaces = []
    
    for workspace in storage.workspaces.values():
        if (workspace.is_public or 
            workspace.owner_id == user_id or
            user_id in workspace.members or
            (workspace.id in storage.workspace_members and 
             any(member.user_id == user_id for member in storage.workspace_members[workspace.id]))):
            accessible_workspaces.append(workspace)
    
    # Sort by name
    accessible_workspaces.sort(key=lambda x: x.name)
    
    # Paginate
    total = len(accessible_workspaces)
    start_idx = (pagination.page - 1) * pagination.size
    end_idx = start_idx + pagination.size
    page_workspaces = accessible_workspaces[start_idx:end_idx]
    
    return PaginatedResponse.create(page_workspaces, total, pagination)


@router.post("/workspaces", response_model=Workspace)
@handle_collab_errors
async def create_workspace(
    workspace_data: WorkspaceCreate,
    created_by: str = Query(..., description="Workspace creator user ID")
) -> Workspace:
    """Create new workspace with creator as owner."""
    workspace = Workspace(
        **workspace_data.dict(),
        owner_id=created_by,
        members=[created_by]
    )
    
    storage.workspaces[workspace.id] = workspace
    
    # Add creator as owner member
    if workspace.id not in storage.workspace_members:
        storage.workspace_members[workspace.id] = []
    
    storage.workspace_members[workspace.id].append(WorkspaceMember(
        user_id=created_by,
        role=WorkspaceRole.OWNER
    ))
    
    # Log activity
    activity = Activity(
        type=ActivityType.WORKSPACE_CREATED,
        user_id=created_by,
        workspace_id=workspace.id,
        description=f"Created workspace: {workspace.name}"
    )
    await storage.add_activity(activity)
    
    return workspace


@router.get("/workspaces/{workspace_id}/stats", response_model=WorkspaceStats)
@handle_collab_errors
async def get_workspace_stats(
    workspace_id: str = Path(..., description="Workspace identifier")
) -> WorkspaceStats:
    """Get comprehensive workspace statistics."""
    if workspace_id not in storage.workspaces:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Workspace not found: {workspace_id}",
            {"workspace_id": workspace_id}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    # Calculate statistics
    workspace_tasks = [t for t in storage.tasks.values() if t.workspace_id == workspace_id]
    completed_tasks = [t for t in workspace_tasks if t.status == TaskStatus.DONE]
    workspace_comments = [c for c in storage.comments.values() if c.workspace_id == workspace_id]
    workspace_files = [f for f in storage.files.values() if f.workspace_id == workspace_id]
    workspace_activities = [a for a in storage.activities if a.workspace_id == workspace_id]
    recent_activities = [a for a in workspace_activities if (datetime.now() - a.timestamp).days < 7]
    
    completion_rate = len(completed_tasks) / max(len(workspace_tasks), 1)
    member_count = len(storage.workspace_members.get(workspace_id, []))
    channel_count = len([c for c in storage.channels.values() if c.workspace_id == workspace_id])
    
    return WorkspaceStats(
        workspace_id=workspace_id,
        member_count=member_count,
        channel_count=channel_count,
        task_count=len(workspace_tasks),
        completed_tasks=len(completed_tasks),
        comment_count=len(workspace_comments),
        file_count=len(workspace_files),
        activity_count=len(recent_activities),
        completion_rate=completion_rate
    )


# Statistics and Health

@router.get("/stats", response_model=CollabStats)
@handle_collab_errors
async def get_collaboration_stats() -> CollabStats:
    """Get overall collaboration hub statistics."""
    # Calculate recent activity (last 24 hours)
    recent_cutoff = datetime.now() - timedelta(hours=24)
    recent_activities = [a for a in storage.activities if a.timestamp >= recent_cutoff]
    
    # Get unique active users from recent activities
    active_users = set(a.user_id for a in recent_activities)
    
    # Group tasks by status and priority
    tasks_by_status = {}
    tasks_by_priority = {}
    
    for task in storage.tasks.values():
        status_key = task.status.value
        priority_key = task.priority.value
        
        tasks_by_status[status_key] = tasks_by_status.get(status_key, 0) + 1
        tasks_by_priority[priority_key] = tasks_by_priority.get(priority_key, 0) + 1
    
    return CollabStats(
        total_workspaces=len(storage.workspaces),
        total_tasks=len(storage.tasks),
        total_comments=len(storage.comments),
        total_files=len(storage.files),
        active_users=len(active_users),
        tasks_by_status=tasks_by_status,
        tasks_by_priority=tasks_by_priority,
        recent_activity_count=len(recent_activities)
    )


@router.get("/health", response_model=HealthStatus)
async def get_collaboration_health() -> HealthStatus:
    """Get collaboration hub health status."""
    import psutil
    
    # Calculate uptime
    start_time = getattr(storage, '_start_time', datetime.now())
    uptime = (datetime.now() - start_time).total_seconds()
    
    # Check file storage
    file_storage_available = True
    try:
        tasks_path = os.getenv("CH_TASKS_PATH", "/data/collab_tasks.json")
        os.makedirs(os.path.dirname(tasks_path), exist_ok=True)
        test_file = os.path.join(os.path.dirname(tasks_path), ".health_test")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
    except Exception:
        file_storage_available = False
    
    return HealthStatus(
        status="healthy" if file_storage_available else "degraded",
        service="collab-hub",
        active_connections=len(storage.connections),
        total_workspaces=len(storage.workspaces),
        total_tasks=len(storage.tasks),
        file_storage_available=file_storage_available,
        database_healthy=True,  # Using in-memory storage
        uptime_seconds=uptime
    )


@router.get("/labels", response_model=Dict[str, Any])
@handle_collab_errors
async def get_labels_statistics() -> Dict[str, Any]:
    """Get label usage statistics across all tasks."""
    label_counts = {}
    
    for task in storage.tasks.values():
        for label in task.labels:
            label_counts[label] = label_counts.get(label, 0) + 1
    
    # Sort by usage count
    sorted_labels = sorted(
        [{"label": k, "count": v} for k, v in label_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )
    
    return {
        "labels": sorted_labels[:50],  # Top 50 labels
        "total_unique_labels": len(label_counts)
    }


# Initialize storage start time for uptime calculation
if not hasattr(storage, '_start_time'):
    storage._start_time = datetime.now()
