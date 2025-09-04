"""Plugin loading for InfoTerminal CLI."""
from __future__ import annotations

from importlib.metadata import entry_points


def load_plugins(app) -> None:
    """Load optional plugin Typer apps via entry points."""
    try:
        eps = entry_points(group="info_terminal.plugins")
    except TypeError:  # pragma: no cover - for older Python
        eps = entry_points().get("info_terminal.plugins", [])
    for ep in eps:
        try:
            name, subapp = ep.load()
            app.add_typer(subapp, name=name)
        except Exception:  # pragma: no cover - optional
            pass
