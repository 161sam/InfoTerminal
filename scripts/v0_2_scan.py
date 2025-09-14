#!/usr/bin/env python3
"""Scan project docs for v0.2 tasks and update TRACKER.json.

This script searches various documentation sources for TODO-like markers
related to the v0.2 release. The results are stored in
``docs/dev/en/releases/v0.2/TRACKER.json``. Re-running the script is
idempotent: existing tasks are preserved and updated in-place.

Usage:
    python scripts/v0_2_scan.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import hashlib
import os
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

# Directories/files to scan
SCAN_TARGETS = [
    Path("docs/dev"),
    Path("ROADMAP.md"),
    # The new-docs workspace is large; restrict scanning to the v0.2 section to
    # keep the tracker manageable while still covering planned items.
    Path(
        "WORK-ON-new_docs/InfoTerminal-docs-clean-with-indexes/docs/dev/v0.2"
    ),
    Path("Checkliste.md"),
]

# Search keywords. A line is considered a task when it contains at least one of
# the "main" keywords (typically todo markers). Additional terms such as
# ``v0.2`` or ``legacy`` are searched as context but won't create tasks on their
# own to keep the tracker compact.
MAIN_KEYWORDS = [r"TODO", r"FIXME", r"WIP", r"Muss", r"Must", r"Soll"]
EXTRA_KEYWORDS = [r"v0\.2", r"pre-release", r"legacy"]
KEYWORD_RE = re.compile("|".join(MAIN_KEYWORDS + EXTRA_KEYWORDS), re.IGNORECASE)
MAIN_RE = re.compile("|".join(MAIN_KEYWORDS), re.IGNORECASE)

TRACKER_PATH = Path("docs/dev/en/releases/v0.2/TRACKER.json")

CATEGORY_KEYWORDS = {
    "NLP": ["nlp", "entity", "ner", "relation"],
    "Graph": ["graph", "ontology", "gds"],
    "Search": ["search", "query", "facet"],
    "Dossier": ["dossier", "report"],
    "Geospatial": ["geo", "map", "leaflet"],
    "Security/Ops": ["security", "oauth", "oidc", "jwt", "audit"],
    "Automation/Agent": ["flowise", "n8n", "agent", "workflow"],
    "Docs/Build": [],
}

DONE_CHECKS = {
    "NLP": lambda: Path("services/doc-entities").exists()
    or Path("services/nlp-service").exists(),
    "Graph": lambda: Path("services/graph-api").exists()
    and Path("services/graph-views").exists(),
    "Search": lambda: Path("services/search-api").exists(),
    "Dossier": lambda: Path("services/graph-views/dossier").exists(),
    "Geospatial": lambda: Path("services/graph-views/geo.py").exists(),
    "Security/Ops": lambda: Path("services/gateway").exists(),
    "Automation/Agent": lambda: Path("plugins/n8n").exists()
    or Path("plugins/flowise").exists(),
    "Docs/Build": lambda: True,
}


def in_scope(path: Path) -> bool:
    for target in SCAN_TARGETS:
        try:
            if path.is_relative_to(target):
                return True
        except AttributeError:
            # For Python <3.9: emulate is_relative_to
            try:
                path.resolve().relative_to(target.resolve())
                return True
            except Exception:
                pass
    return False


def discover_files() -> Iterable[Path]:
    for target in SCAN_TARGETS:
        if target.is_file():
            yield target
        elif target.exists():
            yield from target.rglob("*.md")



def categorize(path: Path, text: str) -> str:
    lower = f"{path} {text}".lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in lower for kw in kws):
            return cat
    return "Docs/Build"


def extract_tasks(file: Path) -> List[Dict[str, str]]:
    tasks: List[Dict[str, str]] = []
    section: Optional[str] = None
    in_code = False
    max_tasks = 20
    with file.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if line.startswith("#"):
                section = line.strip().lstrip("# ")
            if KEYWORD_RE.search(line) and MAIN_RE.search(line):
                title = line.strip()
                tags = [m.group(0) for m in KEYWORD_RE.finditer(line)]
                cat = categorize(file, line)
                source = f"{file}#{section or line_no}"
                task_id = hashlib.md5(f"{source}{title}".encode()).hexdigest()[:8]
                tasks.append(
                    {
                        "id": task_id,
                        "category": cat,
                        "source": source,
                        "title": title,
                        "status": "todo",
                        "tags": tags,
                        "acceptance": "",
                    }
                )
                if len(tasks) >= max_tasks:
                    break
    return tasks


def merge_tasks(existing: Dict[str, Dict[str, str]], new_tasks: Iterable[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    for task in new_tasks:
        existing.setdefault(task["id"], task)
    return existing


def update_status(tasks: Dict[str, Dict[str, str]]) -> None:
    for t in tasks.values():
        check = DONE_CHECKS.get(t["category"], lambda: False)
        if check():
            t["status"] = "done"


def load_tracker() -> Dict[str, Dict[str, str]]:
    if TRACKER_PATH.exists():
        with TRACKER_PATH.open() as fh:
            data = json.load(fh)
        return {item["id"]: item for item in data.get("tasks", [])}
    return {}


def save_tracker(tasks: Dict[str, Dict[str, str]]) -> None:
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {"tasks": list(tasks.values())}
    with TRACKER_PATH.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan docs and update TRACKER.json")
    parser.add_argument("--dry-run", action="store_true", help="do not write tracker")
    args = parser.parse_args()

    existing = load_tracker()
    all_tasks: Dict[str, Dict[str, str]] = existing.copy()
    for file in discover_files():
        for task in extract_tasks(file):
            all_tasks.setdefault(task["id"], task)
    update_status(all_tasks)

    if args.dry_run:
        print(json.dumps({"tasks": list(all_tasks.values())}, indent=2))
    else:
        save_tracker(all_tasks)
        print(f"[scan] wrote {TRACKER_PATH}")


if __name__ == "__main__":
    main()
