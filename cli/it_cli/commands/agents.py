"""Agent execution and management commands."""
from __future__ import annotations

import asyncio
from typing import Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Agent Execution & Management")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    agent_type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by agent type"),
) -> None:
    """List available agents."""
    settings = get_settings()

    async def _action():
        params = {}
        if status:
            params["status"] = status
        if agent_type:
            params["type"] = agent_type
            
        async with client() as c:
            resp = await c.get(f"{settings.agents_api}/v1/agents", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Available Agents")
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("Type")
            table.add_column("Status")
            table.add_column("Capabilities")
            
            for agent in data.get("agents", []):
                capabilities = ", ".join(agent.get("capabilities", [])[:3])
                table.add_row(
                    agent.get("id", ""),
                    agent.get("name", ""),
                    agent.get("type", ""),
                    agent.get("status", ""),
                    capabilities,
                )
            
            console.print(table)

    _run(_action)

@app.command()
def chat(
    agent_id: str = typer.Argument(..., help="Agent ID"),
    message: str = typer.Argument(..., help="Message to send"),
    session_id: Optional[str] = typer.Option(None, "--session", "-s", help="Session ID"),
    stream: bool = typer.Option(False, "--stream", help="Stream response"),
) -> None:
    """Chat with an agent."""
    settings = get_settings()

    async def _action():
        payload = {
            "message": message,
            "agent_id": agent_id
        }
        if session_id:
            payload["session_id"] = session_id
            
        async with client() as c:
            resp = await c.post(
                f"{settings.agents_api}/v1/agents/chat",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🤖 Agent: {agent_id}")
            console.print(f"💬 Response: {data.get('response', '')}")
            
            if data.get("session_id"):
                console.print(f"📱 Session: {data.get('session_id')}")
            
            # Show execution steps if available
            if data.get("execution_steps"):
                table = Table(title="Execution Steps")
                table.add_column("Step")
                table.add_column("Tool")
                table.add_column("Status")
                table.add_column("Result")
                
                for step in data.get("execution_steps", []):
                    table.add_row(
                        str(step.get("step", "")),
                        step.get("tool", ""),
                        step.get("status", ""),
                        step.get("result", "")[:50] + "...",
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def invoke(
    agent_id: str = typer.Argument(..., help="Agent ID"),
    task: str = typer.Argument(..., help="Task description"),
    tools: List[str] = typer.Option([], "--tool", "-t", help="Available tools"),
    params: List[str] = typer.Option([], "--param", "-p", help="Parameters key=value"),
) -> None:
    """Invoke agent with specific task."""
    settings = get_settings()

    # Parse parameters
    param_dict = {}
    for item in params:
        if "=" not in item:
            console.print(f"❌ Invalid parameter format: {item}")
            continue
        key, value = item.split("=", 1)
        param_dict[key.strip()] = value.strip()

    async def _action():
        payload = {
            "agent_id": agent_id,
            "task": task,
            "tools": tools,
            "parameters": param_dict
        }
        
        async with client() as c:
            resp = await c.post(
                f"{settings.agents_api}/v1/agents/invoke",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🎯 Task: {task}")
            console.print(f"🤖 Agent: {agent_id}")
            console.print(f"📊 Result: {data.get('result', '')}")
            console.print(f"⏱️  Execution Time: {data.get('execution_time', 0)}s")
            
            # Show tool usage
            if data.get("tools_used"):
                table = Table(title="Tools Used")
                table.add_column("Tool")
                table.add_column("Input")
                table.add_column("Output")
                table.add_column("Duration")
                
                for tool in data.get("tools_used", []):
                    table.add_row(
                        tool.get("name", ""),
                        str(tool.get("input", ""))[:30] + "...",
                        str(tool.get("output", ""))[:30] + "...",
                        f"{tool.get('duration', 0)}s",
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def execute(
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    input_data: Optional[str] = typer.Option(None, "--input", "-i", help="Input data (JSON)"),
) -> None:
    """Execute an agent workflow."""
    settings = get_settings()

    async def _action():
        payload = {"workflow_id": workflow_id}
        if input_data:
            import json
            try:
                payload["input"] = json.loads(input_data)
            except json.JSONDecodeError:
                console.print("❌ Invalid JSON input data")
                return
        
        async with client() as c:
            resp = await c.post(
                f"{settings.agents_api}/v1/agents/execute",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🔄 Workflow: {workflow_id}")
            console.print(f"📋 Status: {data.get('status', '')}")
            console.print(f"📊 Output: {data.get('output', '')}")
            
            # Show workflow steps
            if data.get("steps"):
                table = Table(title="Workflow Steps")
                table.add_column("Step")
                table.add_column("Agent")
                table.add_column("Status")
                table.add_column("Duration")
                
                for step in data.get("steps", []):
                    table.add_row(
                        step.get("name", ""),
                        step.get("agent", ""),
                        step.get("status", ""),
                        f"{step.get('duration', 0)}s",
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def tools(
    agent_id: Optional[str] = typer.Option(None, "--agent", "-a", help="Agent ID"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Tool category"),
) -> None:
    """List available agent tools."""
    settings = get_settings()

    async def _action():
        params = {}
        if agent_id:
            params["agent_id"] = agent_id
        if category:
            params["category"] = category
            
        async with client() as c:
            resp = await c.get(f"{settings.agents_api}/v1/agents/tools", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Available Tools")
            table.add_column("Name")
            table.add_column("Category")
            table.add_column("Description")
            table.add_column("Parameters")
            
            for tool in data.get("tools", []):
                params_str = ", ".join(tool.get("parameters", []))
                table.add_row(
                    tool.get("name", ""),
                    tool.get("category", ""),
                    tool.get("description", "")[:50] + "...",
                    params_str[:30] + "..." if len(params_str) > 30 else params_str,
                )
            
            console.print(table)

    _run(_action)

@app.command()
def workflows(
    agent_type: Optional[str] = typer.Option(None, "--type", "-t", help="Agent type"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Workflow status"),
) -> None:
    """List available workflows."""
    settings = get_settings()

    async def _action():
        params = {}
        if agent_type:
            params["type"] = agent_type
        if status:
            params["status"] = status
            
        async with client() as c:
            resp = await c.get(f"{settings.agents_api}/v1/agents/workflows", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Available Workflows")
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("Type")
            table.add_column("Steps")
            table.add_column("Status")
            
            for workflow in data.get("workflows", []):
                table.add_row(
                    workflow.get("id", ""),
                    workflow.get("name", ""),
                    workflow.get("type", ""),
                    str(len(workflow.get("steps", []))),
                    workflow.get("status", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def sessions(
    agent_id: Optional[str] = typer.Option(None, "--agent", "-a", help="Agent ID"),
    active_only: bool = typer.Option(False, "--active", help="Show only active sessions"),
    limit: int = typer.Option(20, "--limit", "-l", help="Results limit"),
) -> None:
    """List agent conversation sessions."""
    settings = get_settings()

    async def _action():
        params = {"limit": limit}
        if agent_id:
            params["agent_id"] = agent_id
        if active_only:
            params["status"] = "active"
            
        async with client() as c:
            resp = await c.get(f"{settings.agents_api}/v1/agents/conversations", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Conversation Sessions")
            table.add_column("Session ID")
            table.add_column("Agent")
            table.add_column("Messages")
            table.add_column("Status")
            table.add_column("Created")
            
            for session in data.get("sessions", []):
                table.add_row(
                    session.get("id", "")[:8] + "...",
                    session.get("agent_id", ""),
                    str(session.get("message_count", 0)),
                    session.get("status", ""),
                    session.get("created_at", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def health(
    agent_id: Optional[str] = typer.Option(None, "--agent", "-a", help="Specific agent ID"),
) -> None:
    """Check agent health status."""
    settings = get_settings()

    async def _action():
        if agent_id:
            # Check specific agent health
            async with client() as c:
                resp = await c.get(f"{settings.agents_api}/v1/agents/{agent_id}/health")
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🔍 Agent Health: {agent_id}")
                console.print(f"Status: {data.get('status', 'Unknown')}")
                console.print(f"Uptime: {data.get('uptime', 0)}s")
                console.print(f"Memory Usage: {data.get('memory_usage', 0)}MB")
                console.print(f"Active Sessions: {data.get('active_sessions', 0)}")
        else:
            # Check overall agent service health
            async with client() as c:
                resp = await c.get(f"{settings.agents_api}/healthz")
                resp.raise_for_status()
                data = resp.json()
                
                console.print("🏥 Agent Service Health")
                console.print_json(data=data)

    _run(_action)
