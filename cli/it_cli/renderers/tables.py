"""Helpers for creating Rich tables."""
from __future__ import annotations

from rich.table import Table


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
