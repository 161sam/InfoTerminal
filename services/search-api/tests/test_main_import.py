import importlib
import sys
import types

import app.main as main


def test_main_handles_missing_otel(monkeypatch):
    monkeypatch.delitem(sys.modules, "_shared.obs.otel_boot", raising=False)
    monkeypatch.setitem(sys.modules, "_shared", types.ModuleType("_shared"))
    monkeypatch.setitem(sys.modules, "_shared.obs", types.ModuleType("_shared.obs"))
    importlib.reload(main)
    assert main.app.title == "InfoTerminal Search API"
