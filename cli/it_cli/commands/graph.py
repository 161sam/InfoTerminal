"""Graph commands."""
from __future__ import annotations

import asyncio

import typer
from rich.console import Console

from ..config import get_settings
from ..http import client
from ..renderers.graphs import adjacency_tree

app = typer.Typer()
console = Console()


@app.command()
def ping() -> None:
    """Ping graph-api health endpoint."""
    settings = get_settings()

    async def _run():
        async with client() as c:
            r = await c.get(f"{settings.graph_api}/healthz")
            console.print(r.json())

    asyncio.run(_run())


@app.command()
def cypher(query: str, visualize: bool = False, limit: int = 50) -> None:
    """Execute a Cypher query via graph-api and optionally visualise."""
    settings = get_settings()

    async def _run():
        async with client() as c:
            try:
                r = await c.post(f"{settings.graph_api}/query", json={"cypher": query, "limit": limit})
                r.raise_for_status()
                data = r.json()
            except Exception:
                r = await c.get(f"{settings.graph_api}/nodes", params={"limit": limit})
                r.raise_for_status()
                data = r.json()
            console.print_json(data=data)
            if visualize:
                adj: dict[str, list[str]] = {}
                nodes = data.get("nodes") or []
                for n in nodes:
                    adj[n.get("id", "node")] = [
                        rel.get("target") for rel in n.get("relations", []) if rel.get("target")
                    ]
                if adj:
                    adjacency_tree(adj)

    asyncio.run(_run())
