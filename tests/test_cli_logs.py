"""Tests for infra logs command."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from it_cli.commands import infra

runner = CliRunner()


def test_logs_from_file(monkeypatch, tmp_path):
    log = tmp_path / "it_graph-api.log"
    log.write_text("a\nb\nc\n")
    monkeypatch.setitem(infra.LOG_FILES, "graph-api", str(log))
    result = runner.invoke(infra.app, ["logs", "--services", "graph-api", "--lines", "2"])
    assert result.exit_code == 0
    assert "b" in result.stdout
    assert "a\n" not in result.stdout


def test_logs_follow(monkeypatch, tmp_path):
    log = tmp_path / "it_search-api.log"
    log.write_text("")
    monkeypatch.setitem(infra.LOG_FILES, "search-api", str(log))

    def fake_follow(path: Path, lines: int):
        yield "x\n"
        yield "y\n"

    monkeypatch.setattr(infra, "_follow_file", fake_follow)
    result = runner.invoke(infra.app, ["logs", "--services", "search-api", "-f", "--lines", "1"])
    assert result.exit_code == 0
    assert "x" in result.stdout and "y" in result.stdout


def test_logs_docker(monkeypatch):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(infra.subprocess, "run", fake_run)
    result = runner.invoke(infra.app, ["logs", "--services", "neo4j", "--lines", "5", "-f"])
    assert result.exit_code == 0
    assert ["docker", "logs", "--tail", "5", "-f", "neo4j"] in calls
