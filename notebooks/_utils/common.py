"""Common helpers for deterministic forensic lab notebooks."""

from __future__ import annotations

import csv
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from itertools import count
from pathlib import Path
from typing import Iterable, Sequence

__all__ = [
    "DRY_RUN",
    "CLI_OK",
    "LABS_ROOT",
    "lab_root",
    "_ts",
    "json_dump_sorted",
    "csv_write_rows_sorted",
    "shell_available",
    "run_cli",
    "preview",
]

LABS_ROOT = Path(".labs")
LABS_ROOT.mkdir(exist_ok=True)

_DR_DEFAULT_SEED = os.environ.get("LABS_SEED_TIMESTAMP", "20240101T000000Z")
_TS_FORMAT = None
_TS_COUNTER = count()


def _load_timestamp_format() -> str:
    global _TS_FORMAT
    if _TS_FORMAT is not None:
        return _TS_FORMAT

    fmt = "%Y%m%dT%H%M%SZ"
    config_path_candidates = [
        Path("config/framework.yaml"),
        Path("config/framework.yml"),
    ]
    for candidate in config_path_candidates:
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                stripped = line.strip()
                if stripped.startswith("timestamp_format:"):
                    _, value = stripped.split(":", 1)
                    value = value.strip().strip("'\"")
                    if value:
                        fmt = value
                    break
    _TS_FORMAT = fmt
    return fmt


def _initial_timestamp() -> datetime:
    seed = _DR_DEFAULT_SEED
    try:
        base = datetime.strptime(seed, "%Y%m%dT%H%M%SZ")
        return base.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime(2024, 1, 1, tzinfo=timezone.utc)


_BASE_TS = _initial_timestamp()


class _DryRunFlag:
    """Runtime toggle shared by notebooks."""

    value: bool = True


DRY_RUN = _DryRunFlag()


class _CliFlag:
    value: bool = False


CLI_OK = _CliFlag()


def lab_root(lab_id: str) -> Path:
    """Return and create the deterministic folder for a lab."""
    safe_id = lab_id.strip().lower().replace(" ", "_")
    path = LABS_ROOT / safe_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _ts() -> str:
    """Return a deterministic, monotonic timestamp string."""
    fmt = _load_timestamp_format()
    step = next(_TS_COUNTER)
    current = _BASE_TS + timedelta(seconds=step)
    return current.strftime(fmt)


def json_dump_sorted(obj: object, path: Path) -> None:
    """Write JSON with sorted keys and trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(obj, handle, indent=2, sort_keys=True)
        handle.write("\n")


def csv_write_rows_sorted(
    rows: Iterable[Sequence[object]],
    path: Path,
    header: Sequence[str],
) -> None:
    """Write a CSV with rows sorted lexicographically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_rows = sorted(list(rows))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(list(header))
        for row in sorted_rows:
            writer.writerow(list(row))


def shell_available(command: str) -> bool:
    """Return True when a CLI command is available on PATH."""
    from shutil import which

    return which(command) is not None


def run_cli(cmd: Sequence[str], tolerate: bool = True, timeout: int = 60):
    """Execute a CLI command with optional tolerance for failures."""
    try:
        completed = subprocess.run(
            list(cmd),
            check=not tolerate,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return completed.returncode, completed.stdout.strip(), completed.stderr.strip()
    except subprocess.CalledProcessError as exc:  # pragma: no cover - fallback path
        return exc.returncode, exc.stdout.strip(), exc.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"


def preview(path: Path, max_bytes: int = 4096) -> str:
    """Return a bounded preview of a file for notebook display."""
    if not path.exists():
        return "<missing>"
    data = path.read_bytes()[:max_bytes]
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")
