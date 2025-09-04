"""Infrastructure control commands."""
from __future__ import annotations

import asyncio
import os
import subprocess
import time
from collections import deque
from pathlib import Path
from typing import Iterable, List, Dict, Optional
from urllib.parse import urlparse

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client
from ..renderers.tables import status_table, log_panel
from ..utils import NaturalOrderGroup

app = typer.Typer(cls=NaturalOrderGroup)
console = Console(no_color=bool(os.environ.get("NO_COLOR")))

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


def _services_callback(ctx: typer.Context, param: typer.CallbackParam, value: List[str] | None) -> List[str] | None:
    if not value:
        return value
    result: List[str] = []
    for item in value:
        result.extend([v.strip() for v in item.split(",") if v.strip()])
    return result


COMPOSE_FILE_OPTION = typer.Option(None, "--compose-file", "-f", help="Compose file")
PROJECT_NAME_OPTION = typer.Option(None, "--project-name", "-p", help="Compose project")
ENV_FILE_OPTION = typer.Option(None, "--env-file", help="Env file")
PROFILE_OPTION = typer.Option(None, "--profile", help="Compose profile")
SERVICES_OPTION = typer.Option([], "--services", "-s", help="Limit to services", callback=_services_callback)
SERVICES_REQUIRED_OPTION = typer.Option(..., "--services", "-s", help="Service names", min=1, callback=_services_callback)
DETACH_OPTION = typer.Option(False, "--detach", "-d", help="Detached")
RETRIES_OPTION = typer.Option(1, "--retries", help="Status retries")
TIMEOUT_OPTION = typer.Option(5, "--timeout", help="Retry timeout")
DRY_RUN_OPTION = typer.Option(False, "--dry-run", "-n", help="Print commands")
VERBOSE_OPTION = typer.Option(False, "--verbose", "-v", help="Verbose output")
QUIET_OPTION = typer.Option(False, "--quiet", "-q", help="Quiet output")
VOLUMES_OPTION = typer.Option(False, "--volumes", "-v", help="Remove volumes")
IMAGES_OPTION = typer.Option("none", "--images", help="Remove images")


def _parse_list(value: Optional[str]) -> List[str]:
    """Parse comma/colon separated env var into a list."""
    if not value:
        return []
    sep = ":" if ":" in value else ","
    return [v.strip() for v in value.split(sep) if v.strip()]


def resolve_compose_files(files: List[Path] | None) -> List[str]:
    """Resolve compose files from CLI, env or auto-discovery."""
    if files:
        return [str(f) for f in files]
    env_val = os.environ.get("IT_COMPOSE_FILE")
    if env_val:
        return _parse_list(env_val)
    auto = [f for f in ["docker-compose.yml", "compose.yml"] if Path(f).exists()]
    return auto


def resolve_project_name(name: Optional[str]) -> str:
    """Resolve project name from CLI or env."""
    if name:
        return name
    return os.environ.get("IT_PROJECT_NAME", "infoterminal")


def resolve_env_files(files: List[Path] | None) -> List[str]:
    env_val = os.environ.get("IT_ENV_FILES")
    paths = _parse_list(env_val)
    if files:
        paths.extend(str(f) for f in files)
    return paths


def resolve_profiles(profiles: List[str] | None) -> List[str]:
    env_val = os.environ.get("IT_PROFILE")
    result = _parse_list(env_val)
    if profiles:
        result.extend(profiles)
    return result


def load_env_files(files: List[str]) -> dict:
    env = os.environ.copy()
    for f in files:
        path = Path(f)
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def compose_cmd(base: List[str], compose_files: List[str], project: str, profiles: List[str]) -> List[str]:
    cmd = ["docker", "compose"]
    for f in compose_files:
        cmd += ["-f", f]
    if project:
        cmd += ["-p", project]
    for prof in profiles:
        cmd += ["--profile", prof]
    cmd += base
    return cmd


def execute(cmd: List[str], env: dict | None, dry_run: bool, verbose: bool, quiet: bool, **kwargs):
    if dry_run:
        console.print("DRY RUN: " + " ".join(cmd))
        return subprocess.CompletedProcess(cmd, 0)
    if verbose and not quiet:
        console.print(" ".join(cmd))
    return subprocess.run(cmd, env=env, **kwargs)


def _warn_deprecated(replacement: str) -> None:
    if os.environ.get("IT_CLI_SILENCE_DEPRECATIONS") == "1":
        return
    typer.echo(f"Deprecated, use '{replacement}'", err=True)


