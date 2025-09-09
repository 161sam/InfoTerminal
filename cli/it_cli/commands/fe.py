import subprocess
from pathlib import Path

import typer

app = typer.Typer(help="Frontend commands")

ROOT = Path(__file__).resolve().parents[3]


def _run(cmd: list[str]):
    subprocess.check_call(cmd, cwd=ROOT)


@app.command("dev")
def dev() -> None:
    _run(["npm", "-w", "apps/frontend", "run", "dev"])


@app.command("build")
def build() -> None:
    _run(["npm", "-w", "apps/frontend", "run", "build"])


@app.command("test")
def test() -> None:
    _run(["npm", "-w", "apps/frontend", "run", "test", "--", "--reporter=dot"])
