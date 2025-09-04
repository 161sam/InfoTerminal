"""Tests for TUI log action."""
from __future__ import annotations

import types
import sys

from it_cli.commands import tui, infra


def test_tui_logs_no_typeerror(monkeypatch):
    calls = []

    def fake_show_logs(service: str, lines: int = 0, follow: bool = False) -> None:
        calls.append((service, lines, follow))

    monkeypatch.setattr(infra, "show_logs", fake_show_logs)

    class DummyTable:
        def __init__(self) -> None:
            self.rows = [("search-api",)]
            self.cursor_row = 0

        def get_row_at(self, idx: int):
            return self.rows[idx]

    class DummyApp:
        BINDINGS = []

        def __init__(self) -> None:
            self.table = DummyTable()

        def run(self) -> None:
            self.action_logs()

        # placeholders for abstract methods
        def compose(self):  # pragma: no cover - not used
            return []

    dummy_app = types.SimpleNamespace(App=DummyApp, ComposeResult=list)
    dummy_widgets = types.SimpleNamespace(DataTable=DummyTable, Footer=object, Header=object)
    monkeypatch.setitem(sys.modules, "textual.app", dummy_app)
    monkeypatch.setitem(sys.modules, "textual.widgets", dummy_widgets)

    tui.run()
    assert calls == [("search-api", 200, False)]
