"""Settings commands."""
from __future__ import annotations

import json

import typer
from rich.console import Console

from ..config import get_settings

app = typer.Typer()
console = Console()


@app.command()
def show() -> None:
    """Print current configuration."""
    settings = get_settings()
    console.print_json(data=json.loads(settings.model_dump_json()))
