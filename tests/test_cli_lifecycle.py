"""Tests for lifecycle CLI commands."""
from __future__ import annotations

from typer.testing import CliRunner

from it_cli.__main__ import app as main_app
from it_cli.commands import infra

runner = CliRunner()


def _run_main(cmd: list[str]):
    return runner.invoke(main_app, cmd)


def test_root_help_layout_exact():
    result = _run_main(["--help"])
    assert result.exit_code == 0
    # extract lines between command box
    lines = [line.strip("│ ") for line in result.stdout.splitlines() if line.startswith("│")]
    start_idx = lines.index(next(l for l in lines if l.startswith("start")))
    commands = lines[start_idx:start_idx + 13]
    expected = [
        "start       Start local development infrastructure.",
        "stop        laufende Services anhalten",
        "rm          Umgebung entfernen",
        "restart     Restart infrastructure.",
        "status      Check health of services.",
        "logs        Show logs for services.",
        "infra       Infra: up/down/status/logs",
        "search      Search API",
        "graph       Neo4j / Graph",
        "views       Graph-Views (Postgres)",
        "analytics   KPIs & Dashboards",
        "settings    Config/Env",
        "ui          Textual TUI",
    ]
    assert commands == expected


def test_infra_visible_but_not_expanded():
    result = _run_main(["--help"])
    assert "infra" in result.stdout
    assert "\n│ up" not in result.stdout
    sub = _run_main(["infra", "--help"])
    assert "up" in sub.stdout and "down" in sub.stdout
    assert "restart" in sub.stdout and "halt" in sub.stdout


def test_services_flag_normalization(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_UP", tmp_path / "missing.sh")
    async def fake_status():
        return []
    monkeypatch.setattr(infra, "gather_status", fake_status)
    calls = []
    monkeypatch.setattr(infra, "execute", lambda cmd, env, dry, verb, quiet, **kw: calls.append(cmd))
    runner.invoke(main_app, ["start", "-n", "-s", "a,b", "-s", "c"])
    first = calls[-1]
    runner.invoke(main_app, ["start", "-n", "-s", "a", "-s", "b", "-s", "c"])
    second = calls[-1]
    assert first == second


def test_rm_flags_rendering(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_DOWN", tmp_path / "missing.sh")
    calls = []
    monkeypatch.setattr(infra, "execute", lambda cmd, env, dry, verb, quiet, **kw: calls.append(cmd))
    runner.invoke(main_app, ["rm", "-n"])
    cmd = calls[-1]
    assert "down" in cmd and "--remove-orphans" in cmd and "-v" not in cmd and "--rmi" not in cmd
    runner.invoke(main_app, ["rm", "-n", "-v"])
    assert "-v" in calls[-1]
    runner.invoke(main_app, ["rm", "-n", "--images", "local"])
    assert "--rmi" in calls[-1] and "local" in calls[-1]


def test_status_exit_codes(monkeypatch):
    async def failing():
        return [{"service": "a", "status": "DOWN (500)", "port": 1, "latency": ""}]
    monkeypatch.setattr(infra, "gather_status", failing)
    res = runner.invoke(main_app, ["status"])
    assert res.exit_code == 1
    async def degraded():
        return [{"service": "a", "status": "DEGRADED", "port": 1, "latency": ""}]
    monkeypatch.setattr(infra, "gather_status", degraded)
    res = runner.invoke(main_app, ["status"])
    assert res.exit_code == 0


def test_logs_requires_services(monkeypatch):
    res = runner.invoke(main_app, ["logs"])
    assert res.exit_code == 2
    monkeypatch.setattr(infra, "show_logs", lambda *a, **k: None)
    res = runner.invoke(main_app, ["logs", "-s", "a"])
    assert res.exit_code == 0
