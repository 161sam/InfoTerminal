#!/usr/bin/env python3
"""Execute tasks from TRACKER.json.

The runner reads the tracker created by ``v0_2_scan.py`` and executes
category-specific routines. Each routine is a thin placeholder that can be
extended over time. After successful execution an acceptance check is run
and the task status is updated to ``done``.

Usage:
    python scripts/v0_2_run.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict

TRACKER_PATH = Path("docs/dev/en/releases/v0.2/TRACKER.json")

# Import status checks from the scanner so both scripts stay in sync.
try:
    from v0_2_scan import DONE_CHECKS  # type: ignore
except Exception:  # pragma: no cover - fallback when executed standalone
    DONE_CHECKS = {}


def load_tasks() -> Dict[str, Dict[str, str]]:
    if not TRACKER_PATH.exists():
        return {}
    with TRACKER_PATH.open() as fh:
        data = json.load(fh)
    return {t["id"]: t for t in data.get("tasks", [])}


def save_tasks(tasks: Dict[str, Dict[str, str]]) -> None:
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER_PATH.open("w", encoding="utf-8") as fh:
        json.dump({"tasks": list(tasks.values())}, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def routine_default(task: Dict[str, str]) -> None:
    print(f"[run] TODO for category {task['category']}: {task['title']}")


ROUTINES: Dict[str, Callable[[Dict[str, str]], None]] = {
    # Real implementations would go here; placeholders keep idempotency.
    "NLP": routine_default,
    "Graph": routine_default,
    "Search": routine_default,
    "Dossier": routine_default,
    "Geospatial": routine_default,
    "Security/Ops": routine_default,
    "Automation/Agent": routine_default,
    "Docs/Build": routine_default,
}


def acceptance_ok(task: Dict[str, str]) -> bool:
    check = DONE_CHECKS.get(task["category"], lambda: False)
    return bool(check())


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v0.2 tasks from TRACKER.json")
    parser.add_argument("--dry-run", action="store_true", help="only print actions")
    args = parser.parse_args()

    tasks = load_tasks()
    for task in tasks.values():
        if task.get("status") != "todo":
            continue
        ROUTINES.get(task["category"], routine_default)(task)
        if not args.dry_run and acceptance_ok(task):
            task["status"] = "done"
    if not args.dry_run:
        save_tasks(tasks)


if __name__ == "__main__":
    main()
