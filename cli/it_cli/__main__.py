"""Entry point for InfoTerminal CLI."""
import typer
from rich.console import Console

from .banner import print_banner
from .commands import infra, search, graph, views, analytics, settings, tui
from .plugins import load_plugins

app = typer.Typer(no_args_is_help=True, help="InfoTerminal CLI – modular & pretty")
console = Console()


@app.callback(invoke_without_command=True)
def _root(ctx: typer.Context):  # noqa: D401 - minimal docstring
    """Root callback printing banner."""
    print_banner(console)


# register subcommands
app.add_typer(infra.app, name="infra", help="Infra: up/down/status/logs")
app.add_typer(search.app, name="search", help="Search API")
app.add_typer(graph.app, name="graph", help="Neo4j / Graph")
app.add_typer(views.app, name="views", help="Graph-Views (Postgres)")
app.add_typer(analytics.app, name="analytics", help="KPIs & Dashboards")
app.add_typer(settings.app, name="settings", help="Config/Env")
app.add_typer(tui.app, name="ui", help="Textual TUI")

# load plugins
load_plugins(app)


if __name__ == "__main__":  # pragma: no cover - main entry
    app()
