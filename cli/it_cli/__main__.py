"""Entry point for the InfoTerminal CLI."""
from __future__ import annotations

import sys

import typer
from rich.console import Console

from . import __version__, infra, root as root_cmds
from .plugins import load_plugins
from .utils import NaturalOrderGroup
from .utils.compose import print_banner_once

console = Console()
app = typer.Typer(no_args_is_help=True, help="InfoTerminal CLI", cls=NaturalOrderGroup)


@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-V", is_eager=True, help="Show version and exit"),
) -> None:
    if version:
        console.print(f"it {__version__}")
        raise typer.Exit()


# register root commands in explicit order
app.command("start", help="Start services")(root_cmds.start)
app.command("stop", help="Stop services")(root_cmds.stop)
app.command("restart", help="Restart services")(root_cmds.restart)
app.command("rm", help="Remove services")(root_cmds.rm)
app.command("status", help="Service status")(root_cmds.status)
app.command("logs", help="Show logs")(root_cmds.logs)

# infra namespace
app.add_typer(infra.app, name="infra", help="Infra: compose wrapper")

# load plugins if available
load_plugins(app)


def main() -> None:
    if any(arg in ("-V", "--version") for arg in sys.argv[1:]):
        console.print(f"it {__version__}")
        raise SystemExit(0)
    print_banner_once()
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
