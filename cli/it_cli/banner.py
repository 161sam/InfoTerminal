"""Colorful startup banner using Rich."""
from __future__ import annotations

import os
import platform

from rich import box
from rich.panel import Panel
from rich.text import Text


def print_banner(console):
    """Render a simple InfoTerminal banner."""
    title = Text(" InfoTerminal CLI ", style="bold white on blue")
    meta = Text.assemble(
        (" version ", "dim"), (os.environ.get("IT_VERSION", "dev"), "bold"),
        (" • py ", "dim"), (platform.python_version(), "bold"),
        (" • env ", "dim"), (os.environ.get("IT_ENV", "local"), "bold"),
    )
    console.print(Panel.fit(meta, title=title, border_style="blue", box=box.ROUNDED))
