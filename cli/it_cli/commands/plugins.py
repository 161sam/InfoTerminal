"""Plugin management and execution commands."""
from __future__ import annotations

import asyncio
from typing import Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Plugin Management & Execution")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
) -> None:
    """List available plugins."""
    settings = get_settings()

    async def _action():
        params = {}
        if status:
            params["status"] = status
        if category:
            params["category"] = category
            
        async with client() as c:
            resp = await c.get(f"{settings.plugins_api}/v1/plugins/registry", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Plugin Registry")
            table.add_column("Name")
            table.add_column("Version")
            table.add_column("Category")
            table.add_column("Status")
            table.add_column("Description")
            
            for plugin in data.get("plugins", []):
                table.add_row(
                    plugin.get("name", ""),
                    plugin.get("version", ""),
                    plugin.get("category", ""),
                    plugin.get("status", ""),
                    plugin.get("description", "")[:50] + "...",
                )
            
            console.print(table)

    _run(_action)

@app.command()
def enable(
    plugin_name: str = typer.Argument(..., help="Plugin name to enable"),
    config: List[str] = typer.Option([], "--config", "-c", help="Config key=value pairs"),
) -> None:
    """Enable a plugin."""
    settings = get_settings()

    # Parse config
    config_dict = {}
    for item in config:
        if "=" not in item:
            console.print(f"❌ Invalid config format: {item}")
            continue
        key, value = item.split("=", 1)
        config_dict[key.strip()] = value.strip()

    async def _action():
        payload = {"enabled": True}
        if config_dict:
            payload["config"] = config_dict
            
        async with client() as c:
            resp = await c.put(
                f"{settings.plugins_api}/v1/plugins/{plugin_name}/enable",
                json=payload
            )
            resp.raise_for_status()
            console.print(f"✅ Plugin '{plugin_name}' enabled")

    _run(_action)

@app.command()
def disable(
    plugin_name: str = typer.Argument(..., help="Plugin name to disable"),
) -> None:
    """Disable a plugin."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.put(
                f"{settings.plugins_api}/v1/plugins/{plugin_name}/enable",
                json={"enabled": False}
            )
            resp.raise_for_status()
            console.print(f"❌ Plugin '{plugin_name}' disabled")

    _run(_action)

@app.command()
def configure(
    plugin_name: str = typer.Argument(..., help="Plugin name to configure"),
    config: List[str] = typer.Option([], "--config", "-c", help="Config key=value pairs"),
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
) -> None:
    """Configure a plugin."""
    settings = get_settings()

    async def _action():
        if show:
            # Show current configuration
            async with client() as c:
                resp = await c.get(f"{settings.plugins_api}/v1/plugins/{plugin_name}/config")
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🔧 Configuration for '{plugin_name}':")
                console.print_json(data=data.get("config", {}))
        else:
            # Update configuration
            config_dict = {}
            for item in config:
                if "=" not in item:
                    console.print(f"❌ Invalid config format: {item}")
                    continue
                key, value = item.split("=", 1)
                config_dict[key.strip()] = value.strip()
            
            if not config_dict:
                console.print("❌ No configuration provided")
                return
            
            async with client() as c:
                resp = await c.put(
                    f"{settings.plugins_api}/v1/plugins/{plugin_name}/config",
                    json={"config": config_dict}
                )
                resp.raise_for_status()
                console.print(f"✅ Plugin '{plugin_name}' configured")

    _run(_action)

@app.command()
def status(
    plugin_name: Optional[str] = typer.Argument(None, help="Plugin name"),
) -> None:
    """Show plugin status."""
    settings = get_settings()

    async def _action():
        if plugin_name:
            # Show specific plugin status
            async with client() as c:
                resp = await c.get(f"{settings.plugins_api}/v1/plugins/state")
                resp.raise_for_status()
                data = resp.json()
                
                plugins = data.get("plugins", {})
                if plugin_name in plugins:
                    plugin_data = plugins[plugin_name]
                    console.print(f"🔍 Plugin Status: {plugin_name}")
                    console.print(f"Enabled: {plugin_data.get('enabled', False)}")
                    console.print(f"Status: {plugin_data.get('status', 'Unknown')}")
                    console.print(f"Last Updated: {plugin_data.get('last_updated', '')}")
                    console.print(f"Health: {plugin_data.get('health', 'Unknown')}")
                else:
                    console.print(f"❌ Plugin '{plugin_name}' not found")
        else:
            # Show all plugin statuses
            async with client() as c:
                resp = await c.get(f"{settings.plugins_api}/v1/plugins/state")
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Plugin Status")
                table.add_column("Name")
                table.add_column("Enabled")
                table.add_column("Status")
                table.add_column("Health")
                table.add_column("Last Updated")
                
                for name, plugin in data.get("plugins", {}).items():
                    table.add_row(
                        name,
                        "✅" if plugin.get("enabled", False) else "❌",
                        plugin.get("status", "Unknown"),
                        plugin.get("health", "Unknown"),
                        plugin.get("last_updated", ""),
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def tools(
    plugin_name: Optional[str] = typer.Option(None, "--plugin", "-p", help="Plugin name"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Tool category"),
) -> None:
    """List available plugin tools."""
    settings = get_settings()

    async def _action():
        params = {}
        if plugin_name:
            params["plugin"] = plugin_name
        if category:
            params["category"] = category
            
        async with client() as c:
            resp = await c.get(f"{settings.plugins_api}/v1/plugins/tools", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Plugin Tools")
            table.add_column("Plugin")
            table.add_column("Tool")
            table.add_column("Category")
            table.add_column("Description")
            table.add_column("Parameters")
            
            for tool in data.get("tools", []):
                params_list = tool.get("parameters", [])
                params_str = ", ".join([p.get("name", "") for p in params_list])
                
                table.add_row(
                    tool.get("plugin", ""),
                    tool.get("name", ""),
                    tool.get("category", ""),
                    tool.get("description", "")[:40] + "...",
                    params_str[:30] + "..." if len(params_str) > 30 else params_str,
                )
            
            console.print(table)

    _run(_action)

@app.command()
def run(
    plugin_name: str = typer.Argument(..., help="Plugin name"),
    tool_name: str = typer.Argument(..., help="Tool name"),
    params: List[str] = typer.Option([], "--param", "-p", help="Parameters key=value"),
    timeout: Optional[int] = typer.Option(None, "--timeout", "-t", help="Execution timeout"),
) -> None:
    """Execute a plugin tool."""
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
        payload = {"parameters": param_dict}
        if timeout:
            payload["timeout"] = timeout
            
        async with client() as c:
            resp = await c.post(
                f"{settings.plugins_api}/v1/plugins/invoke/{plugin_name}/{tool_name}",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🔧 Tool: {plugin_name}.{tool_name}")
            console.print(f"📊 Status: {data.get('status', 'Unknown')}")
            console.print(f"⏱️  Duration: {data.get('execution_time', 0)}s")
            console.print(f"📤 Result:")
            console.print_json(data=data.get("result", {}))
            
            # Show errors if any
            if data.get("error"):
                console.print(f"❌ Error: {data.get('error')}")

    _run(_action)

@app.command()
def health(
    plugin_name: Optional[str] = typer.Option(None, "--plugin", "-p", help="Plugin name"),
) -> None:
    """Check plugin health."""
    settings = get_settings()

    async def _action():
        if plugin_name:
            # Check specific plugin health
            async with client() as c:
                resp = await c.get(f"{settings.plugins_api}/v1/plugins/{plugin_name}/health")
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🏥 Plugin Health: {plugin_name}")
                console.print(f"Status: {data.get('status', 'Unknown')}")
                console.print(f"Health: {data.get('health', 'Unknown')}")
                console.print(f"Last Check: {data.get('last_check', '')}")
                
                if data.get("details"):
                    console.print("Details:")
                    console.print_json(data=data.get("details"))
        else:
            # Check overall plugin service health
            async with client() as c:
                resp = await c.get(f"{settings.plugins_api}/healthz")
                resp.raise_for_status()
                data = resp.json()
                
                console.print("🏥 Plugin Service Health")
                console.print_json(data=data)

    _run(_action)

@app.command()
def install(
    plugin_url: str = typer.Argument(..., help="Plugin URL or package name"),
    force: bool = typer.Option(False, "--force", "-f", help="Force installation"),
) -> None:
    """Install a new plugin."""
    settings = get_settings()

    async def _action():
        payload = {
            "source": plugin_url,
            "force": force
        }
        
        async with client() as c:
            resp = await c.post(
                f"{settings.plugins_api}/v1/plugins/install",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📦 Installing plugin from: {plugin_url}")
            console.print(f"📊 Status: {data.get('status', 'Unknown')}")
            
            if data.get("plugin_name"):
                console.print(f"✅ Installed: {data.get('plugin_name')}")

    _run(_action)

@app.command()
def uninstall(
    plugin_name: str = typer.Argument(..., help="Plugin name to uninstall"),
    force: bool = typer.Option(False, "--force", "-f", help="Force uninstallation"),
) -> None:
    """Uninstall a plugin."""
    settings = get_settings()

    async def _action():
        payload = {"force": force}
        
        async with client() as c:
            resp = await c.delete(
                f"{settings.plugins_api}/v1/plugins/{plugin_name}",
                json=payload
            )
            resp.raise_for_status()
            console.print(f"🗑️  Plugin '{plugin_name}' uninstalled")

    _run(_action)
