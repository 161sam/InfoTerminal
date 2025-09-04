from __future__ import annotations

import os
import shutil
import sys
from typing import Optional

_PRINTED = False  # once-per-process guard


def _is_tty() -> bool:
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def _banner_enabled() -> bool:
    # Env kill-switch
    if os.getenv("IT_NO_BANNER") == "1":
        return False
    # Hidden flags: --no-banner, --quiet, -q
    argv = sys.argv[1:]
    hidden_flags = {"--no-banner", "--quiet", "-q"}
    if any(a in hidden_flags for a in argv):
        return False
    return True


def _render_figlet(text: str) -> Optional[str]:
    try:
        import pyfiglet  # type: ignore
    except Exception:
        return None
    try:
        return pyfiglet.figlet_format(text, font="Standard", width=100)
    except Exception:
        return None


def _render_fallback(text: str) -> str:
    # Minimal, breiteunabhängige ASCII-Variante (nur als Fallback genutzt)
    return f"=== {text} ==="


def _terminal_width(default: int = 100) -> int:
    try:
        return shutil.get_terminal_size((default, 20)).columns
    except Exception:
        return default


def render_banner() -> str:
    title = "INFOTERMINAL"
    sub = "it — infra/search/graph/views"
    art = _render_figlet(title) or _render_fallback(title)
    width = max(40, min(120, _terminal_width(100)))
    subline = sub.center(width)
    return f"{art.rstrip()}\n{subline}"


def show_banner(force: bool = False) -> None:
    global _PRINTED
    if _PRINTED and not force:
        return
    if not force and not _banner_enabled():
        return

    if _is_tty():
        try:
            print(render_banner())
        except Exception:
            # Never block CLI on banner issues
            pass
    else:
        # Non-TTY: kurze Einzeile, damit Logs nicht vollfluten
        print("InfoTerminal CLI — it")

    _PRINTED = True


def auto_banner_on_import() -> None:
    # Run best-effort. Swallow all exceptions to avoid breaking CLI.
    try:
        show_banner(False)
    except Exception:
        pass
