"""Tests for `it infra status`."""
from __future__ import annotations

from typer.testing import CliRunner

from it_cli.commands import infra

runner = CliRunner()


def test_status_all_up(monkeypatch):
    async def ok_http(name, url):
        return {"service": name, "status": "UP", "port": 1, "latency": "1ms"}

    async def ok_tcp(name, host, port):
        return {"service": name, "status": "UP", "port": port, "latency": "1ms"}

    monkeypatch.setattr(infra, "probe_http", ok_http)
    monkeypatch.setattr(infra, "probe_tcp", ok_tcp)

    result = runner.invoke(infra.app, ["status"])
    assert result.exit_code == 0
    assert "search-api" in result.stdout
    assert "UP" in result.stdout


def test_status_failure_exit(monkeypatch):
    async def fake_http(name, url):
        status = "DOWN" if name == "graph-api" else "UP"
        return {"service": name, "status": status, "port": 1, "latency": ""}

    async def fake_tcp(name, host, port):
        return {"service": name, "status": "UNAVAILABLE", "port": port, "latency": ""}

    monkeypatch.setattr(infra, "probe_http", fake_http)
    monkeypatch.setattr(infra, "probe_tcp", fake_tcp)

    result = runner.invoke(infra.app, ["status"])
    assert result.exit_code != 0
    assert "graph-api" in result.stdout
    assert "DOWN" in result.stdout
