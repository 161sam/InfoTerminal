"""Tests for infra command aliases."""
from __future__ import annotations

from pathlib import Path
from typer.testing import CliRunner

from it_cli.commands import infra

runner = CliRunner()


def test_start_alias(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_UP", tmp_path / "missing.sh")
    async def fake_status():
        return []
    monkeypatch.setattr(infra, "gather_status", fake_status)
    result = runner.invoke(infra.app, ["start", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN" in result.stdout


def test_stop_aliases(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_DOWN", tmp_path / "missing.sh")
    for alias in ("stop", "halt"):
        result = runner.invoke(infra.app, [alias, "--dry-run"])
        assert result.exit_code == 0
        assert "DRY RUN" in result.stdout
