#!/usr/bin/env python3
"""Scan repository docs for v0.2 related tasks and update TRACKER.json.

The script searches predefined documentation paths for keywords that hint at
open work items (e.g. TODO, FIXME, v0.2). It extracts a short description of
each match together with its source file and section and writes the collected
items to ``docs/dev/en/releases/v0.2/TRACKER.json``.

Running the script multiple times is safe; existing tasks are merged using a
stable identifier based on ``source`` and ``title``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List

TRACKER_PATH = Path("docs/dev/en/releases/v0.2/TRACKER.json")
SEARCH_ROOTS = [
    Path("docs/dev"),
    Path("docs/user"),
    Path("WORK-ON-new_docs"),
]
EXTRA_FILES = [
    Path("ROADMAP.md"),
    Path("Checkliste.md"),
    Path("docs/SECURITY_SWEEP.md"),
]
KEYWORDS = [
    r"v0\.2(?:\.\w+)?",
    "Muss",
    "Must",
    "Soll",
    "TODO",
    "FIXME",
    "WIP",
    "pre-release",
    "legacy",
]
KEYWORD_RE = re.compile(r"|".join(KEYWORDS), re.IGNORECASE)


def categorize(path: Path) -> str:
    """Return the high level category for a file path."""
    p = path.as_posix().lower()
    if any(k in p for k in ["nlp", "doc-entities"]):
        return "NLP"
    if any(k in p for k in ["graph", "ontology"]):
        return "Graph"
    if "search" in p:
        return "Search"
    if any(k in p for k in ["dossier", "report"]):
        return "Dossier"
    if any(k in p for k in ["geo", "geospatial"]):
        return "Geospatial"
    if any(k in p for k in ["security", "gateway", "oidc", "opa", "jwt"]):
        return "Security/Ops"
    if any(k in p for k in ["automation", "agent", "flowise", "n8n"]):
        return "Automation/Agent"
    return "Docs/Build"


def iter_files() -> List[Path]:
    files: set[Path] = set()
    for root in SEARCH_ROOTS:
        if root.exists():
            for p in root.rglob("*.md"):
                posix = p.as_posix()
                if "InfoTerminal-analysis-reports" in posix:
                    continue
                if "WORK-ON-new_docs" in posix and any(
                    part.startswith("InfoTerminal-") for part in p.parts
                ):
                    continue
                files.add(p)
    for extra in EXTRA_FILES:
        if extra.exists():
            files.add(extra)
    return sorted(files)


def scan_file(path: Path) -> List[Dict[str, str]]:
    """Yield matches found in ``path``."""
    matches = []
    heading = ""
    in_code = False
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return matches
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
        if not stripped.startswith(("-", "*")):
            continue
        if KEYWORD_RE.search(stripped):
            tags = [t.lower() for t in KEYWORD_RE.findall(stripped)]
            matches.append(
                {
                    "heading": heading,
                    "text": stripped,
                    "tags": tags,
                }
            )
    return matches


def load_tracker() -> Dict[str, Dict]:
    if not TRACKER_PATH.exists():
        return {}
    data = json.loads(TRACKER_PATH.read_text())
    return {task["id"]: task for task in data.get("tasks", [])}


def write_tracker(tasks: Dict[str, Dict]) -> None:
    out = {"tasks": sorted(tasks.values(), key=lambda t: (t["category"], t["id"]))}
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRACKER_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")


def build_id(source: str, title: str) -> str:
    return hashlib.md5(f"{source}:{title}".encode("utf-8")).hexdigest()[:8]


def scan() -> None:
    tracker = load_tracker()
    for path in iter_files():
        matches = scan_file(path)
        if not matches:
            continue
        for m in matches:
            heading = m["heading"]
            source = f"{path.as_posix()}#{heading}" if heading else path.as_posix()
            title = m["text"]
            tid = build_id(source, title)
            category = categorize(path)
            existing = tracker.get(tid, {})
            tracker[tid] = {
                "id": tid,
                "category": category,
                "source": source,
                "title": title,
                "status": existing.get("status", "todo"),
                "tags": m["tags"],
                "acceptance": existing.get("acceptance", ""),
            }
    write_tracker(tracker)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan docs and update TRACKER.json")
    parser.add_argument("--dry-run", action="store_true", help="only print stats")
    args = parser.parse_args()
    if args.dry_run:
        files = iter_files()
        print(f"Found {len(files)} files to scan")
        total = 0
        for path in files:
            matches = scan_file(path)
            if matches:
                print(f"{path}: {len(matches)} matches")
                total += len(matches)
        print(f"Total matches: {total}")
    else:
        scan()


if __name__ == "__main__":
    main()
