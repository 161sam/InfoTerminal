"""Tests for CLI banner and version option."""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

from it_cli import __version__


def _run_cli(args: list[str], env: dict[str, str] | None = None):
    cmd = [sys.executable, "-m", "it_cli", *args]
    env = env or os.environ.copy()
    cli_path = pathlib.Path(__file__).resolve().parents[1] / "cli"
    env["PYTHONPATH"] = os.pathsep.join(
        [str(cli_path), env.get("PYTHONPATH", "")]
    )
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def test_help_shows_banner():
    result = _run_cli(["--help"])
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert not lines[0].startswith("Usage:")  # banner printed before help
    assert "InfoTerminal CLI" in result.stdout


def test_version_option_no_banner():
    result = _run_cli(["-V"])
    assert result.returncode == 0
    assert result.stdout.strip() == f"it {__version__}"
    assert "InfoTerminal CLI" not in result.stdout


def test_no_banner_env(monkeypatch):
    env = os.environ.copy()
    env["IT_NO_BANNER"] = "1"
    result = _run_cli(["--help"], env=env)
    assert result.returncode == 0
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert lines[0].lstrip().startswith("Usage:")
