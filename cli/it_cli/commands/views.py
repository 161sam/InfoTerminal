"""Views/SQL commands."""
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
def query(sql: str, limit: int = 20) -> None:
    """Execute a SQL query via views-api."""
    settings = get_settings()

    async def _run():
        async with client() as c:
            r = await c.post(f"{settings.views_api}/query", json={"sql": sql, "limit": limit})
            r.raise_for_status()
            data = r.json()
            rows = data.get("rows", [])
            table = Table(title=f"SQL: {len(rows)} rows")
            if rows:
                for col in rows[0].keys():
                    table.add_column(str(col))
                for row in rows:
                    table.add_row(*[str(v) for v in row.values()])
            console.print(table)

    asyncio.run(_run())
