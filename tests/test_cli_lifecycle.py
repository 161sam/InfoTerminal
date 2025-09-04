"""Lifecycle command forwarding tests."""
from __future__ import annotations

from typer.testing import CliRunner

from it_cli.__main__ import app

runner = CliRunner()


def run(args: list[str]):
    return runner.invoke(app, args)


def test_root_help_lists_commands():
    res = run(["--help"])
    assert res.exit_code == 0
    assert "start" in res.stdout
    assert "infra" in res.stdout
    assert "search" not in res.stdout  # no other groups


def test_start_dry_run_builds_command():
    res = run(["start", "-n"])
    assert res.exit_code == 0
    assert "docker compose up" in res.stdout


def test_restart_forwards_services():
    res = run(["restart", "-n", "-s", "graph-api"])
    assert res.exit_code == 0
    assert "docker compose restart graph-api" in res.stdout


def test_rm_with_flags():
    res = run(["rm", "-n", "-v", "--images", "local"])
    assert res.exit_code == 0
    out = res.stdout
    assert "docker compose down --remove-orphans" in out
    assert "-v" in out and "--rmi local" in out


def test_logs_requires_service():
    res = run(["logs", "-n", "-s", "neo4j", "--lines", "50"])
    assert res.exit_code == 0
    assert "docker compose logs --tail 50 neo4j" in res.stdout
    res2 = run(["logs", "-n"])
    assert res2.exit_code != 0
    assert "requires at least one service" in res2.stderr
