"""Graph commands."""
from __future__ import annotations

import asyncio
from typing import List

import typer
from rich.console import Console

from ..config import get_settings
from ..http import client
from ..renderers.graphs import adjacency_tree

app = typer.Typer(help="Graph API operations")
console = Console()


def _run(action):
    asyncio.run(action())


@app.command()
def ping() -> None:
    """Ping graph-api health endpoint."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.graph_api}/healthz")
            resp.raise_for_status()
            console.print(resp.json())

    _run(_action)


def _parse_kv(pairs: List[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise typer.BadParameter(f"Expected key=value pair, got '{item}'")
        key, value = item.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


@app.command()
def cypher(
    query: str = typer.Argument(..., help="Cypher query to execute"),
    param: List[str] = typer.Option([], "--param", "-p", help="Cypher parameter key=value"),
    read_only: bool = typer.Option(True, help="Execute the query in read-only mode"),
) -> None:
    """Execute a Cypher query via `/v1/cypher`."""

    settings = get_settings()
    parameters = _parse_kv(param)

    async def _action():
        async with client() as c:
            resp = await c.post(
                f"{settings.graph_api}/v1/cypher",
                json={
                    "query": query,
                    "parameters": parameters,
                    "read_only": read_only,
                },
            )
            resp.raise_for_status()
            console.print_json(data=resp.json())

    _run(_action)


@app.command()
def neighbors(
    node_id: str = typer.Argument(..., help="Source node identifier"),
    depth: int = typer.Option(1, help="Traversal depth", min=1, max=5),
    limit: int = typer.Option(50, help="Maximum number of neighbors", min=1, max=1000),
    direction: str = typer.Option("both", help="Traversal direction", show_default=True, case_sensitive=False),
    relationship_types: str | None = typer.Option(
        None,
        help="Comma separated relationship types",
    ),
    visualize: bool = typer.Option(False, help="Render an adjacency tree"),
) -> None:
    """Fetch neighbors for a node via `/v1/nodes/{id}/neighbors`."""

    direction = direction.lower()
    if direction not in {"incoming", "outgoing", "both"}:
        raise typer.BadParameter("direction must be one of incoming|outgoing|both")

    settings = get_settings()

    async def _action():
        params = {"depth": depth, "limit": limit, "direction": direction}
        if relationship_types:
            params["relationship_types"] = relationship_types

        async with client() as c:
            resp = await c.get(f"{settings.graph_api}/v1/nodes/{node_id}/neighbors", params=params)
            resp.raise_for_status()
            data = resp.json()
            console.print_json(data=data)

            if visualize and data.get("relationships"):
                adjacency: dict[str, list[str]] = {}
                for rel in data.get("relationships", []):
                    source = str(rel.get("source"))
                    target = str(rel.get("target"))
                    adjacency.setdefault(source, []).append(target)
                if adjacency:
                    adjacency_tree(adjacency)

    _run(_action)


@app.command("shortest-path")
def shortest_path(
    source: str = typer.Option(..., "--source", "-s", help="Source node id"),
    target: str = typer.Option(..., "--target", "-t", help="Target node id"),
    max_length: int = typer.Option(6, help="Maximum path length", min=1, max=16),
) -> None:
    """Compute shortest path via `/v1/shortest-path`."""

    settings = get_settings()

    async def _action():
        payload = {"source_node": source, "target_node": target, "max_length": max_length}
        async with client() as c:
            resp = await c.post(f"{settings.graph_api}/v1/shortest-path", json=payload)
            resp.raise_for_status()
            console.print_json(data=resp.json())

    _run(_action)
