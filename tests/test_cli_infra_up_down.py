"""Tests for infra up/down commands."""
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

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(infra.subprocess, "run", fake_run)

    result = runner.invoke(infra.app, ["up", "--agents", "--gateway", "--opa-host", "opa"])
    assert result.exit_code == 0
    assert calls[0][0] == str(script)
    assert "--agents" in calls[0]
    assert "--gateway" in calls[0]
    assert "--opa-host" in calls[0]


def test_up_docker_compose(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_UP", tmp_path / "missing.sh")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docker-compose.agents.yml").write_text("")
    (tmp_path / "docker-compose.gateway.yml").write_text("")

    calls = []

    def fake_run(cmd, check=False, capture_output=False, text=False, **kwargs):
        calls.append(cmd)
        if check:
            raise infra.subprocess.CalledProcessError(1, cmd, stderr="network already exists")
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(infra.subprocess, "run", fake_run)

    result = runner.invoke(infra.app, ["up", "--agents", "--gateway"])
    assert result.exit_code == 0
    assert ["docker", "compose", "up", "-d", "opensearch", "neo4j"] in calls
    assert ["docker", "compose", "-f", "docker-compose.agents.yml", "up", "-d"] in calls
    assert ["docker", "compose", "-f", "docker-compose.gateway.yml", "up", "-d"] in calls


def test_down_docker_compose(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_DOWN", tmp_path / "missing.sh")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docker-compose.agents.yml").write_text("")
    (tmp_path / "docker-compose.gateway.yml").write_text("")

    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(infra.subprocess, "run", fake_run)

    result = runner.invoke(infra.app, ["down", "--all"])
    assert result.exit_code == 0
    assert ["docker", "compose", "down", "--remove-orphans"] in calls
    assert ["docker", "compose", "-f", "docker-compose.agents.yml", "down", "--remove-orphans"] in calls
    assert ["docker", "compose", "-f", "docker-compose.gateway.yml", "down", "--remove-orphans"] in calls
