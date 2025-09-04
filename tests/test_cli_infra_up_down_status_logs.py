"""Combined tests for infra commands."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from it_cli.commands import infra

runner = CliRunner()


def test_up_uses_script(monkeypatch, tmp_path):
    script = tmp_path / "dev_up.sh"
    script.write_text("echo up")
    monkeypatch.setattr(infra, "DEV_UP", script)
    calls = []

    def fake_execute(cmd, env, dry_run, verbose, quiet, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(infra, "execute", fake_execute)
    async def fake_status():
        return []
    monkeypatch.setattr(infra, "gather_status", fake_status)
    result = runner.invoke(infra.app, ["up", "--detach"])
    assert result.exit_code == 0
    assert calls[0][0] == str(script)
    assert "-d" in calls[0]


def test_down_services(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_DOWN", tmp_path / "missing.sh")
    calls = []

    def fake_execute(cmd, env, dry_run, verbose, quiet, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(infra, "execute", fake_execute)
    result = runner.invoke(infra.app, ["down", "--services", "neo4j"])
    assert result.exit_code == 0
    assert "neo4j" in calls[0]


def test_status_filter(monkeypatch):
    async def fake_status():
        return [
            {"service": "search-api", "status": "UP", "port": 1, "latency": ""},
            {"service": "graph-api", "status": "DOWN", "port": 1, "latency": ""},
        ]

    monkeypatch.setattr(infra, "gather_status", fake_status)
    result = runner.invoke(infra.app, ["status", "--services", "search-api"])
    assert result.exit_code == 0
    assert "graph-api" not in result.stdout


def test_logs_multi(monkeypatch, tmp_path):
    log = tmp_path / "it_search-api.log"
    log.write_text("hello")
    monkeypatch.setattr(infra, "LOG_FILES", {"search-api": str(log)})
    file_calls = []
    docker_calls = []
    monkeypatch.setattr(infra, "_display_file_logs", lambda p, l, f: file_calls.append((str(p), l, f)))
    monkeypatch.setattr(infra, "_display_docker_logs", lambda c, l, f: docker_calls.append((c, l, f)))
    result = runner.invoke(
        infra.app,
        ["logs", "--services", "search-api", "--services", "graph-api", "--lines", "5", "--follow"],
    )
    assert result.exit_code == 0
    assert file_calls[0] == (str(log), 5, True)
    assert docker_calls[0] == ("graph-api", 5, True)
