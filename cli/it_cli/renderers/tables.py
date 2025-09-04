"""Helpers for creating Rich tables."""
from __future__ import annotations

from rich.table import Table
from rich.panel import Panel


def status_table(rows: list[dict]) -> Table:
    """Render a service status table with colored states."""
    table = Table(title="Service Status")
    table.add_column("Service")
    table.add_column("Status")
    table.add_column("Port")
    table.add_column("Latency")
    for row in rows:
        status = row.get("status", "")
        style = "green" if status == "UP" else "red" if status.startswith("DOWN") else "yellow"
        table.add_row(
            row.get("service", ""),
            f"[{style}]{status}[/{style}]" if status else "",
            str(row.get("port", "")),
            row.get("latency", ""),
        )
    return table


def log_panel(title: str) -> Panel:
    """Return a simple panel used as heading for log output."""
    return Panel("", title=title)


def dicts_to_table(title: str, rows: list[dict]) -> Table:
    """Return a table built from a list of dicts."""
    table = Table(title=title)
    if not rows:
        return table
    columns = list(rows[0].keys())
    for col in columns:
        table.add_column(str(col))
    for row in rows:
        table.add_row(*[str(row.get(col, "")) for col in columns])
    return table
