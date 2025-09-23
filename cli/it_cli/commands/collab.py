"""Collaboration and task management commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Collaboration & Task Management")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def workspaces(
    action: Optional[str] = typer.Argument(None, help="Action: list|create|delete"),
    workspace_id: Optional[str] = typer.Option(None, "--id", help="Workspace ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Workspace name"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description"),
) -> None:
    """Manage collaboration workspaces."""
    settings = get_settings()

    async def _action():
        if not action or action == "list":
            # List workspaces
            async with client() as c:
                resp = await c.get(f"{settings.collab_api}/v1/workspaces")
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title=f"Workspaces ({data.get('total', 0)})")
                table.add_column("ID")
                table.add_column("Name")
                table.add_column("Members")
                table.add_column("Tasks")
                table.add_column("Status")
                table.add_column("Created")
                
                for workspace in data.get("items", []):
                    table.add_row(
                        workspace.get("id", "")[:8] + "...",
                        workspace.get("name", ""),
                        str(workspace.get("member_count", 0)),
                        str(workspace.get("task_count", 0)),
                        workspace.get("status", ""),
                        workspace.get("created_at", ""),
                    )
                
                console.print(table)
                
        elif action == "create":
            if not name:
                console.print("❌ Workspace name required for create action")
                return
                
            payload = {"name": name}
            if description:
                payload["description"] = description
                
            async with client() as c:
                resp = await c.post(f"{settings.collab_api}/v1/workspaces", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Workspace created")
                console.print(f"ID: {result.get('id')}")
                console.print(f"Name: {name}")
                
        elif action == "delete":
            if not workspace_id:
                console.print("❌ Workspace ID required for delete action")
                return
                
            confirm = typer.confirm(f"Delete workspace {workspace_id}?")
            if not confirm:
                console.print("❌ Operation cancelled")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.collab_api}/v1/workspaces/{workspace_id}")
                resp.raise_for_status()
                console.print(f"🗑️  Workspace deleted: {workspace_id}")

    _run(_action)

@app.command()
def tasks(
    action: Optional[str] = typer.Argument(None, help="Action: list|create|update|delete"),
    task_id: Optional[str] = typer.Option(None, "--id", help="Task ID"),
    workspace_id: Optional[str] = typer.Option(None, "--workspace", "-w", help="Workspace ID"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Task title"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Task status"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Task priority"),
    assignee: Optional[str] = typer.Option(None, "--assignee", "-a", help="Assigned user"),
    labels: List[str] = typer.Option([], "--label", "-l", help="Task labels"),
) -> None:
    """Manage collaboration tasks."""
    settings = get_settings()

    async def _action():
        if not action or action == "list":
            # List tasks
            params = {}
            if workspace_id:
                params["workspace_id"] = workspace_id
            if status:
                params["status"] = status
            if assignee:
                params["assignee"] = assignee
                
            async with client() as c:
                resp = await c.get(f"{settings.collab_api}/v1/tasks", params=params)
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title=f"Tasks ({data.get('total', 0)})")
                table.add_column("ID")
                table.add_column("Title")
                table.add_column("Status")
                table.add_column("Priority")
                table.add_column("Assignee")
                table.add_column("Due Date")
                
                for task in data.get("items", []):
                    task_id_short = task.get("id", "")[:8] + "..."
                    priority_icon = "🔴" if task.get("priority") == "high" else "🟡" if task.get("priority") == "medium" else "🟢"
                    
                    table.add_row(
                        task_id_short,
                        task.get("title", "")[:30] + "...",
                        task.get("status", ""),
                        f"{priority_icon} {task.get('priority', '')}",
                        task.get("assignee", ""),
                        task.get("due_date", ""),
                    )
                
                console.print(table)
                
        elif action == "create":
            if not title:
                console.print("❌ Task title required for create action")
                return
                
            payload = {"title": title}
            if workspace_id:
                payload["workspace_id"] = workspace_id
            if status:
                payload["status"] = status
            if priority:
                payload["priority"] = priority
            if assignee:
                payload["assignee"] = assignee
            if labels:
                payload["labels"] = labels
                
            async with client() as c:
                resp = await c.post(f"{settings.collab_api}/v1/tasks", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Task created")
                console.print(f"ID: {result.get('id')}")
                console.print(f"Title: {title}")
                console.print(f"Status: {result.get('status', 'todo')}")
                
        elif action == "update":
            if not task_id:
                console.print("❌ Task ID required for update action")
                return
                
            payload = {}
            if title:
                payload["title"] = title
            if status:
                payload["status"] = status
            if priority:
                payload["priority"] = priority
            if assignee:
                payload["assignee"] = assignee
            if labels:
                payload["labels"] = labels
                
            if not payload:
                console.print("❌ No update fields provided")
                return
                
            async with client() as c:
                resp = await c.put(f"{settings.collab_api}/v1/tasks/{task_id}", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Task updated: {task_id}")
                for key, value in payload.items():
                    console.print(f"  {key}: {value}")
                    
        elif action == "delete":
            if not task_id:
                console.print("❌ Task ID required for delete action")
                return
                
            confirm = typer.confirm(f"Delete task {task_id}?")
            if not confirm:
                console.print("❌ Operation cancelled")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.collab_api}/v1/tasks/{task_id}")
                resp.raise_for_status()
                console.print(f"🗑️  Task deleted: {task_id}")

    _run(_action)

@app.command()
def show(
    task_id: str = typer.Argument(..., help="Task ID"),
    comments: bool = typer.Option(False, "--comments", "-c", help="Show comments"),
) -> None:
    """Show detailed task information."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.collab_api}/v1/tasks/{task_id}")
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📋 Task: {data.get('title', '')}")
            console.print(f"ID: {task_id}")
            console.print(f"Status: {data.get('status', '')}")
            console.print(f"Priority: {data.get('priority', '')}")
            console.print(f"Assignee: {data.get('assignee', 'Unassigned')}")
            console.print(f"Created: {data.get('created_at', '')}")
            console.print(f"Updated: {data.get('updated_at', '')}")
            console.print(f"Due Date: {data.get('due_date', 'Not set')}")
            
            if data.get("description"):
                console.print(f"\nDescription:")
                console.print(f"  {data.get('description', '')}")
            
            if data.get("labels"):
                labels_str = ", ".join(data.get("labels", []))
                console.print(f"\nLabels: {labels_str}")
            
            if data.get("subtasks"):
                console.print(f"\nSubtasks ({len(data.get('subtasks', []))}):")
                for subtask in data.get("subtasks", []):
                    status_icon = "✅" if subtask.get("completed", False) else "⏳"
                    console.print(f"  {status_icon} {subtask.get('title', '')}")
            
            if comments:
                # Fetch comments
                resp = await c.get(f"{settings.collab_api}/v1/comments", params={"task_id": task_id})
                resp.raise_for_status()
                comments_data = resp.json()
                
                if comments_data.get("items"):
                    console.print(f"\n💬 Comments ({len(comments_data.get('items', []))}):")
                    for comment in comments_data.get("items", []):
                        author = comment.get("author", "Unknown")
                        content = comment.get("content", "")
                        timestamp = comment.get("created_at", "")
                        console.print(f"  {author} ({timestamp}): {content}")

    _run(_action)

