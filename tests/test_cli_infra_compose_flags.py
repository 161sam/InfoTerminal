"""Tests for compose flag resolution."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from it_cli.commands import infra

runner = CliRunner()


def test_compose_file_resolution(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docker-compose.yml").write_text("")
    monkeypatch.setenv("IT_COMPOSE_FILE", "env.yml")
    assert infra.resolve_compose_files(None) == ["env.yml"]
    assert infra.resolve_compose_files([Path("cli.yml")]) == ["cli.yml"]
    monkeypatch.delenv("IT_COMPOSE_FILE")
    assert infra.resolve_compose_files(None) == ["docker-compose.yml"]


def test_project_name_resolution(monkeypatch):
    monkeypatch.setenv("IT_PROJECT_NAME", "envproj")
    assert infra.resolve_project_name(None) == "envproj"
    assert infra.resolve_project_name("cliproj") == "cliproj"
    monkeypatch.delenv("IT_PROJECT_NAME")
    assert infra.resolve_project_name(None) == "infoterminal"


def test_env_files_merge(monkeypatch, tmp_path):
    env1 = tmp_path / "env1"
    env1.write_text("A=1\n")
    env2 = tmp_path / "env2"
    env2.write_text("A=2\nB=3\n")
    monkeypatch.setenv("IT_ENV_FILES", str(env1))
    files = infra.resolve_env_files([env2])
    env = infra.load_env_files(files)
    assert env["A"] == "2"
    assert env["B"] == "3"


def test_profiles_resolution(monkeypatch):
    monkeypatch.setenv("IT_PROFILE", "env,default")
    profiles = infra.resolve_profiles(["cli"])
    assert profiles == ["env", "default", "cli"]


def test_dry_run_output(monkeypatch, tmp_path):
    monkeypatch.setattr(infra, "DEV_UP", tmp_path / "missing.sh")
    async def fake_status():
        return []
    monkeypatch.setattr(infra, "gather_status", fake_status)
    result = runner.invoke(
        infra.app,
        ["up", "--dry-run", "-f", "one.yml", "-p", "proj"],
    )
    assert result.exit_code == 0
    assert "DRY RUN" in result.stdout
    assert "one.yml" in result.stdout
    assert "proj" in result.stdout
