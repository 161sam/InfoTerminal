"""Entry point for InfoTerminal CLI."""
from __future__ import annotations

import os
import sys

import typer
from rich.console import Console

from . import __version__
from .banner import print_banner
from .commands import analytics, graph, infra, search, settings, tui, views
from .plugins import load_plugins
from .utils import NaturalOrderGroup

console = Console()
app = typer.Typer(
    no_args_is_help=True,
    help="InfoTerminal CLI – modular & pretty",
    cls=NaturalOrderGroup,
)


@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        is_eager=True,
        help="Show version and exit",
    ),
):
    """Handle root options like --version."""
    if version:
        console.print(f"it {__version__}")
        raise typer.Exit()


# register lifecycle commands in explicit order
app.command("start", help="Start local development infrastructure.")(infra.start)
app.command("stop", help="laufende Services anhalten")(infra.stop)
app.command("rm", help="Umgebung entfernen")(infra.rm)
app.command("restart", help="Restart infrastructure.")(infra.restart)
app.command("status", help="Check health of services.")(infra.status)
app.command("logs", help="Show logs for services.")(infra.logs)

# remaining command groups
app.add_typer(infra.app, name="infra", help="Infra: up/down/status/logs")
app.add_typer(search.app, name="search", help="Search API")
app.add_typer(graph.app, name="graph", help="Neo4j / Graph")
app.add_typer(views.app, name="views", help="Graph-Views (Postgres)")
app.add_typer(analytics.app, name="analytics", help="KPIs & Dashboards")
app.add_typer(settings.app, name="settings", help="Config/Env")
app.add_typer(tui.app, name="ui", help="Textual TUI")

# load plugins
load_plugins(app)


def main() -> None:
    """CLI entry point that prints banner before running Typer."""
    if any(arg in ("-V", "--version") for arg in sys.argv[1:]):
        console.print(f"it {__version__}")
        raise SystemExit(0)
    if os.environ.get("IT_NO_BANNER") != "1":
        print_banner(console)
    app()


if __name__ == "__main__":  # pragma: no cover - main entry
    main()
