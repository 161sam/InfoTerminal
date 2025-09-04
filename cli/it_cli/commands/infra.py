"""Infrastructure control commands."""
from __future__ import annotations

import asyncio
import os
import subprocess
import time
from collections import deque
from pathlib import Path
from typing import Iterable, List, Dict
from urllib.parse import urlparse

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client
from ..renderers.tables import status_table, log_panel

app = typer.Typer()
console = Console()

DEV_UP = Path("scripts/dev_up.sh")
DEV_DOWN = Path("scripts/dev_down.sh")

LOG_FILES: Dict[str, str] = {
    "search-api": "/tmp/it_search-api.log",
    "graph-api": "/tmp/it_graph-api.log",
    "views-api": "/tmp/it_graph-views.log",
    "frontend": "/tmp/it_frontend.log",
}

CONTAINER_MAP: Dict[str, str] = {
    "search-api": "search-api",
    "graph-api": "graph-api",
    "views-api": "graph-views",
    "frontend": "frontend",
    "gateway": "gateway",
    "agents": "flowise-connector",
    "neo4j": "neo4j",
    "opensearch": "opensearch",
    "postgres": "postgres",
}


def _tail_file(path: Path, lines: int) -> List[str]:
    with path.open() as f:
        return list(deque(f, maxlen=lines))


def _follow_file(path: Path, lines: int) -> Iterable[str]:
    for line in _tail_file(path, lines):
        yield line
    with path.open() as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(0.5)


def _display_file_logs(path: Path, lines: int, follow: bool) -> None:
    if follow:
        for line in _follow_file(path, lines):
            console.print(line, end="")
    else:
        for line in _tail_file(path, lines):
            console.print(line, end="")


def _display_docker_logs(container: str, lines: int, follow: bool) -> None:
    cmd = ["docker", "logs", "--tail", str(lines)]
    if follow:
        cmd.append("-f")
    cmd.append(container)
    subprocess.run(cmd, check=False)


async def probe_http(name: str, url: str) -> Dict[str, str]:
    start = time.perf_counter()
    status = "UNAVAILABLE"
    latency = ""
    try:
        async with client() as c:
            r = await c.get(url)
        latency = f"{(time.perf_counter()-start)*1000:.0f} ms"
        status = "UP" if r.status_code == 200 else f"DOWN ({r.status_code})"
    except Exception as exc:  # pragma: no cover - network
        status = f"DOWN ({type(exc).__name__})"
    port = urlparse(url).port or (443 if url.startswith("https") else 80)
    return {"service": name, "status": status, "port": port, "latency": latency}


async def probe_tcp(name: str, host: str, port: int) -> Dict[str, str]:
    start = time.perf_counter()
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
        latency = f"{(time.perf_counter()-start)*1000:.0f} ms"
        status = "UP"
    except Exception as exc:  # pragma: no cover - network
        latency = ""
        status = f"DOWN ({type(exc).__name__})"
    return {"service": name, "status": status, "port": port, "latency": latency}


async def gather_status() -> List[Dict[str, str]]:
    settings = get_settings()
    tasks = [
        probe_http("search-api", f"{settings.search_api}/healthz"),
        probe_http("graph-api", f"{settings.graph_api}/healthz"),
        probe_http("views-api", f"{settings.views_api}/healthz"),
        probe_http("frontend", settings.frontend_url),
        probe_tcp("gateway", "127.0.0.1", settings.gateway_port),
        probe_tcp("agents", "127.0.0.1", settings.agents_port),
        probe_tcp("neo4j", "127.0.0.1", settings.neo4j_port),
        probe_tcp("postgres", settings.pg_host, settings.pg_port),
        probe_tcp("opensearch", "127.0.0.1", settings.opensearch_port),
    ]
    return await asyncio.gather(*tasks)


@app.command()
def up(
    agents: bool = typer.Option(False, "--agents", help="Start agents connector"),
    gateway: bool = typer.Option(False, "--gateway", help="Start gateway"),
    opa_host: str | None = typer.Option(None, "--opa-host", help="OPA host"),
) -> None:
    """Start local development infrastructure."""
    cmd: List[str]
    env = os.environ.copy()
    if DEV_UP.exists():
        cmd = [str(DEV_UP)]
        if agents:
            cmd.append("--agents")
        if gateway:
            cmd.append("--gateway")
        if opa_host:
            cmd.extend(["--opa-host", opa_host])
        subprocess.run(cmd, check=False)
    else:
        services = ["opensearch", "neo4j"]
        try:
            subprocess.run(["docker", "compose", "up", "-d", *services], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            if "already exists" not in (exc.stderr or ""):
                raise
        if agents and Path("docker-compose.agents.yml").exists():
            subprocess.run(["docker", "compose", "-f", "docker-compose.agents.yml", "up", "-d"], check=False)
        if gateway and Path("docker-compose.gateway.yml").exists():
            subprocess.run(["docker", "compose", "-f", "docker-compose.gateway.yml", "up", "-d"], check=False)
    settings = get_settings()
    table = Table(title="Components started")
    table.add_column("Service")
    table.add_column("Port")
    for name, url in [
        ("search-api", settings.search_api),
        ("graph-api", settings.graph_api),
        ("views-api", settings.views_api),
        ("frontend", settings.frontend_url),
    ]:
        port = urlparse(url).port
        table.add_row(name, str(port))
    console.print(table)


@app.command()
def down(all: bool = typer.Option(False, "--all", help="Stop all services")) -> None:
    """Stop local development infrastructure."""
    if DEV_DOWN.exists():
        cmd = [str(DEV_DOWN)]
        if all:
            cmd.append("--all")
        subprocess.run(cmd, check=False)
    else:
        subprocess.run(["docker", "compose", "down", "--remove-orphans"], check=False)
        if all:
            if Path("docker-compose.agents.yml").exists():
                subprocess.run(["docker", "compose", "-f", "docker-compose.agents.yml", "down", "--remove-orphans"], check=False)
            if Path("docker-compose.gateway.yml").exists():
                subprocess.run(["docker", "compose", "-f", "docker-compose.gateway.yml", "down", "--remove-orphans"], check=False)
    console.print("Infra stopped", style="green")


@app.command()
def status() -> None:
    """Check health of services."""
    rows = asyncio.run(gather_status())
    console.print(status_table(rows))
    core = {"search-api", "graph-api", "views-api"}
    exit_code = 0 if all(r["status"] == "UP" for r in rows if r["service"] in core) else 1
    raise typer.Exit(exit_code)


@app.command()
def logs(
    service: str = typer.Option(..., "--service", help="Service name"),
    lines: int = typer.Option(200, "--lines", help="Number of lines"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Tail logs"),
) -> None:
    """Show logs for a service."""
    path = Path(LOG_FILES.get(service, ""))
    if path.is_file():
        console.print(log_panel(service))
        _display_file_logs(path, lines, follow)
        return
    container = CONTAINER_MAP.get(service)
    if container:
        console.print(log_panel(service))
        _display_docker_logs(container, lines, follow)
        return
    raise typer.BadParameter(f"Unknown service: {service}")
