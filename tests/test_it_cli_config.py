"""Tests for it_cli.config settings."""
from __future__ import annotations

import importlib

from it_cli import config
from it_cli.config import Settings


def test_env_override(monkeypatch):
    monkeypatch.setenv("IT_SEARCH_API", "http://example.com")
    s = Settings()
    assert s.search_api == "http://example.com"


def test_get_settings_reads_file(tmp_path, monkeypatch):
    cfgdir = tmp_path / ".config/infoterminal"
    cfgdir.mkdir(parents=True)
    (cfgdir / "config.json").write_text('{"search_api": "http://cfg"}')
    monkeypatch.setenv("HOME", str(tmp_path))
    importlib.reload(config)
    s = config.get_settings()
    assert s.search_api == "http://cfg"
