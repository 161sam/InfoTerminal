"""Operations and system management commands."""
from __future__ import annotations

import asyncio
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Operations & System Management")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def stacks(
    action: str = typer.Argument(..., help="Action: list|start|stop|restart|status"),
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Specific stack name"),
    services: List[str] = typer.Option([], "--service", help="Specific services"),
) -> None:
    """Manage Docker Compose stacks."""
    settings = get_settings()

    async def _action():
        if action == "list":
            # List available stacks
            async with client() as c:
                resp = await c.get(f"{settings.ops_api}/v1/stacks")
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Docker Compose Stacks")
                table.add_column("Name")
                table.add_column("Status")
                table.add_column("Services")
                table.add_column("Last Updated")
                
                for stack_info in data.get("stacks", []):
                    services_count = len(stack_info.get("services", []))
                    table.add_row(
                        stack_info.get("name", ""),
                        stack_info.get("status", ""),
                        str(services_count),
                        stack_info.get("last_updated", ""),
                    )
                
                console.print(table)
        else:
            # Execute stack action
            payload = {"action": action}
            if stack:
                payload["stack"] = stack
            if services:
                payload["services"] = services
                
            async with client() as c:
                resp = await c.post(f"{settings.ops_api}/v1/stacks", json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🔧 Stack Action: {action}")
                console.print(f"Status: {data.get('status', 'Unknown')}")
                console.print(f"Message: {data.get('message', '')}")
                
                if data.get("services"):
                    table = Table(title="Service Status")
                    table.add_column("Service")
                    table.add_column("Status")
                    table.add_column("Health")
                    
                    for service in data.get("services", []):
                        table.add_row(
                            service.get("name", ""),
                            service.get("status", ""),
                            service.get("health", ""),
                        )
                    
                    console.print(table)

    _run(_action)

@app.command()
def scale(
    service: str = typer.Argument(..., help="Service name"),
    replicas: int = typer.Argument(..., help="Number of replicas"),
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Stack name"),
) -> None:
    """Scale service replicas."""
    settings = get_settings()

    async def _action():
        payload = {
            "service": service,
            "replicas": replicas
        }
        if stack:
            payload["stack"] = stack
            
        async with client() as c:
            resp = await c.post(f"{settings.ops_api}/v1/stacks/scale", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📈 Scaling: {service} → {replicas} replicas")
            console.print(f"Status: {data.get('status', 'Unknown')}")
            console.print(f"Current Replicas: {data.get('current_replicas', 0)}")

    _run(_action)

@app.command()
def logs(
    service: str = typer.Argument(..., help="Service name"),
    lines: int = typer.Option(100, "--lines", "-n", help="Number of lines"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Stack name"),
) -> None:
    """Stream service logs."""
    settings = get_settings()

    async def _action():
        params = {
            "service": service,
            "lines": lines,
            "follow": follow
        }
        if stack:
            params["stack"] = stack
            
        async with client() as c:
            resp = await c.get(f"{settings.ops_api}/v1/stacks/logs", params=params)
            resp.raise_for_status()
            
            if follow:
                # Stream logs
                async for line in resp.aiter_lines():
                    console.print(line)
            else:
                # Print all logs
                data = resp.json()
                logs = data.get("logs", [])
                for log_line in logs:
                    console.print(log_line)

    _run(_action)

@app.command()
def security(
    action: str = typer.Argument(..., help="Action: start|stop|status|wipe"),
    level: Optional[str] = typer.Option(None, "--level", "-l", help="Security level: basic|enhanced|paranoid"),
) -> None:
    """Manage security/incognito mode."""
    settings = get_settings()

    async def _action():
        if action == "status":
            # Get security status
            async with client() as c:
                resp = await c.get(f"{settings.ops_api}/v1/security/incognito/status")
                resp.raise_for_status()
                data = resp.json()
                
                console.print("🛡️  Security Status")
                console.print(f"Mode: {data.get('mode', 'Unknown')}")
                console.print(f"Level: {data.get('level', 'Unknown')}")
                console.print(f"Active: {'✅' if data.get('active', False) else '❌'}")
                console.print(f"Data Wiped: {'✅' if data.get('data_wiped', False) else '❌'}")
        else:
            # Execute security action
            payload = {"action": action}
            if level:
                payload["level"] = level
                
            async with client() as c:
                resp = await c.post(f"{settings.ops_api}/v1/security/incognito", json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🛡️  Security Action: {action}")
                console.print(f"Status: {data.get('status', 'Unknown')}")
                console.print(f"Message: {data.get('message', '')}")
                
                if data.get("warnings"):
                    console.print("⚠️  Warnings:")
                    for warning in data.get("warnings", []):
                        console.print(f"  - {warning}")

    _run(_action)

@app.command()
def health(
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Specific component"),
    comprehensive: bool = typer.Option(False, "--comprehensive", help="Comprehensive health check"),
) -> None:
    """Check system health."""
    settings = get_settings()

    async def _action():
        if comprehensive:
            endpoint = "/v1/health/comprehensive"
        else:
            endpoint = "/healthz"
            
        params = {}
        if component:
            params["component"] = component
            
        async with client() as c:
            resp = await c.get(f"{settings.ops_api}{endpoint}", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            if comprehensive:
                console.print("🏥 Comprehensive Health Check")
                
                table = Table(title="Component Health")
                table.add_column("Component")
                table.add_column("Status")
                table.add_column("Response Time")
                table.add_column("Details")
                
                for comp in data.get("components", []):
                    status_icon = "✅" if comp.get("healthy", False) else "❌"
                    table.add_row(
                        comp.get("name", ""),
                        status_icon,
                        f"{comp.get('response_time', 0)}ms",
                        comp.get("details", ""),
                    )
                
                console.print(table)
                
                # Overall status
                overall = data.get("overall", {})
                console.print(f"\n📊 Overall: {'✅ Healthy' if overall.get('healthy', False) else '❌ Unhealthy'}")
                console.print(f"Total Components: {overall.get('total_components', 0)}")
                console.print(f"Healthy: {overall.get('healthy_components', 0)}")
            else:
                console.print("🏥 Basic Health Check")
                console.print_json(data=data)

    _run(_action)

@app.command()
def performance(
    metric: Optional[str] = typer.Option(None, "--metric", "-m", help="Specific metric"),
    duration: str = typer.Option("1h", "--duration", "-d", help="Time duration"),
) -> None:
    """Show performance metrics."""
    settings = get_settings()

    async def _action():
        params = {"duration": duration}
        if metric:
            params["metric"] = metric
            
        async with client() as c:
            resp = await c.get(f"{settings.ops_api}/v1/performance", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Performance Metrics ({duration})")
            table.add_column("Metric")
            table.add_column("Current")
            table.add_column("Average")
            table.add_column("Peak")
            table.add_column("Status")
            
            for metric_data in data.get("metrics", []):
                status_icon = "✅" if metric_data.get("status") == "healthy" else "⚠️"
                table.add_row(
                    metric_data.get("name", ""),
                    str(metric_data.get("current", 0)),
                    str(metric_data.get("average", 0)),
                    str(metric_data.get("peak", 0)),
                    status_icon,
                )
            
            console.print(table)

    _run(_action)

@app.command()
def reload(
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Specific component"),
    config_file: Optional[str] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Reload system configuration."""
    settings = get_settings()

    async def _action():
        payload = {}
        if component:
            payload["component"] = component
        if config_file:
            payload["config_file"] = config_file
            
        async with client() as c:
            resp = await c.post(f"{settings.ops_api}/v1/ops/reload-config", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🔄 Configuration Reload")
            console.print(f"Status: {data.get('status', 'Unknown')}")
            console.print(f"Message: {data.get('message', '')}")
            
            if data.get("reloaded_components"):
                console.print("Reloaded:")
                for comp in data.get("reloaded_components", []):
                    console.print(f"  ✅ {comp}")
                    
            if data.get("errors"):
                console.print("Errors:")
                for error in data.get("errors", []):
                    console.print(f"  ❌ {error}")

    _run(_action)

@app.command()
def emergency(
    action: str = typer.Argument(..., help="Emergency action: shutdown|restart|lockdown"),
    confirm: bool = typer.Option(False, "--confirm", "-y", help="Confirm emergency action"),
) -> None:
    """Execute emergency operations."""
    if not confirm:
        console.print("❌ Emergency actions require --confirm flag")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        payload = {"action": action, "confirmed": True}
        
        async with client() as c:
            resp = await c.post(f"{settings.ops_api}/v1/ops/emergency", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🚨 Emergency Action: {action}")
            console.print(f"Status: {data.get('status', 'Unknown')}")
            console.print(f"Message: {data.get('message', '')}")

    _run(_action)

@app.command()
def backup(
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Specific component"),
    destination: Optional[str] = typer.Option(None, "--dest", "-d", help="Backup destination"),
) -> None:
    """Create system backup."""
    settings = get_settings()

    async def _action():
        payload = {}
        if component:
            payload["component"] = component
        if destination:
            payload["destination"] = destination
            
        async with client() as c:
            resp = await c.post(f"{settings.ops_api}/v1/ops/backup", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("💾 System Backup")
            console.print(f"Status: {data.get('status', 'Unknown')}")
            console.print(f"Backup Path: {data.get('backup_path', '')}")
            console.print(f"Size: {data.get('backup_size', 0)} bytes")

    _run(_action)

@app.command()
def status() -> None:
    """Show overall system status."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.ops_api}/v1/ops/status")
            resp.raise_for_status()
            data = resp.json()
            
            console.print("📊 System Status")
            console.print_json(data=data)

    _run(_action)