@app.callback()
def main(no_color: bool = typer.Option(False, "--no-color", help="Disable color output")) -> None:
    if no_color:
        console.no_color = True


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


def show_logs(service: str, lines: int = 200, follow: bool = False) -> None:
    """Display logs for *service* from file or docker container.

    Parameters are plain ``int``/``bool`` values to allow reuse outside Typer
    commands.
    """
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
    raise FileNotFoundError(service)


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


def start(
    agents: bool = typer.Option(False, "--agents", help="Start agents connector"),
    gateway: bool = typer.Option(False, "--gateway", help="Start gateway"),
    opa_host: str | None = typer.Option(None, "--opa-host", help="OPA host"),
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    services: List[str] = SERVICES_OPTION,
    detach: bool = DETACH_OPTION,
    retries: int = RETRIES_OPTION,
    timeout: int = TIMEOUT_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = VERBOSE_OPTION,
    quiet: bool = QUIET_OPTION,
) -> None:
    """Start local development infrastructure."""
    compose_files = resolve_compose_files(compose_file)
    project = resolve_project_name(project_name)
    env_files = resolve_env_files(env_file)
    profiles = resolve_profiles(profile)
    env = load_env_files(env_files)
    run_env = env
    cmd: List[str]
    if DEV_UP.exists():
        cmd = [str(DEV_UP)]
        if agents:
            cmd.append("--agents")
        if gateway:
            cmd.append("--gateway")
        if opa_host:
            cmd.extend(["--opa-host", opa_host])
        if detach:
            cmd.append("-d")
        execute(cmd, run_env, dry_run, verbose, quiet)
    else:
        base_services = services if services else ["opensearch", "neo4j", "postgres"]
        cmd = compose_cmd(["up"] + (["-d"] if detach else []) + base_services, compose_files, project, profiles)
        try:
            execute(cmd, run_env, dry_run, verbose, quiet, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            if "already exists" not in (exc.stderr or ""):
                raise
            if not project_name:
                console.print("Network exists; consider -p to use a different project", style="yellow")
        if agents and Path("docker-compose.agents.yml").exists():
            acmd = ["up"] + (["-d"] if detach else [])
            execute(compose_cmd(acmd, ["docker-compose.agents.yml"], project, profiles), run_env, dry_run, verbose, quiet)
        if gateway and Path("docker-compose.gateway.yml").exists():
            gcmd = ["up"] + (["-d"] if detach else [])
            execute(compose_cmd(gcmd, ["docker-compose.gateway.yml"], project, profiles), run_env, dry_run, verbose, quiet)

    for _ in range(retries):
        rows = asyncio.run(gather_status())
        if all(r["status"].startswith("UP") for r in rows):
            break
        time.sleep(timeout)
    console.print(status_table(rows))


def stop(
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    services: List[str] = SERVICES_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = VERBOSE_OPTION,
    quiet: bool = QUIET_OPTION,
) -> None:
    """laufende Services anhalten"""
    compose_files = resolve_compose_files(compose_file)
    project = resolve_project_name(project_name)
    env_files = resolve_env_files(env_file)
    profiles = resolve_profiles(profile)
    run_env = load_env_files(env_files)
    base = ["stop"] + (services if services else [])
    execute(compose_cmd(base, compose_files, project, profiles), run_env, dry_run, verbose, quiet)
    if not quiet:
        console.print("Services stopped", style="green")


def rm(
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    services: List[str] = SERVICES_OPTION,
    volumes: bool = VOLUMES_OPTION,
    images: str = IMAGES_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = typer.Option(False, "--verbose", help="Verbose output"),
    quiet: bool = QUIET_OPTION,
) -> None:
    """Umgebung entfernen"""
    compose_files = resolve_compose_files(compose_file)
    project = resolve_project_name(project_name)
    env_files = resolve_env_files(env_file)
    profiles = resolve_profiles(profile)
    run_env = load_env_files(env_files)
    base = ["down", "--remove-orphans"] + (services if services else [])
    if volumes:
        base.append("-v")
    if images != "none":
        base.extend(["--rmi", images])
    execute(compose_cmd(base, compose_files, project, profiles), run_env, dry_run, verbose, quiet)
    if not quiet:
        console.print("Infra removed", style="green")


def status(
    services: List[str] = SERVICES_OPTION,
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    retries: int = RETRIES_OPTION,
    timeout: int = TIMEOUT_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = VERBOSE_OPTION,
    quiet: bool = QUIET_OPTION,
) -> None:
    """Check health of services."""
    _ = resolve_compose_files(compose_file)
    _ = resolve_project_name(project_name)
    _ = resolve_env_files(env_file)
    _ = resolve_profiles(profile)
    rows: List[Dict[str, str]] = []
    for _ in range(retries):
        rows = asyncio.run(gather_status())
        if all(r["status"].startswith("UP") for r in rows):
            break
        time.sleep(timeout)
    if services:
        rows = [r for r in rows if r["service"] in services]
    console.print(status_table(rows))
    exit_code = 1 if any(r["status"].startswith("DOWN") for r in rows) else 0
    raise typer.Exit(exit_code)


def logs(
    services: List[str] = SERVICES_REQUIRED_OPTION,
    lines: int = typer.Option(200, "--lines", help="Number of lines"),
    follow: bool = typer.Option(False, "--follow", "-F", help="Tail logs"),
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
) -> None:
    """Show logs for services."""
    _ = resolve_compose_files(compose_file)
    _ = resolve_project_name(project_name)
    _ = resolve_env_files(env_file)
    _ = resolve_profiles(profile)
    for service in services:
        try:
            show_logs(service, lines, follow)
        except FileNotFoundError:
            raise typer.BadParameter(f"Unknown service: {service}")


def restart(
    ctx: typer.Context,
    agents: bool = typer.Option(False, "--agents"),
    gateway: bool = typer.Option(False, "--gateway"),
    opa_host: str | None = typer.Option(None, "--opa-host"),
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    services: List[str] = SERVICES_OPTION,
    detach: bool = DETACH_OPTION,
    retries: int = RETRIES_OPTION,
    timeout: int = TIMEOUT_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = VERBOSE_OPTION,
    quiet: bool = QUIET_OPTION,
) -> None:
    """Restart infrastructure."""
    ctx.invoke(
        stop,
        compose_file=compose_file,
        project_name=project_name,
        env_file=env_file,
        profile=profile,
        services=services,
        dry_run=dry_run,
        verbose=verbose,
        quiet=quiet,
    )
    ctx.invoke(
        start,
        agents=agents,
        gateway=gateway,
        opa_host=opa_host,
        compose_file=compose_file,
        project_name=project_name,
        env_file=env_file,
        profile=profile,
        services=services,
        detach=detach,
        retries=retries,
        timeout=timeout,
        dry_run=dry_run,
        verbose=verbose,
        quiet=quiet,
    )


def up(
    ctx: typer.Context,
    agents: bool = typer.Option(False, "--agents"),
    gateway: bool = typer.Option(False, "--gateway"),
    opa_host: str | None = typer.Option(None, "--opa-host"),
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    services: List[str] = SERVICES_OPTION,
    detach: bool = DETACH_OPTION,
    retries: int = RETRIES_OPTION,
    timeout: int = TIMEOUT_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = VERBOSE_OPTION,
    quiet: bool = QUIET_OPTION,
) -> None:
    _warn_deprecated("it start")
    ctx.invoke(
        start,
        agents=agents,
        gateway=gateway,
        opa_host=opa_host,
        compose_file=compose_file,
        project_name=project_name,
        env_file=env_file,
        profile=profile,
        services=services,
        detach=detach,
        retries=retries,
        timeout=timeout,
        dry_run=dry_run,
        verbose=verbose,
        quiet=quiet,
    )


def down(
    ctx: typer.Context,
    compose_file: List[Path] = COMPOSE_FILE_OPTION,
    project_name: str | None = PROJECT_NAME_OPTION,
    env_file: List[Path] = ENV_FILE_OPTION,
    profile: List[str] = PROFILE_OPTION,
    services: List[str] = SERVICES_OPTION,
    volumes: bool = VOLUMES_OPTION,
    images: str = IMAGES_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
    verbose: bool = typer.Option(False, "--verbose", help="Verbose output"),
    quiet: bool = QUIET_OPTION,
) -> None:
    _warn_deprecated("it rm")
    ctx.invoke(
        rm,
        compose_file=compose_file,
        project_name=project_name,
        env_file=env_file,
        profile=profile,
        services=services,
        volumes=volumes,
        images=images,
        dry_run=dry_run,
        verbose=verbose,
        quiet=quiet,
    )


# register commands in desired order
app.command("up")(up)
app.command("down")(down)
app.command("status")(status)
app.command("logs")(logs)
app.command("start")(start)
app.command("stop")(stop)
app.command("restart")(restart)
app.command("halt")(stop)