@app.command()
def move(
    task_id: str = typer.Argument(..., help="Task ID"),
    status: str = typer.Argument(..., help="Target status"),
    position: Optional[int] = typer.Option(None, "--position", "-p", help="Position in column"),
) -> None:
    """Move task to different status/position."""
    settings = get_settings()

    async def _action():
        payload = {"status": status}
        if position is not None:
            payload["position"] = position
            
        async with client() as c:
            resp = await c.post(f"{settings.collab_api}/v1/tasks/{task_id}/move", json=payload)
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"✅ Task moved")
            console.print(f"Task: {task_id}")
            console.print(f"Status: {status}")
            console.print(f"Position: {result.get('position', 'Last')}")

    _run(_action)

@app.command()
def bulk(
    action: str = typer.Argument(..., help="Action: update|delete|move"),
    task_ids: List[str] = typer.Option([], "--task", "-t", help="Task IDs"),
    file: Optional[typer.FileText] = typer.Option(None, "--file", "-f", help="File with task IDs"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="New status"),
    assignee: Optional[str] = typer.Option(None, "--assignee", "-a", help="New assignee"),
    labels: List[str] = typer.Option([], "--label", "-l", help="New labels"),
) -> None:
    """Bulk operations on tasks."""
    settings = get_settings()

    async def _action():
        # Get task IDs from file if provided
        if file:
            import json
            try:
                file_data = json.load(file)
                if isinstance(file_data, list):
                    task_ids.extend(file_data)
                elif isinstance(file_data, dict) and "task_ids" in file_data:
                    task_ids.extend(file_data["task_ids"])
            except json.JSONDecodeError:
                console.print("❌ Invalid JSON file")
                return
        
        if not task_ids:
            console.print("❌ No task IDs provided")
            return
        
        payload = {"task_ids": task_ids}
        
        if action == "update":
            updates = {}
            if status:
                updates["status"] = status
            if assignee:
                updates["assignee"] = assignee
            if labels:
                updates["labels"] = labels
                
            if not updates:
                console.print("❌ No update fields provided")
                return
                
            payload["updates"] = updates
            
            async with client() as c:
                resp = await c.put(f"{settings.collab_api}/v1/tasks/bulk", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Bulk update completed")
                console.print(f"Updated: {result.get('updated_count', 0)}")
                console.print(f"Failed: {result.get('failed_count', 0)}")
                
        elif action == "delete":
            confirm = typer.confirm(f"Delete {len(task_ids)} tasks?")
            if not confirm:
                console.print("❌ Operation cancelled")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.collab_api}/v1/tasks/bulk", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"🗑️  Bulk delete completed")
                console.print(f"Deleted: {result.get('deleted_count', 0)}")
                
        elif action == "move":
            if not status:
                console.print("❌ Target status required for move action")
                return
                
            payload["target_status"] = status
            
            async with client() as c:
                resp = await c.post(f"{settings.collab_api}/v1/tasks/bulk/move", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Bulk move completed")
                console.print(f"Moved: {result.get('moved_count', 0)}")
                console.print(f"Target Status: {status}")

    _run(_action)

@app.command()
def comments(
    action: Optional[str] = typer.Argument(None, help="Action: list|create|delete"),
    task_id: Optional[str] = typer.Option(None, "--task", "-t", help="Task ID"),
    comment_id: Optional[str] = typer.Option(None, "--id", help="Comment ID"),
    content: Optional[str] = typer.Option(None, "--content", "-c", help="Comment content"),
    thread: bool = typer.Option(False, "--thread", help="Show threaded comments"),
) -> None:
    """Manage task comments."""
    settings = get_settings()

    async def _action():
        if not action or action == "list":
            if not task_id:
                console.print("❌ Task ID required for list action")
                return
                
            params = {"task_id": task_id}
            if thread:
                params["threaded"] = True
                
            async with client() as c:
                resp = await c.get(f"{settings.collab_api}/v1/comments", params=params)
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"💬 Comments for Task: {task_id}")
                
                for comment in data.get("items", []):
                    author = comment.get("author", "Unknown")
                    content_text = comment.get("content", "")
                    timestamp = comment.get("created_at", "")
                    
                    console.print(f"\n📝 {author} ({timestamp}):")
                    console.print(f"   {content_text}")
                    
                    # Show replies if threaded
                    if thread and comment.get("replies"):
                        for reply in comment.get("replies", []):
                            reply_author = reply.get("author", "Unknown")
                            reply_content = reply.get("content", "")
                            reply_time = reply.get("created_at", "")
                            console.print(f"   ↳ {reply_author} ({reply_time}): {reply_content}")
                            
        elif action == "create":
            if not task_id or not content:
                console.print("❌ Task ID and content required for create action")
                return
                
            payload = {
                "task_id": task_id,
                "content": content
            }
            
            async with client() as c:
                resp = await c.post(f"{settings.collab_api}/v1/comments", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Comment created")
                console.print(f"ID: {result.get('id')}")
                console.print(f"Task: {task_id}")
                
        elif action == "delete":
            if not comment_id:
                console.print("❌ Comment ID required for delete action")
                return
                
            confirm = typer.confirm(f"Delete comment {comment_id}?")
            if not confirm:
                console.print("❌ Operation cancelled")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.collab_api}/v1/comments/{comment_id}")
                resp.raise_for_status()
                console.print(f"🗑️  Comment deleted: {comment_id}")

    _run(_action)

