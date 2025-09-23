"""Entry point for the InfoTerminal CLI."""
from __future__ import annotations

import sys

import typer
from rich.console import Console

from . import __version__, infra, root as root_cmds
from .commands import (
    analytics, auth, agents, cache, collab, feedback, fe, forensics, 
    graph, media, nlp, ops, perf, plugins, rag, search, settings, 
    tui, verify, views, ws
)
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

# Register all command groups in logical order
app.add_typer(infra.app, name="infra", help="Infrastructure: Docker Compose operations")
app.add_typer(auth.app, name="auth", help="Authentication & User Management")
app.add_typer(search.app, name="search", help="Search & Document Indexing")
app.add_typer(graph.app, name="graph", help="Graph Operations & Analytics")
app.add_typer(views.app, name="views", help="Graph Views & Visualizations")
app.add_typer(nlp.app, name="nlp", help="NLP & Document Processing")
app.add_typer(verify.app, name="verify", help="Verification & Fact-Checking")
app.add_typer(rag.app, name="rag", help="RAG & Document Retrieval")
app.add_typer(agents.app, name="agents", help="Agent Execution & Management")
app.add_typer(plugins.app, name="plugins", help="Plugin Management & Execution")
app.add_typer(forensics.app, name="forensics", help="Forensics & Evidence Management")
app.add_typer(media.app, name="media", help="Media Forensics & Analysis")
app.add_typer(feedback.app, name="feedback", help="User Feedback & Analytics")
app.add_typer(perf.app, name="perf", help="Performance Monitoring & Metrics")
app.add_typer(ops.app, name="ops", help="Operations & System Management")
app.add_typer(cache.app, name="cache", help="Cache Management & Operations")
app.add_typer(ws.app, name="ws", help="WebSocket & Real-time Communication")
app.add_typer(collab.app, name="collab", help="Collaboration & Task Management")
app.add_typer(fe.app, name="fe", help="Frontend Management")
app.add_typer(analytics.app, name="analytics", help="Analytics & KPI Dashboard")
app.add_typer(settings.app, name="settings", help="Configuration Management")
app.add_typer(tui.app, name="tui", help="Terminal User Interface")

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
