from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Optional

import typer
import yaml

from .utils import NaturalOrderGroup
from .utils.compose import build_compose_cmd, extend_with_services, run

app = typer.Typer(cls=NaturalOrderGroup, help="Low-level infrastructure commands")


def _parse_services(value: List[str]) -> List[str]:
    result: List[str] = []
    for item in value:
        result.extend([s.strip() for s in item.split(",") if s.strip()])
    seen = set()
    unique: List[str] = []
    for s in result:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return unique


# Common options
COMPOSE_FILE_OPT = typer.Option(None, "--compose-file", "-f", help="Compose file", show_default=False)
PROJECT_NAME_OPT = typer.Option(None, "--project-name", "-p", help="Compose project name")
ENV_FILE_OPT = typer.Option(None, "--env-file", help="Env file", show_default=False)
PROFILE_OPT = typer.Option([], "--profile", help="Compose profile", show_default=False)
SERVICES_OPT = typer.Option([], "--services", "-s", help="Target services", callback=_parse_services, show_default=False)
SERVICES_REQ_OPT = typer.Option(..., "--services", "-s", help="Target services", callback=_parse_services, show_default=False)
DRY_RUN_OPT = typer.Option(False, "--dry-run", "-n", help="Print command without executing")
VERBOSE_OPT = typer.Option(False, "--verbose", help="Show subprocess output")
QUIET_OPT = typer.Option(False, "--quiet", "-q", help="Minimal output")


# ---------------------------------------------------------------------------
# Implementation functions
# ---------------------------------------------------------------------------

