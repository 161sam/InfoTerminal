"""Infrastructure related commands."""
from __future__ import annotations

import asyncio

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer()
console = Console()


@app.command()
def health() -> None:
    """Check health of core services."""
    settings = get_settings()
    checks = {
        "search-api": f"{settings.search_api}/healthz",
        "graph-api": f"{settings.graph_api}/healthz",
        "views-api": f"{settings.views_api}/healthz",
    }
    table = Table(title="Service Health", show_lines=True)
    table.add_column("Service")
    table.add_column("Status")

    async def _check():
        async with client() as c:
            for name, url in checks.items():
                try:
                    r = await c.get(url)
                    ok = "OK" if r.status_code == 200 else str(r.status_code)
                except Exception as exc:  # pragma: no cover - network
                    ok = f"DOWN ({type(exc).__name__})"
                table.add_row(name, ok)

    asyncio.run(_check())
    console.print(table)
