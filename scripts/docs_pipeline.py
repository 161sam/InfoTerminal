#!/usr/bin/env python3
"""Docs consolidation helper.

This script provides three subcommands:
- analyze: generate tree, inventories, TODO index, duplicates report, link and naming checks
- consolidate: ensure target docs structure and index README files
- dedupe: placeholder for future deduplication logic

The script is intentionally simple and focuses on idempotent behaviour. It writes
all analysis artifacts to WORK-ON-new_docs/out/.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import textwrap
from pathlib import Path
import json
import zipfile
from datetime import datetime
from typing import List, Tuple
import difflib

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
WORK_DIR = REPO_ROOT / "WORK-ON-new_docs"
OUT_DIR = WORK_DIR / "out"
JOURNAL_FILE = OUT_DIR / "migration_journal.md"

MD_LINK_RE = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)")
CHECKBOX_RE = re.compile(r"- \[( |x)\] .*")
TODO_RE = re.compile(r"\b(TODO|FIXME|NOTE):?\b", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#+)\s+(.*)")


def ensure_out_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def hash_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def analyze() -> None:
    ensure_out_dir()
    # optional extraction of analysis zip
    zip_path = WORK_DIR / "InfoTerminal-analysis-reports.zip"
    target_ws = WORK_DIR / "_analysis_ws"
    if zip_path.exists() and not target_ws.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(target_ws)
    tree_lines: List[str] = []
    inventory_lines: List[str] = ["# Inventory of blueprints/yaml/json\n\n"]
    todo_lines: List[str] = ["# TODO index\n\n"]
    duplicates: List[Tuple[str, str, str]] = []  # (file, heading, hash)
    sections = []  # list of (norm_text, file, heading, start_line, end_line)

    # walk docs
    for root, _, files in os.walk(DOCS_DIR):
        rel_root = Path(root).relative_to(REPO_ROOT)
        indent = "  " * len(rel_root.parts)
        tree_lines.append(f"{indent}{rel_root}/")
        for fname in sorted(files):
            fpath = Path(root) / fname
            rel_path = fpath.relative_to(REPO_ROOT)
            tree_lines.append(f"{indent}  {rel_path}")
            if fname.endswith(('.yaml', '.yml', '.json')) or fname.startswith('blueprint-'):
                inventory_lines.append(f"- {rel_path}")
            if fname.endswith('.md'):
                lines = fpath.read_text(encoding='utf-8').splitlines()
                if lines:
                    summary = lines[0].strip()
                    tree_lines.append(f"{indent}    > {summary}")
                for idx, line in enumerate(lines, 1):
                    if CHECKBOX_RE.search(line) or TODO_RE.search(line):
                        tid = hash_text(f"{rel_path}:{idx}:{line.strip()}")
                        todo_lines.append(f"- T{tid} {rel_path}#L{idx}: {line.strip()}")
                # section parsing for duplicates
                sec_start = None
                sec_title = None
                buf = []
                for i, line in enumerate(lines, 1):
                    m = HEADING_RE.match(line)
                    if m:
                        if sec_start is not None:
                            norm = normalize("\n".join(buf))
                            sections.append((norm, str(rel_path), sec_title, sec_start, i-1))
                        sec_title = m.group(2).strip()
                        sec_start = i
                        buf = []
                    else:
                        buf.append(line)
                if sec_start is not None:
                    norm = normalize("\n".join(buf))
                    sections.append((norm, str(rel_path), sec_title, sec_start, len(lines)))
    # duplicates detection (naive hash-based)
    seen = {}
    for norm, path, title, start, end in sections:
        h = hash_text(norm)
        if h in seen and difflib.SequenceMatcher(None, norm, seen[h][0]).ratio() >= 0.88:
            duplicates.append((seen[h][1], f"{path}#{title}", f"L{start}-L{end}"))
        else:
            seen[h] = (norm, f"{path}#{title}")
    dup_lines = ["# Potential duplicate sections\n\n"]
    for a, b, lines in duplicates:
        dup_lines.append(f"- {a} <-> {b} ({lines})")

    write_file(OUT_DIR / "tree_with_summaries.txt", "\n".join(tree_lines) + "\n")
    write_file(OUT_DIR / "inventory_blueprints_yaml_json.md", "\n".join(inventory_lines) + "\n")
    write_file(OUT_DIR / "todo_index.md", "\n".join(todo_lines) + "\n")
    write_file(OUT_DIR / "duplicates_report.md", "\n".join(dup_lines) + "\n")

    check_broken_links()
    check_naming()


def normalize(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(MD_LINK_RE, lambda m: m.group('text'), text)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text)
    return " ".join(text.lower().split())


def consolidate() -> None:
    ensure_out_dir()
    entries = []
    targets = [
        "architecture/diagrams",
        "blueprints",
        "dev/guides",
        "dev/research",
        "dev/roadmap/v0.3-plus",
        "integrations",
        "presets/waveterm",
        "runbooks",
        "user",
    ]
    for t in targets:
        path = DOCS_DIR / t
        if not path.exists():
            path.mkdir(parents=True)
            entries.append(f"- ACTION: mkdir\n  DST: docs/{t}\n  WHY: ensure structure")
    if entries:
        content = "\n".join(entries) + "\n"
        if JOURNAL_FILE.exists():
            JOURNAL_FILE.write_text(JOURNAL_FILE.read_text(encoding="utf-8") + content, encoding="utf-8")
        else:
            write_file(JOURNAL_FILE, content)


def dedupe() -> None:
    ensure_out_dir()
    # Placeholder: In a full implementation, duplicate sections would be merged.
    note = textwrap.dedent(
        """
        Dedupe step not yet implemented. See duplicates_report.md for candidates.
        """
    )
    write_file(OUT_DIR / "dedupe_placeholder.txt", note)


def check_broken_links() -> None:
    lines = ["# Broken markdown links\n\n"]
    for md in DOCS_DIR.rglob("*.md"):
        content = md.read_text(encoding="utf-8")
        for m in MD_LINK_RE.finditer(content):
            target = m.group("target")
            if target.startswith("http"):
                continue
            target_path = (md.parent / target).resolve()
            if not target_path.exists():
                rel = md.relative_to(REPO_ROOT)
                lines.append(f"- {rel}: broken link to {target}")
    write_file(OUT_DIR / "broken_links.md", "\n".join(lines) + "\n")


def check_naming() -> None:
    bad = ["# Naming issues\n\n"]
    valid_re = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)?$")
    for path in DOCS_DIR.rglob("*"):
        if path.is_file():
            name = path.name
            if not valid_re.match(name):
                rel = path.relative_to(REPO_ROOT)
                bad.append(f"- {rel}")
    write_file(OUT_DIR / "naming_issues.md", "\n".join(bad) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="+", help="tasks to run")
    args = parser.parse_args()
    for task in args.tasks:
        if task == "analyze":
            analyze()
        elif task == "consolidate":
            consolidate()
        elif task == "dedupe":
            dedupe()
        else:
            raise ValueError(f"Unknown task {task}")


if __name__ == "__main__":
    main()
