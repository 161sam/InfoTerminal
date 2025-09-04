"""Compose flag handling tests."""
from __future__ import annotations

from typing import List

from typer.testing import CliRunner

from it_cli.__main__ import app

runner = CliRunner()


def run(args: List[str]):
    return runner.invoke(app, args)


def test_multiple_compose_files_and_profiles():
    res = run(["start", "-n", "-f", "one.yml", "-f", "two.yml", "--profile", "p1", "--profile", "p2"])
    out = res.stdout
    assert "-f one.yml" in out and "-f two.yml" in out
    assert "--profile p1" in out and "--profile p2" in out


def test_env_file_and_project_name():
    res = run(["start", "-n", "--env-file", "env.env", "-p", "proj"])
    out = res.stdout
    assert "--env-file env.env" in out
    assert "-p proj" in out


def test_services_parsing():
    res = run(["start", "-n", "-s", "a,b", "-s", "c"])
    assert "a b c" in res.stdout


def test_status_formats(monkeypatch):
    called = {}

    def fake_run(cmd, *a, **k):
        called["cmd"] = cmd
        class R:
            stdout = "[{\"Service\":\"s\"}]"
            returncode = 0
        return R()

    monkeypatch.setattr("subprocess.run", fake_run)
    res = run(["status", "--format", "json"])
    assert called["cmd"][-2:] == ["--format", "json"]
    res = run(["status", "--format", "yaml"])
    assert "Service" in res.stdout
    res = run(["status", "-n"])
    assert "docker compose ps" in res.stdout
