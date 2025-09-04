from pathlib import Path
from typing import List, Optional

import typer

from . import infra


def start(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: Optional[str] = infra.PROJECT_NAME_OPT,
    env_file: Optional[Path] = infra.ENV_FILE_OPT,
    profile: List[str] = infra.PROFILE_OPT,
    services: List[str] = infra.SERVICES_OPT,
    detach: bool = typer.Option(False, "--detach", "-d"),
    retries: int = typer.Option(10, "--retries"),
    timeout: Optional[int] = typer.Option(None, "--timeout"),
    dry_run: bool = infra.DRY_RUN_OPT,
    verbose: bool = infra.VERBOSE_OPT,
    quiet: bool = infra.QUIET_OPT,
) -> None:
    code = infra.start(compose_file, project_name, env_file, profile, services, detach, retries, timeout, dry_run, verbose, quiet)
    raise typer.Exit(code)


def stop(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: Optional[str] = infra.PROJECT_NAME_OPT,
    env_file: Optional[Path] = infra.ENV_FILE_OPT,
    profile: List[str] = infra.PROFILE_OPT,
    services: List[str] = infra.SERVICES_OPT,
    dry_run: bool = infra.DRY_RUN_OPT,
    verbose: bool = infra.VERBOSE_OPT,
    quiet: bool = infra.QUIET_OPT,
) -> None:
    code = infra.stop(compose_file, project_name, env_file, profile, services, dry_run, verbose, quiet)
    raise typer.Exit(code)


def restart(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: Optional[str] = infra.PROJECT_NAME_OPT,
    env_file: Optional[Path] = infra.ENV_FILE_OPT,
    profile: List[str] = infra.PROFILE_OPT,
    services: List[str] = infra.SERVICES_OPT,
    retries: int = typer.Option(10, "--retries"),
    timeout: Optional[int] = typer.Option(None, "--timeout"),
    dry_run: bool = infra.DRY_RUN_OPT,
    verbose: bool = infra.VERBOSE_OPT,
    quiet: bool = infra.QUIET_OPT,
) -> None:
    code = infra.restart(compose_file, project_name, env_file, profile, services, retries, timeout, dry_run, verbose, quiet)
    raise typer.Exit(code)


def rm(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: Optional[str] = infra.PROJECT_NAME_OPT,
    env_file: Optional[Path] = infra.ENV_FILE_OPT,
    profile: List[str] = infra.PROFILE_OPT,
    services: List[str] = infra.SERVICES_OPT,
    volumes: bool = typer.Option(False, "--volumes", "-v"),
    images: str = typer.Option("none", "--images", help="[all|local|none]"),
    dry_run: bool = infra.DRY_RUN_OPT,
    verbose: bool = infra.VERBOSE_OPT,
    quiet: bool = infra.QUIET_OPT,
) -> None:
    code = infra.rm(compose_file, project_name, env_file, profile, services, volumes, images, dry_run, verbose, quiet)
    raise typer.Exit(code)


def status(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: Optional[str] = infra.PROJECT_NAME_OPT,
    env_file: Optional[Path] = infra.ENV_FILE_OPT,
    profile: List[str] = infra.PROFILE_OPT,
    services: List[str] = infra.SERVICES_OPT,
    format: str = typer.Option("table", "--format", help="[table|text|json|yaml]"),
    dry_run: bool = infra.DRY_RUN_OPT,
    verbose: bool = infra.VERBOSE_OPT,
    quiet: bool = infra.QUIET_OPT,
) -> None:
    code = infra.status(compose_file, project_name, env_file, profile, services, format, dry_run, verbose, quiet)
    raise typer.Exit(code)


def logs(
    compose_file: List[Path] = typer.Option([], "--compose-file", "-f"),
    project_name: Optional[str] = infra.PROJECT_NAME_OPT,
    env_file: Optional[Path] = infra.ENV_FILE_OPT,
    profile: List[str] = infra.PROFILE_OPT,
    services: List[str] = infra.SERVICES_OPT,
    follow: bool = typer.Option(False, "--follow", "-F"),
    lines: int = typer.Option(200, "--lines"),
    format: str = typer.Option("plain", "--format", help="[plain|jsonl]"),
    dry_run: bool = infra.DRY_RUN_OPT,
    verbose: bool = infra.VERBOSE_OPT,
    quiet: bool = infra.QUIET_OPT,
) -> None:
    code = infra.logs(compose_file, project_name, env_file, profile, services, follow, lines, format, dry_run, verbose, quiet)
    raise typer.Exit(code)