def start(
    compose_file: List[Path] | None = None,
    project_name: str | None = None,
    env_file: Path | None = None,
    profile: List[str] | None = None,
    services: List[str] | None = None,
    detach: bool = False,
    retries: int = 10,
    timeout: int | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    files = [str(f) for f in compose_file] if compose_file else None
    cmd = build_compose_cmd(files=files, project=project_name, env_file=str(env_file) if env_file else None, profiles=profile)
    cmd.append("up")
    if detach:
        cmd.append("-d")
    if timeout is not None:
        cmd.extend(["--timeout", str(timeout)])
    cmd = extend_with_services(cmd, services or [])
    return run(cmd, dry_run=dry_run, verbose=verbose, quiet=quiet)


def stop(
    compose_file: List[Path] | None = None,
    project_name: str | None = None,
    env_file: Path | None = None,
    profile: List[str] | None = None,
    services: List[str] | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    files = [str(f) for f in compose_file] if compose_file else None
    cmd = build_compose_cmd(files=files, project=project_name, env_file=str(env_file) if env_file else None, profiles=profile)
    cmd.append("stop")
    cmd = extend_with_services(cmd, services or [])
    return run(cmd, dry_run=dry_run, verbose=verbose, quiet=quiet)


def restart(
    compose_file: List[Path] | None = None,
    project_name: str | None = None,
    env_file: Path | None = None,
    profile: List[str] | None = None,
    services: List[str] | None = None,
    retries: int = 10,
    timeout: int | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    files = [str(f) for f in compose_file] if compose_file else None
    cmd = build_compose_cmd(files=files, project=project_name, env_file=str(env_file) if env_file else None, profiles=profile)
    cmd.append("restart")
    if timeout is not None:
        cmd.extend(["--timeout", str(timeout)])
    cmd = extend_with_services(cmd, services or [])
    return run(cmd, dry_run=dry_run, verbose=verbose, quiet=quiet)


def rm(
    compose_file: List[Path] | None = None,
    project_name: str | None = None,
    env_file: Path | None = None,
    profile: List[str] | None = None,
    services: List[str] | None = None,
    volumes: bool = False,
    images: str = "none",
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    files = [str(f) for f in compose_file] if compose_file else None
    cmd = build_compose_cmd(files=files, project=project_name, env_file=str(env_file) if env_file else None, profiles=profile)
    cmd.extend(["down", "--remove-orphans"])
    if volumes:
        cmd.append("-v")
    if images != "none":
        cmd.extend(["--rmi", images])
    cmd = extend_with_services(cmd, services or [])
    return run(cmd, dry_run=dry_run, verbose=verbose, quiet=quiet)


def status(
    compose_file: List[Path] | None = None,
    project_name: str | None = None,
    env_file: Path | None = None,
    profile: List[str] | None = None,
    services: List[str] | None = None,
    format: str = "table",
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    files = [str(f) for f in compose_file] if compose_file else None
    cmd = build_compose_cmd(files=files, project=project_name, env_file=str(env_file) if env_file else None, profiles=profile)
    cmd.append("ps")
    if format in ("json", "yaml"):
        cmd.extend(["--format", "json"])
    elif format == "text":
        cmd.extend(["--format", "plain"])
    cmd = extend_with_services(cmd, services or [])
    if dry_run:
        return run(cmd, dry_run=True, verbose=verbose, quiet=quiet)
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True)
    if format == "yaml":
        data = json.loads(result.stdout or "[]")
        out = yaml.safe_dump(data)
    else:
        out = result.stdout
    if not quiet and out:
        print(out.strip())
    return result.returncode


def logs(
    compose_file: List[Path] | None = None,
    project_name: str | None = None,
    env_file: Path | None = None,
    profile: List[str] | None = None,
    services: List[str] | None = None,
    follow: bool = False,
    lines: int = 200,
    format: str = "plain",
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    if not services:
        raise typer.BadParameter("logs requires at least one service (--services)")
    files = [str(f) for f in compose_file] if compose_file else None
    cmd = build_compose_cmd(files=files, project=project_name, env_file=str(env_file) if env_file else None, profiles=profile)
    cmd.append("logs")
    if lines:
        cmd.extend(["--tail", str(lines)])
    if follow:
        cmd.append("-f")
    cmd = extend_with_services(cmd, services)
    if format == "plain" or dry_run:
        return run(cmd, dry_run=dry_run, verbose=verbose, quiet=quiet)
    import subprocess
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout or []:
        line = line.rstrip()
        if "|" in line:
            svc, msg = line.split("|", 1)
            data = {"service": svc.strip(), "line": msg.strip()}
        else:
            data = {"service": "", "line": line}
        print(json.dumps(data))
    return proc.wait()


# ---------------------------------------------------------------------------
# Typer command wrappers for infra namespace
# ---------------------------------------------------------------------------

@app.command()
def start_cmd(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: str | None = PROJECT_NAME_OPT,
    env_file: Path | None = ENV_FILE_OPT,
    profile: List[str] = PROFILE_OPT,
    services: List[str] = SERVICES_OPT,
    detach: bool = typer.Option(False, "--detach", "-d"),
    retries: int = typer.Option(10, "--retries"),
    timeout: int | None = typer.Option(None, "--timeout"),
    dry_run: bool = DRY_RUN_OPT,
    verbose: bool = VERBOSE_OPT,
    quiet: bool = QUIET_OPT,
) -> None:
    raise typer.Exit(start(compose_file, project_name, env_file, profile, services, detach, retries, timeout, dry_run, verbose, quiet))


@app.command()
def stop_cmd(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: str | None = PROJECT_NAME_OPT,
    env_file: Path | None = ENV_FILE_OPT,
    profile: List[str] = PROFILE_OPT,
    services: List[str] = SERVICES_OPT,
    dry_run: bool = DRY_RUN_OPT,
    verbose: bool = VERBOSE_OPT,
    quiet: bool = QUIET_OPT,
) -> None:
    raise typer.Exit(stop(compose_file, project_name, env_file, profile, services, dry_run, verbose, quiet))


@app.command()
def restart_cmd(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: str | None = PROJECT_NAME_OPT,
    env_file: Path | None = ENV_FILE_OPT,
    profile: List[str] = PROFILE_OPT,
    services: List[str] = SERVICES_OPT,
    retries: int = typer.Option(10, "--retries"),
    timeout: int | None = typer.Option(None, "--timeout"),
    dry_run: bool = DRY_RUN_OPT,
    verbose: bool = VERBOSE_OPT,
    quiet: bool = QUIET_OPT,
) -> None:
    raise typer.Exit(restart(compose_file, project_name, env_file, profile, services, retries, timeout, dry_run, verbose, quiet))


@app.command()
def rm_cmd(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: str | None = PROJECT_NAME_OPT,
    env_file: Path | None = ENV_FILE_OPT,
    profile: List[str] = PROFILE_OPT,
    services: List[str] = SERVICES_OPT,
    volumes: bool = typer.Option(False, "--volumes", "-v"),
    images: str = typer.Option("none", "--images", help="[all|local|none]"),
    dry_run: bool = DRY_RUN_OPT,
    verbose: bool = VERBOSE_OPT,
    quiet: bool = QUIET_OPT,
) -> None:
    raise typer.Exit(rm(compose_file, project_name, env_file, profile, services, volumes, images, dry_run, verbose, quiet))


@app.command()
def status_cmd(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: str | None = PROJECT_NAME_OPT,
    env_file: Path | None = ENV_FILE_OPT,
    profile: List[str] = PROFILE_OPT,
    services: List[str] = SERVICES_OPT,
    format: str = typer.Option("table", "--format", help="[table|text|json|yaml]"),
    dry_run: bool = DRY_RUN_OPT,
    verbose: bool = VERBOSE_OPT,
    quiet: bool = QUIET_OPT,
) -> None:
    raise typer.Exit(status(compose_file, project_name, env_file, profile, services, format, dry_run, verbose, quiet))


@app.command()
def logs_cmd(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: str | None = PROJECT_NAME_OPT,
    env_file: Path | None = ENV_FILE_OPT,
    profile: List[str] = PROFILE_OPT,
    services: List[str] = SERVICES_OPT,
    follow: bool = typer.Option(False, "--follow", "-F"),
    lines: int = typer.Option(200, "--lines"),
    format: str = typer.Option("plain", "--format", help="[plain|jsonl]"),
    dry_run: bool = DRY_RUN_OPT,
    verbose: bool = VERBOSE_OPT,
    quiet: bool = QUIET_OPT,
) -> None:
    raise typer.Exit(logs(compose_file, project_name, env_file, profile, services, follow, lines, format, dry_run, verbose, quiet))
