import importlib
import sys
import types

import app.main as main


def test_main_handles_missing_otel(monkeypatch):
    monkeypatch.delitem(sys.modules, "obs.otel_boot", raising=False)
    monkeypatch.setitem(sys.modules, "obs", types.ModuleType("obs"))
    importlib.reload(main)
    assert main.app.title == "InfoTerminal Search API"
