"""Placeholder for Textual TUI."""
from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def run() -> None:
    """Run the Textual TUI (placeholder)."""
    console.print("TUI not implemented.")
