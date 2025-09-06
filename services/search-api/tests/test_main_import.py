import importlib
import sys
import types

import search_api.app.main as main


def test_main_handles_missing_otel(monkeypatch):
    monkeypatch.delitem(sys.modules, "search_api._shared.obs.otel_boot", raising=False)
    monkeypatch.setitem(sys.modules, "search_api._shared", types.ModuleType("search_api._shared"))
    monkeypatch.setitem(sys.modules, "search_api._shared.obs", types.ModuleType("search_api._shared.obs"))
    importlib.reload(main)
    assert main.app.title == "InfoTerminal Search API"
