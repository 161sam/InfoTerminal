#!/usr/bin/env python3
"""Documentation consolidation helper.

The script implements three subcommands which may be chained:

```
python3 scripts/docs_pipeline.py analyze consolidate dedupe
```

* ``analyze`` – generate inventories, TODO index, duplicate report and
  a tree view of ``docs/``. Results are written to ``WORK-ON-new_docs/out``.
* ``consolidate`` – ensure the target folder structure, move a couple of
  legacy files to their canonical location and update index files. It also
  integrates tasks from ``todo_index.md`` into roadmap overviews.
* ``dedupe`` – merge duplicate sections into canonical targets while
  inserting provenance front‑matter and rewriting the source location with a
  pointer.

The implementation favours idempotency: running the same command multiple
 times yields the same output.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from difflib import SequenceMatcher
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
WORK_DIR = REPO_ROOT / "WORK-ON-new_docs"
OUT_DIR = WORK_DIR / "out"
JOURNAL_FILE = OUT_DIR / "migration_journal.md"

MD_LINK_RE = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)")
CHECKBOX_RE = re.compile(r"- \[( |x|X)\] .*")
TODO_RE = re.compile(r"\b(TODO|FIXME|NOTE):?\b")
HEADING_RE = re.compile(r"^(#+)\s+(.*)")


def ensure_out_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def append_journal(entry: str) -> None:
    JOURNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = ""
    if JOURNAL_FILE.exists():
        existing = JOURNAL_FILE.read_text(encoding="utf-8")
    if entry in existing:
        return
    with JOURNAL_FILE.open("a", encoding="utf-8") as fh:
        fh.write(entry + "\n")


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------


def hash_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def normalize(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(MD_LINK_RE, lambda m: m.group("text"), text)
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def first_nonempty_line(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                return line
    except Exception:
        pass
    return ""


def analyze() -> None:
    ensure_out_dir()
    tree_lines: List[str] = []
    inventory_lines: List[str] = ["# Inventory of blueprints/yaml/json\n"]
    todo_rows: List[Tuple[str, str, int, str]] = []
    sections: List[Tuple[str, str, str, int, int]] = []

    for root, dirs, files in os.walk(DOCS_DIR):
        rel_root = Path(root).relative_to(DOCS_DIR)
        indent = "  " * len(rel_root.parts)
        tree_lines.append(f"{indent}{rel_root.name}/" if rel_root.parts else "docs/")
        for fname in sorted(files):
            fpath = Path(root) / fname
            rel_path = fpath.relative_to(REPO_ROOT)
            if fpath.suffix.lower() in {".yaml", ".yml", ".json"} or fname.startswith(
                "blueprint-"
            ):
                inventory_lines.append(f"- {rel_path}")
            if fpath.suffix.lower() == ".md":
                summary = first_nonempty_line(fpath)
                tree_lines.append(f"{indent}  {fname} :: {summary}")
                lines = fpath.read_text(encoding="utf-8").splitlines()
                for idx, line in enumerate(lines, 1):
                    if CHECKBOX_RE.search(line) or TODO_RE.search(line):
                        todo_rows.append(
                            (
                                str(rel_path),
                                line.strip(),
                                idx,
                                hash_text(f"{rel_path}:{idx}:{line.strip()}"),
                            )
                        )
                start = 1
                title = "<start>"
                buf: List[str] = []
                for i, line in enumerate(lines, 1):
                    m = HEADING_RE.match(line)
                    if m:
                        if buf:
                            norm = normalize("\n".join(buf))
                            sections.append((norm, str(rel_path), title, start, i - 1))
                        title = m.group(2).strip()
                        start = i
                        buf = []
                    else:
                        buf.append(line)
                if buf:
                    norm = normalize("\n".join(buf))
                    sections.append((norm, str(rel_path), title, start, len(lines)))

    write_file(OUT_DIR / "tree_with_summaries.txt", "\n".join(tree_lines) + "\n")
    write_file(
        OUT_DIR / "inventory_blueprints_yaml_json.md", "\n".join(inventory_lines) + "\n"
    )

    todo_lines = ["| ID | File | Line | Text |", "|---|---|---|---|"]
    for i, (path, text, line_no, digest) in enumerate(todo_rows, 1):
        tid = f"T{i:04d}-{digest[:8]}"
        todo_lines.append(
            f"| {tid} | {path} | {line_no} | {text.replace('|', '\\\\|')} |"
        )
    write_file(OUT_DIR / "todo_index.md", "\n".join(todo_lines) + "\n")

    dup_lines = ["# Potential duplicate sections\n"]
    seen: Dict[str, Tuple[str, str, int, int]] = {}
    for norm, path, title, start, end in sections:
        if not norm.strip():
            continue
        key = norm[:100]
        if key in seen:
            norm2, path2, title2, start2, end2 = seen[key]
            if SequenceMatcher(None, norm, norm2).ratio() >= 0.88:
                dup_lines.append(
                    f"- {path2}#L{start2}-L{end2} ({title2}) <-> {path}#L{start}-L{end} ({title})"
                )
                continue
        seen[key] = (norm, path, title, start, end)
    write_file(OUT_DIR / "duplicates_report.md", "\n".join(dup_lines) + "\n")

    check_broken_links()
    check_naming()


# ---------------------------------------------------------------------------
# Consolidation helpers
# ---------------------------------------------------------------------------


def move_with_provenance(src: Path, dst: Path, why: str) -> None:
    if not src.exists() or dst.exists():
        return
    content = src.read_text(encoding="utf-8")
    lines = content.splitlines()
    fm = [
        "---",
        "merged_from:",
        f"  - {src.relative_to(REPO_ROOT)}#L1-L{len(lines)}",
        f"merged_at: {datetime.utcnow().isoformat()}Z",
        "---",
        "",
    ]
    write_file(dst, "\n".join(fm) + content)
    src.unlink()
    append_journal(
        "- ACTION: move\n  SRC: {0}\n  DST: {1}\n  WHY: {2}\n  DIFF: moved".format(
            src.relative_to(REPO_ROOT), dst.relative_to(REPO_ROOT), why
        )
    )


def ensure_docs_readme() -> None:
    path = DOCS_DIR / "README.md"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8").splitlines()
    start_marker = "<!-- GENERATED-QUICKLINKS -->"
    end_marker = "<!-- /GENERATED-QUICKLINKS -->"
    links = [
        start_marker,
        "* [Architecture](architecture/)",
        "* [Blueprints](blueprints/)",
        "* [Dev](dev/)",
        "* [Integrations](integrations/)",
        "* [Presets](presets/)",
        "* [Runbooks](runbooks/)",
        "* [User Guide](user/)",
        end_marker,
    ]
    try:
        i = content.index(start_marker)
        j = content.index(end_marker) + 1
        new_content = content[:i] + links + content[j:]
    except ValueError:
        for idx, line in enumerate(content):
            if line.startswith("#"):
                break
        new_content = content[: idx + 1] + [""] + links + [""] + content[idx + 1 :]
    write_file(path, "\n".join(new_content) + "\n")


def ensure_blueprints_readme() -> None:
    path = DOCS_DIR / "blueprints/README.md"
    if not path.parent.exists():
        return
    lines = ["# Blueprints", ""]
    for f in sorted(path.parent.glob("blueprint-*.md")):
        lines.append(f"- [{f.stem}](./{f.name})")
    write_file(path, "\n".join(lines) + "\n")


def ensure_presets_readme() -> None:
    path = DOCS_DIR / "presets/README.md"
    if not path.parent.exists():
        return
    lines = ["# Preset Profiles", ""]
    for f in sorted(path.parent.glob("profile-*.yml")) + sorted(
        path.parent.glob("profile-*.yaml")
    ):
        lines.append(f"- `{f.name}`")
    if (path.parent / "waveterm").exists():
        lines.append("- [waveterm/](waveterm/)")
    write_file(path, "\n".join(lines) + "\n")


def ensure_integrations_readme() -> None:
    path = DOCS_DIR / "integrations/README.md"
    if not path.parent.exists():
        return
    lines = ["# Integrations", ""]
    for d in sorted(p for p in path.parent.iterdir() if p.is_dir()):
        md_files = sorted(d.glob("*.md"))
        if md_files:
            lines.append(f"- [{d.name}](./{d.name}/{md_files[0].name})")
        else:
            lines.append(f"- {d.name}/")
    write_file(path, "\n".join(lines) + "\n")


def load_todo_tasks() -> List[Tuple[str, Path, int, str, bool]]:
    """Return tasks from the generated ``todo_index.md``.

    The file is created by the ``analyze`` step.  Each line is a pipe separated
    row containing the task id, the source file, the line number and the raw
    todo text.  Tasks from the roadmap overview files are skipped to avoid
    self‑references.
    """

    todo_file = OUT_DIR / "todo_index.md"
    tasks: List[Tuple[str, Path, int, str, bool]] = []
    if not todo_file.exists():
        return tasks
    for line in todo_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("| T"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) != 4:
            continue
        task_id, file_path, line_no, text = parts
        if file_path.startswith("docs/dev/roadmap/"):
            name = Path(file_path).name
            if name in {"v0.1-overview.md", "v0.2-overview.md", "master-todo.md"}:
                # skip overview/master files to avoid self-references
                continue
        done = "[x]" in text.lower()
        text = re.sub(r"^- \[[xX ]\]\s*", "", text)
        tasks.append((task_id, Path(file_path), int(line_no), text.strip(), done))
    return tasks


def update_section(path: Path, heading: str, items: List[str]) -> Tuple[int, set[str]]:
    if not items:
        return 0, set()
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        title = path.stem.replace("-", " ").title()
        lines = [f"# {title}", ""]
    heading_line = f"## {heading}"
    try:
        idx = lines.index(heading_line)
    except ValueError:
        lines.extend(["", heading_line, ""])
        idx = lines.index(heading_line)
    insert_at = idx + 1
    if insert_at < len(lines) and not lines[insert_at].startswith("-"):
        if lines[insert_at].strip() == "":
            insert_at += 1
    while insert_at < len(lines) and lines[insert_at].startswith("-"):
        insert_at += 1
    id_re = re.compile(r"^- \[[xX ]\]\s*(T\d{4}-[0-9a-f]{8})")
    existing_ids = set()
    for l in lines[idx + 1 : insert_at]:
        m = id_re.match(l)
        if m:
            existing_ids.add(m.group(1))
    added = 0
    inserted_ids: set[str] = set()
    for item in items:
        m = id_re.match(item)
        if not m:
            continue
        tid = m.group(1)
        if tid in existing_ids:
            continue
        lines.insert(insert_at, item)
        existing_ids.add(tid)
        inserted_ids.add(tid)
        insert_at += 1
        added += 1
    write_file(path, "\n".join(lines) + "\n")
    return added, inserted_ids


def _detect_version(path: Path) -> str | None:
    """Return version marker ``1``/``2``/``3`` if the path references it.

    The matcher is deliberately fuzzy and scans the entire path for substrings
    like ``v0.1`` or ``v0.3-plus``.  ``None`` is returned when no marker is
    present which keeps the consolidation idempotent.
    """

    lower = path.as_posix().lower()
    if "v0.1" in lower:
        return "1"
    if "v0.2" in lower:
        return "2"
    if "v0.3-plus" in lower or "v0.3" in lower:
        return "3"
    return None


def integrate_todo_tasks() -> int:
    """Integrate tasks from ``todo_index.md`` into roadmap overview files."""

    tasks = load_todo_tasks()
    v01: List[str] = []
    v02: List[str] = []
    master: List[str] = []
    for task_id, fpath, line_no, text, done in tasks:
        version = _detect_version(fpath)
        if not version:
            continue
        rel = fpath.as_posix()
        bullet = f"- [{'x' if done else ' '}] {task_id} {text} ({rel}:{line_no})"
        if version == "1" and done:
            v01.append(bullet)
        if version == "2" and not done:
            v02.append(bullet)
        # All versioned tasks (including v0.3+) are tracked in the master list
        master.append(bullet)

    # Keep deterministic ordering across runs for idempotency
    v01.sort()
    v02.sort()
    master.sort()

    added_v01, _ = update_section(
        DOCS_DIR / "dev/roadmap/v0.1-overview.md", "Abgeschlossene Detail-Tasks", v01
    )
    added_v02, _ = update_section(
        DOCS_DIR / "dev/roadmap/v0.2-overview.md", "Offene Detail-Tasks", v02
    )
    master_file = DOCS_DIR / "dev/roadmap/v0.3-plus/master-todo.md"
    added_master, _ = update_section(master_file, "Master TODO", master)
    if added_master == 0 and not master_file.exists():
        write_file(master_file, "# Master TODO\n")
    total_added = added_v01 + added_v02 + added_master
    if total_added:
        print(f"Integrated {total_added} roadmap tasks")
    else:
        print("No new roadmap tasks")
    return total_added


def ensure_roadmap_index() -> None:
    path = DOCS_DIR / "dev/roadmap/README.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Roadmap",
        "",
        "- [v0.1 overview](v0.1-overview.md)",
        "- [v0.2 overview](v0.2-overview.md)",
        "- [v0.3-plus](v0.3-plus/)",
    ]
    write_file(path, "\n".join(lines) + "\n")


def consolidate_runbook_stack() -> None:
    dst = DOCS_DIR / "runbooks/stack.md"
    if dst.exists():
        return
    src1 = DOCS_DIR / "runbooks/RUNBOOK-stack.md"
    src2 = DOCS_DIR / "OPERABILITY.md"
    parts = []
    merged_from = []
    if src1.exists():
        text1 = src1.read_text(encoding="utf-8")
        parts.append(text1)
        merged_from.append(
            f"docs/runbooks/RUNBOOK-stack.md#L1-L{len(text1.splitlines())}"
        )
    if src2.exists():
        text2 = src2.read_text(encoding="utf-8")
        parts.append(text2)
        merged_from.append(f"docs/OPERABILITY.md#L1-L{len(text2.splitlines())}")
    if not parts:
        return
    fm = (
        ["---", "merged_from:"]
        + [f"  - {m}" for m in merged_from]
        + [f"merged_at: {datetime.utcnow().isoformat()}Z", "---", ""]
    )
    write_file(dst, "\n".join(fm) + "\n\n".join(parts))
    if src1.exists():
        src1.unlink()
    if src2.exists():
        src2.unlink()
    append_journal(
        "- ACTION: merge\n  SRC: docs/runbooks/RUNBOOK-stack.md & docs/OPERABILITY.md\n  DST: docs/runbooks/stack.md\n  WHY: runbooks\n  DIFF: merged"
    )


def consolidate() -> None:
    ensure_out_dir()
    for t in [
        "architecture/diagrams",
        "blueprints",
        "dev/guides",
        "dev/research",
        "dev/roadmap/v0.3-plus",
        "integrations",
        "presets/waveterm",
        "runbooks",
        "user",
    ]:
        path = DOCS_DIR / t
        if not path.exists():
            path.mkdir(parents=True)
            append_journal(f"- ACTION: mkdir\n  DST: docs/{t}\n  WHY: ensure structure")

    move_with_provenance(
        DOCS_DIR / "testing.md", DOCS_DIR / "dev/guides/testing.md", "structure"
    )
    move_with_provenance(
        DOCS_DIR / "dev/testing.md", DOCS_DIR / "dev/guides/testing.md", "structure"
    )
    move_with_provenance(
        DOCS_DIR / "dev/RAG-Systeme.md",
        DOCS_DIR / "dev/guides/rag-systems.md",
        "structure",
    )
    move_with_provenance(
        DOCS_DIR / "dev/Frontend-Modernisierung.md",
        DOCS_DIR / "dev/guides/frontend-modernization.md",
        "structure",
    )
    move_with_provenance(
        DOCS_DIR / "dev/Frontend-Modernisierung_Setup-Guide.md",
        DOCS_DIR / "dev/guides/frontend-modernization-setup-guide.md",
        "structure",
    )
    move_with_provenance(
        DOCS_DIR / "dev/ROADMAPv0.1.0.md",
        DOCS_DIR / "dev/roadmap/v0.1-overview.md",
        "structure",
    )
    move_with_provenance(
        DOCS_DIR / "dev/Release-Planv0.2-v1.0.md",
        DOCS_DIR / "dev/roadmap/v0.2-overview.md",
        "structure",
    )
    move_with_provenance(
        DOCS_DIR / "runbooks/RUNBOOK-obs-opa-secrets.md",
        DOCS_DIR / "runbooks/obs-opa-secrets.md",
        "naming",
    )

    consolidate_runbook_stack()
    ensure_roadmap_index()
    ensure_docs_readme()
    ensure_blueprints_readme()
    ensure_presets_readme()
    ensure_integrations_readme()
    integrate_todo_tasks()


# ---------------------------------------------------------------------------
# Dedupe step – consolidate duplicate sections and fix links
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-+", "-", text)


def canonical_target(path: Path) -> Path | None:
    """Return canonical target file for a given path.

    The mapping follows a couple of simple keyword heuristics.  Only a small
    curated set of topics is consolidated which keeps the operation idempotent
    and avoids surprising moves.  Roadmap files themselves are excluded since
    they describe planning/strategy rather than content that should be merged.
    """

    rel = path.relative_to(REPO_ROOT).as_posix().lower()
    if rel.startswith("docs/dev/roadmap/"):
        # Roadmap files contain planning information and are never deduplicated
        return None

    # Keyword heuristics → canonical destinations
    rules: List[Tuple[Tuple[str, ...], Path]] = [
        (("rag",), DOCS_DIR / "dev/guides/rag-systems.md"),
        (("frontend-modernisierung",), DOCS_DIR / "dev/guides/frontend-modernization.md"),
        (("preset-profile",), DOCS_DIR / "dev/guides/preset-profiles.md"),
        (("flowise", "agent"), DOCS_DIR / "dev/guides/flowise-agents.md"),
        (("operability",), DOCS_DIR / "runbooks/stack.md"),
    ]
    for keywords, target in rules:
        if all(k in rel for k in keywords):
            return target
    return None


def find_existing_anchor(
    target: Path,
    src_rel: str,
    start: int,
    end: int,
    hashval: str,
    section: List[str],
) -> str | None:
    """Return anchor if the section was previously merged."""
    ref = f"{src_rel}#L{start}-L{end}"
    if target.exists():
        content = target.read_text(encoding="utf-8")
        if ref in content:
            return slugify(HEADING_RE.sub(r"\2", section[0]) if section else "section")
    if not JOURNAL_FILE.exists():
        return None
    target_rel = str(target.relative_to(REPO_ROOT))
    content = JOURNAL_FILE.read_text(encoding="utf-8")
    for block in content.split("- ACTION"):
        if f"DST: {target_rel}#" in block and f"HASH: {hashval}" in block:
            m = re.search(r"DST: \S+#([^\n]*)", block)
            if m:
                return m.group(1).strip()
    return None


def extract_sections(line: str) -> List[Tuple[Path, int, int]]:
    clean = re.sub(r"`[^`]*`", "", line)
    matches = re.findall(r"(docs/[^\s#]+)#L(\d+)-L(\d+)", clean)
    result = []
    for path, start, end in matches:
        result.append((REPO_ROOT / path, int(start), int(end)))
    return result


def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def replace_with_pointer(
    src: Path, start: int, end: int, target: Path, anchor: str
) -> bool:
    """Replace the source section with a pointer to the canonical target.

    Returns ``True`` when the file was modified, allowing the caller to keep the
    operation idempotent and to avoid duplicate journal entries."""

    lines = read_lines(src)
    rel_target = os.path.relpath(target, src.parent).replace(os.sep, "/")
    pointer = f"➡ Consolidated at: {rel_target}#{anchor}"
    if lines[start - 1 : end] == [pointer]:
        return False
    lines[start - 1 : end] = [pointer]
    write_file(src, "\n".join(lines) + "\n")
    return True


def append_section(
    target: Path, src_rel: str, start: int, end: int, section: List[str]
) -> str:
    if target.exists():
        tlines = read_lines(target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        tlines = [f"# {target.stem.replace('-', ' ').title()}", ""]
    ref = f"{src_rel}#L{start}-L{end}"
    if ref in "\n".join(tlines):
        # already merged
        return slugify(section[0] if section else "section") or "section"
    anchor = slugify(HEADING_RE.sub(r"\2", section[0]) if section else "section")
    if not anchor:
        anchor = "section"
    fm = [
        "---",
        "merged_from:",
        f"  - {ref}",
        f"merged_at: {datetime.utcnow().isoformat()}Z",
        "---",
        "",
    ]
    tlines.extend(fm + section)
    write_file(target, "\n".join(tlines) + "\n")
    return anchor


def dedupe() -> int:
    """Merge duplicate sections into canonical files and rewrite sources.

    The dedupe step reads ``duplicates_report.md`` and for each section pair
    determines a canonical target based on filename heuristics. Non-empty
    sections that have not yet been consolidated are appended to the target with
    provenance front-matter and a UTC timestamp. The original location is
    replaced by a short pointer linking to the merged section. The operation is
    idempotent: hashes and existing pointers are checked so running the command
    repeatedly does not create duplicates.
    """
    ensure_out_dir()
    dup_file = OUT_DIR / "duplicates_report.md"
    if not dup_file.exists():
        check_broken_links()
        check_naming()
        return 0
    processed: set[Tuple[Path, int, int]] = set()
    merged_pairs: List[Tuple[str, str]] = []
    for line in dup_file.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- "):
            continue
        sections = extract_sections(line)
        if not sections:
            continue
        # Determine canonical target for this duplicate group.  When exactly one
        # canonical mapping exists we treat the other sections as sources and
        # merge them into the canonical file.  This allows pairs like
        # ``flowise-agents.md`` <-> ``waveterm/README.md`` to be consolidated
        # even though only one side matches the heuristics.
        targets = [canonical_target(p) for p, _, _ in sections if canonical_target(p)]
        target = None
        if targets and all(t == targets[0] for t in targets):
            target = targets[0]
        if not target:
            continue
        for src, start, end in sections:
            key = (src, start, end)
            if key in processed:
                continue
            processed.add(key)
            if src == target:
                continue
            lines = read_lines(src)
            section = lines[start - 1 : end]
            if not section or section[0].startswith("➡ Consolidated at:"):
                continue
            hashval = hash_text("\n".join(section))
            src_rel = str(src.relative_to(REPO_ROOT))
            existing = find_existing_anchor(target, src_rel, start, end, hashval, section)
            was_new = False
            if existing:
                anchor = existing
            else:
                anchor = append_section(target, src_rel, start, end, section)
                was_new = True
            pointer_changed = replace_with_pointer(src, start, end, target, anchor)
            if was_new or pointer_changed:
                merged_pairs.append(
                    (
                        str(src.relative_to(REPO_ROOT)),
                        str(target.relative_to(REPO_ROOT)),
                    )
                )
                journal_entry = (
                    "- ACTION: merge+link\n"
                    f"  SRC: {src.relative_to(REPO_ROOT)}#L{start}-L{end}\n"
                    f"  DST: {target.relative_to(REPO_ROOT)}#{anchor}\n"
                    "  WHY: deduplicate\n"
                    f"  HASH: {hashval}"
                )
                append_journal(journal_entry)
    if merged_pairs:
        targets = {dst for _, dst in merged_pairs}
        print(
            f"Deduplicated {len(merged_pairs)} sections into {len(targets)} files"
        )
    else:
        print("No duplicates merged")
    check_broken_links()
    check_naming()
    return len(merged_pairs)


# ---------------------------------------------------------------------------
# QA helpers
# ---------------------------------------------------------------------------


def check_broken_links() -> None:
    lines = ["# Broken markdown links\n"]
    for md in DOCS_DIR.rglob("*.md"):
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in MD_LINK_RE.finditer(content):
            target = m.group("target")
            if target.startswith("http") or target.startswith("#"):
                continue
            target_path = (md.parent / target.split("#")[0]).resolve()
            if not target_path.exists():
                rel = md.relative_to(REPO_ROOT)
                lines.append(f"- {rel}: broken link to {target}")
    write_file(OUT_DIR / "broken_links.md", "\n".join(lines) + "\n")


def check_naming() -> None:
    bad = ["# Naming issues\n"]
    valid_re = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)?$")
    for path in DOCS_DIR.rglob("*"):
        if path.is_file():
            if not valid_re.match(path.name):
                bad.append(f"- {path.relative_to(REPO_ROOT)}")
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