@app.command()
def labels(
    action: Optional[str] = typer.Argument(None, help="Action: list|create|delete"),
    label_name: Optional[str] = typer.Option(None, "--name", "-n", help="Label name"),
    color: Optional[str] = typer.Option(None, "--color", "-c", help="Label color"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Label description"),
) -> None:
    """Manage task labels."""
    settings = get_settings()

    async def _action():
        if not action or action == "list":
            async with client() as c:
                resp = await c.get(f"{settings.collab_api}/v1/labels")
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Task Labels")
                table.add_column("Name")
                table.add_column("Color")
                table.add_column("Usage Count")
                table.add_column("Description")
                
                for label in data.get("items", []):
                    table.add_row(
                        label.get("name", ""),
                        label.get("color", ""),
                        str(label.get("usage_count", 0)),
                        label.get("description", "")[:50] + "...",
                    )
                
                console.print(table)
                
        elif action == "create":
            if not label_name:
                console.print("❌ Label name required for create action")
                return
                
            payload = {"name": label_name}
            if color:
                payload["color"] = color
            if description:
                payload["description"] = description
                
            async with client() as c:
                resp = await c.post(f"{settings.collab_api}/v1/labels", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Label created")
                console.print(f"Name: {label_name}")
                console.print(f"Color: {result.get('color', 'Default')}")
                
        elif action == "delete":
            if not label_name:
                console.print("❌ Label name required for delete action")
                return
                
            confirm = typer.confirm(f"Delete label '{label_name}'?")
            if not confirm:
                console.print("❌ Operation cancelled")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.collab_api}/v1/labels/{label_name}")
                resp.raise_for_status()
                console.print(f"🗑️  Label deleted: {label_name}")

    _run(_action)

@app.command()
def board(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    view: str = typer.Option("kanban", "--view", "-v", help="View type: kanban|list|calendar"),
) -> None:
    """Show workspace task board."""
    settings = get_settings()

    async def _action():
        params = {"view": view}
        
        async with client() as c:
            resp = await c.get(f"{settings.collab_api}/v1/workspaces/{workspace_id}/stats", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📋 Task Board: {data.get('workspace_name', workspace_id)}")
            
            if view == "kanban":
                # Kanban board view
                columns = data.get("kanban_columns", {})
                
                for status, tasks in columns.items():
                    console.print(f"\n📌 {status.upper()} ({len(tasks)})")
                    for task in tasks[:5]:  # Show top 5 tasks per column
                        priority_icon = "🔴" if task.get("priority") == "high" else "🟡" if task.get("priority") == "medium" else "🟢"
                        console.print(f"  {priority_icon} {task.get('title', '')[:40]}")
                    
                    if len(tasks) > 5:
                        console.print(f"  ... and {len(tasks) - 5} more")
                        
            elif view == "list":
                # List view
                tasks = data.get("tasks", [])
                
                table = Table(title="Task List")
                table.add_column("Title")
                table.add_column("Status")
                table.add_column("Priority")
                table.add_column("Assignee")
                table.add_column("Due")
                
                for task in tasks:
                    table.add_row(
                        task.get("title", "")[:30],
                        task.get("status", ""),
                        task.get("priority", ""),
                        task.get("assignee", ""),
                        task.get("due_date", ""),
                    )
                
                console.print(table)
                
            # Workspace stats
            stats = data.get("stats", {})
            console.print(f"\n📊 Statistics:")
            console.print(f"  Total Tasks: {stats.get('total_tasks', 0)}")
            console.print(f"  Completed: {stats.get('completed_tasks', 0)}")
            console.print(f"  In Progress: {stats.get('in_progress_tasks', 0)}")
            console.print(f"  Team Members: {stats.get('team_members', 0)}")

    _run(_action)

@app.command()
def export(
    workspace_id: str = typer.Argument(..., help="Workspace ID"),
    output_file: Path = typer.Argument(..., help="Output file"),
    format: str = typer.Option("json", "--format", "-f", help="Export format: json|csv|xlsx"),
    include_comments: bool = typer.Option(False, "--comments", "-c", help="Include comments"),
) -> None:
    """Export workspace data."""
    settings = get_settings()

    async def _action():
        params = {
            "format": format,
            "include_comments": include_comments
        }
        
        async with client() as c:
            resp = await c.get(f"{settings.collab_api}/v1/workspaces/{workspace_id}/export", params=params)
            resp.raise_for_status()
            
            if format == "json":
                data = resp.json()
                import json
                output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            else:
                # CSV or XLSX format
                output_file.write_bytes(resp.content)
            
            # Get export stats from headers
            task_count = resp.headers.get("X-Task-Count", "Unknown")
            comment_count = resp.headers.get("X-Comment-Count", "Unknown")
            
            console.print(f"✅ Workspace data exported")
            console.print(f"File: {output_file}")
            console.print(f"Format: {format.upper()}")
            console.print(f"Tasks: {task_count}")
            console.print(f"Comments: {comment_count}")

    _run(_action)

@app.command()
def stats(
    workspace_id: Optional[str] = typer.Option(None, "--workspace", "-w", help="Workspace ID"),
    period: str = typer.Option("30d", "--period", "-p", help="Time period"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Specific user"),
) -> None:
    """Show collaboration statistics."""
    settings = get_settings()

    async def _action():
        params = {"period": period}
        if user:
            params["user"] = user
            
        endpoint = f"/v1/workspaces/{workspace_id}/stats" if workspace_id else "/v1/stats"
        
        async with client() as c:
            resp = await c.get(f"{settings.collab_api}{endpoint}", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            if workspace_id:
                console.print(f"📊 Workspace Statistics: {workspace_id} ({period})")
            else:
                console.print(f"📊 Global Collaboration Statistics ({period})")
            
            # Task statistics
            task_stats = data.get("task_stats", {})
            console.print(f"Tasks Created: {task_stats.get('created', 0)}")
            console.print(f"Tasks Completed: {task_stats.get('completed', 0)}")
            console.print(f"Average Completion Time: {task_stats.get('avg_completion_time', 0)} hours")
            
            # User activity
            if data.get("user_activity"):
                table = Table(title="User Activity")
                table.add_column("User")
                table.add_column("Tasks Created")
                table.add_column("Tasks Completed")
                table.add_column("Comments")
                
                for user_stat in data.get("user_activity", []):
                    table.add_row(
                        user_stat.get("user", ""),
                        str(user_stat.get("tasks_created", 0)),
                        str(user_stat.get("tasks_completed", 0)),
                        str(user_stat.get("comments", 0)),
                    )
                
                console.print(table)
            
            # Productivity trends
            if data.get("productivity_trends"):
                trends = data.get("productivity_trends", {})
                console.print(f"\n📈 Productivity Trends:")
                console.print(f"  Task Velocity: {trends.get('task_velocity', 0)} tasks/week")
                console.print(f"  Completion Rate: {trends.get('completion_rate', 0)}%")
                console.print(f"  Team Efficiency: {trends.get('team_efficiency', 0)}%")

    _run(_action)

@app.command()
def health() -> None:
    """Check collaboration service health."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.collab_api}/v1/health")
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🏥 Collaboration Service Health")
            console.print_json(data=data)

    _run(_action)
