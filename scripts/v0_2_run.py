#!/usr/bin/env python3
"""Execute v0.2 tasks based on TRACKER.json.

The runner reads the tracker produced by ``v0_2_scan.py`` and executes a
category specific routine for each task still marked as ``todo``. After the
routine completes an optional acceptance check is performed. Only if the check
passes the task is marked ``done``.

Usage:
    python scripts/v0_2_run.py         # run tasks
    python scripts/v0_2_run.py --dry-run  # only show planned actions
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict, List

TRACKER_PATH = Path("docs/dev/en/releases/v0.2/TRACKER.json")


# ---- tracker helpers -----------------------------------------------------


def load_tasks() -> List[Dict]:
    if not TRACKER_PATH.exists():
        return []
    data = json.loads(TRACKER_PATH.read_text())
    return data.get("tasks", [])


def write_tasks(tasks: List[Dict]) -> None:
    TRACKER_PATH.write_text(
        json.dumps({"tasks": tasks}, indent=2, ensure_ascii=False) + "\n"
    )


# ---- category handlers ---------------------------------------------------


def _placeholder(task: Dict) -> None:
    print(f"[WARN] No implementation for category {task['category']}: {task['title']}")


HANDLERS: Dict[str, Callable[[Dict], None]] = {
    "NLP": _placeholder,
    "Graph": _placeholder,
    "Search": _placeholder,
    "Dossier": _placeholder,
    "Geospatial": _placeholder,
    "Security/Ops": _placeholder,
    "Automation/Agent": _placeholder,
    "Docs/Build": _placeholder,
}


# ---- acceptance ----------------------------------------------------------


def check_acceptance(task: Dict) -> bool:
    """Return True if a task's acceptance criteria are met.

    The current implementation is a stub that always returns ``False`` so that
    tasks remain ``todo`` until a human confirms the result and adjusts the
    tracker accordingly.
    """
    return False


# ---- main runner ---------------------------------------------------------


def run(dry_run: bool = False) -> None:
    tasks = load_tasks()
    changed = False
    for task in tasks:
        if task.get("status") != "todo":
            continue
        if dry_run:
            print(f"[DRY] {task['id']} -> {task['category']}: {task['title']}")
            continue
        try:
            HANDLERS.get(task["category"], _placeholder)(task)
            if check_acceptance(task):
                task["status"] = "done"
                task.pop("last_error", None)
            else:
                task["last_error"] = "acceptance failed"
        except Exception as exc:  # pragma: no cover - defensive
            task["last_error"] = str(exc)
        changed = True
    if changed and not dry_run:
        write_tasks(tasks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v0.2 tasks from TRACKER.json")
    parser.add_argument(
        "--dry-run", action="store_true", help="only print planned tasks"
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
