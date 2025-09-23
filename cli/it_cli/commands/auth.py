"""Authentication commands."""
from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Authentication & User Management")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def login(
    username: str = typer.Option(..., "--username", "-u", help="Username"),
    password: str = typer.Option(..., "--password", "-p", help="Password", hide_input=True),
    remember: bool = typer.Option(False, "--remember", "-r", help="Remember login"),
) -> None:
    """Login to InfoTerminal."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.auth_api}/v1/auth/login",
                json={
                    "username": username,
                    "password": password,
                    "remember_me": remember,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            console.print("✅ Login successful")
            console.print_json(data=data)

    _run(_action)

@app.command()
def whoami() -> None:
    """Show current user information."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.auth_api}/v1/auth/me")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Current User")
            table.add_column("Field")
            table.add_column("Value")
            
            user = data.get("user", {})
            table.add_row("Username", user.get("username", ""))
            table.add_row("Email", user.get("email", ""))
            table.add_row("Role", user.get("role", ""))
            table.add_row("Status", user.get("status", ""))
            table.add_row("Last Login", user.get("last_login", ""))
            
            console.print(table)

    _run(_action)

@app.command()
def logout() -> None:
    """Logout from InfoTerminal."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.post(f"{settings.auth_api}/v1/auth/logout")
            resp.raise_for_status()
            console.print("✅ Logout successful")

    _run(_action)

@app.command()
def token(
    name: str = typer.Option(..., "--name", "-n", help="Token name"),
    expires_days: Optional[int] = typer.Option(None, "--expires", "-e", help="Expiration in days"),
) -> None:
    """Generate API token."""
    settings = get_settings()

    async def _action():
        payload = {"name": name}
        if expires_days:
            payload["expires_in_days"] = expires_days
            
        async with client() as c:
            resp = await c.post(f"{settings.auth_api}/v1/auth/tokens", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("✅ Token created")
            console.print(f"Token: {data.get('token')}")
            console.print(f"Expires: {data.get('expires_at')}")

    _run(_action)

@app.command()
def users(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Filter by role"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    limit: int = typer.Option(50, "--limit", "-l", help="Results limit"),
) -> None:
    """List users."""
    settings = get_settings()

    async def _action():
        params = {"limit": limit}
        if role:
            params["role"] = role
        if status:
            params["status"] = status
            
        async with client() as c:
            resp = await c.get(f"{settings.auth_api}/v1/users", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Users ({data.get('total', 0)})")
            table.add_column("Username")
            table.add_column("Email")
            table.add_column("Role")
            table.add_column("Status")
            table.add_column("Last Login")
            
            for user in data.get("items", []):
                table.add_row(
                    user.get("username", ""),
                    user.get("email", ""),
                    user.get("role", ""),
                    user.get("status", ""),
                    user.get("last_login", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def roles() -> None:
    """List available roles."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.auth_api}/v1/roles")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Available Roles")
            table.add_column("Name")
            table.add_column("Description")
            table.add_column("Permissions")
            
            for role in data.get("items", []):
                permissions = ", ".join(role.get("permissions", []))
                table.add_row(
                    role.get("name", ""),
                    role.get("description", ""),
                    permissions,
                )
            
            console.print(table)

    _run(_action)
