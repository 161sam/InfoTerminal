"""Additional log command tests."""
from __future__ import annotations

from typer.testing import CliRunner

from it_cli.__main__ import app

runner = CliRunner()


def test_logs_follow_and_lines():
    res = runner.invoke(app, ["logs", "-n", "-s", "neo4j", "--lines", "5", "-F"])
    assert res.exit_code == 0
    out = res.stdout
    assert "docker compose logs --tail 5 -f neo4j" in out
