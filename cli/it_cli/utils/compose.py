from __future__ import annotations

import os
import shlex
import subprocess
from typing import Iterable, List, Optional

from rich.console import Console

from ..banner import render_banner

_console = Console()
_banner_printed = False


def print_banner_once() -> None:
    """Render the banner once per process respecting IT_NO_BANNER."""
    global _banner_printed
    if _banner_printed or os.environ.get("IT_NO_BANNER") == "1":
        return
    _console.print(render_banner())
    _banner_printed = True


def build_compose_cmd(
    base: Optional[List[str]] = None,
    files: Optional[Iterable[str]] = None,
    project: Optional[str] = None,
    env_file: Optional[str] = None,
    profiles: Optional[Iterable[str]] = None,
) -> List[str]:
    """Build a docker compose command with common flags."""
    base = list(base or ["docker", "compose"])
    files = files or []
    profiles = profiles or []
    for f in files:
        base.extend(["-f", f])
    if project:
        base.extend(["-p", project])
    if env_file:
        base.extend(["--env-file", env_file])
    for prof in profiles:
        base.extend(["--profile", prof])
    return base


def extend_with_services(cmd: List[str], services: Iterable[str]) -> List[str]:
    cmd.extend(list(services))
    return cmd


def run(cmd: List[str], dry_run: bool = False, verbose: bool = False, quiet: bool = False) -> int:
    """Execute a command or print it when in dry-run mode."""
    print_banner_once()
    printable = " ".join(shlex.quote(c) for c in cmd)
    if dry_run:
        _console.print(printable)
        return 0
    kwargs: dict = {"text": True}
    if quiet:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    elif not verbose:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.STDOUT
    result = subprocess.run(cmd, **kwargs)
    if not quiet and result.stdout:
        _console.print(result.stdout.rstrip())
    return result.returncode
