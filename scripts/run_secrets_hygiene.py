#!/usr/bin/env python3
"""Secrets hygiene scanner for InfoTerminal.

This script scans the working tree and full Git history for common secret
patterns, normalises the findings, and writes deterministic artefacts under
``artifacts/security/secrets``. Findings are matched against the
``policy/secrets_allowlist.json`` allowlist; new (non-allowlisted) secrets cause
the script to exit with status ``1``. Historical allowlisted findings surface as
warnings but do not fail the command.

Usage::

    python scripts/run_secrets_hygiene.py

Helpful flags::

    --worktree-only     # scan only the current working tree (skip history)
    --history-only      # scan only the Git history
    --allowlist PATH    # use a custom allowlist file
    --reports-dir PATH  # change the artefact directory (default artifacts/security/secrets)
    --dry-run           # run detection without generating artefacts / mutating files

The scanner is intentionally lightweight (regex-based) so it runs without
external dependencies in local and CI environments. For higher signal you can
pair it with ``gitleaks`` or similar tools, but this script establishes the
baseline guardrail and CI gate for R3a.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALLOWLIST = REPO_ROOT / "policy" / "secrets_allowlist.json"
DEFAULT_REPORT_DIR = REPO_ROOT / "artifacts" / "security" / "secrets"
DEFAULT_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

EXCLUDED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "node_modules",
    "artifacts",
    "build",
    "dist",
    "tmp",
    "venv",
    "__pycache__",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".7z",
    ".mp3",
    ".mp4",
    ".mov",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".sqlite",
}


@dataclass(frozen=True)
class Pattern:
    name: str
    regex: re.Pattern[str]
    group: Optional[str] = None


@dataclass
class Finding:
    pattern: str
    fingerprint: str
    path: str
    line: Optional[int]
    commit: Optional[str]
    preview: str
    kind: str  # "worktree" or "history"
    metadata: Dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "pattern": self.pattern,
            "fingerprint": self.fingerprint,
            "path": self.path,
            "line": self.line,
            "commit": self.commit,
            "preview": self.preview,
            "kind": self.kind,
        }
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass
class AllowEntry:
    fingerprint: str
    reason: str
    scope: str  # "any", "history", or "worktree"
    expires: Optional[dt.datetime]
    owner: Optional[str]
    comment: Optional[str]

    def is_expired(self, now: dt.datetime) -> bool:
        if self.expires is None:
            return False
        return self.expires < now


def load_allowlist(path: Path) -> Tuple[Dict[str, List[AllowEntry]], Dict[str, object]]:
    if not path.exists():
        return ({}, {"metadata": {"note": "allowlist file missing"}, "entries": []})
    raw = json.loads(path.read_text("utf-8"))
    metadata = raw.get("metadata", {})
    entries: Dict[str, List[AllowEntry]] = {}
    for entry in raw.get("entries", []):
        fingerprint = entry.get("fingerprint")
        if not fingerprint:
            continue
        scope = (entry.get("scope") or "any").lower()
        reason = entry.get("reason") or ""
        owner = entry.get("owner")
        comment = entry.get("comment")
        expires_raw = entry.get("expires")
        expires = None
        if expires_raw:
            try:
                expires = dt.datetime.fromisoformat(expires_raw.replace("Z", "+00:00"))
            except ValueError:
                pass
        allow_entry = AllowEntry(
            fingerprint=fingerprint,
            reason=reason,
            scope=scope,
            expires=expires,
            owner=owner,
            comment=comment,
        )
        entries.setdefault(fingerprint, []).append(allow_entry)
    return entries, metadata


def compile_patterns() -> Sequence[Pattern]:
    patterns: List[Tuple[str, str, Optional[str]]] = [
        ("aws_access_key_id", r"AKIA[0-9A-Z]{16}", None),
        ("aws_secret_key", r"(?i)aws[_-]?(?:secret|access)?[_-]?key\s*[:=]\s*['\"]?(?P<secret>[A-Za-z0-9/+]{40})['\"]?", "secret"),
        ("github_token", r"gh[oprsu]_[0-9A-Za-z]{36,}", None),
        ("high_entropy_assignment", r"(?i)(?:api|access|bearer|client|license|secret|session|token)[_-]?(?:key|token|secret)?\s*[:=]\s*['\"]?(?P<secret>[A-Za-z0-9+/=]{24,})['\"]?", "secret"),
        ("google_api_key", r"AIza[0-9A-Za-z\-_]{35}", None),
        ("private_key_block", r"-----BEGIN (?:RSA|DSA|EC|PGP|OPENSSH)? ?PRIVATE KEY-----", None),
        ("slack_token", r"xox[baprs]-[0-9A-Za-z-]{10,}", None),
        ("stripe_key", r"sk_(?:live|test)_[0-9A-Za-z]{24,}", None),
        ("twilio_key", r"SK[0-9a-fA-F]{32}", None),
        ("firebase_key", r"AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}", None),
    ]
    return [Pattern(name, re.compile(pattern), group) for name, pattern, group in patterns]


def is_binary_path(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        with path.open("rb") as handle:
            chunk = handle.read(2048)
            if b"\0" in chunk:
                return True
    except (OSError, IOError):
        return True
    return False


def should_exclude(path: Path) -> bool:
    parts = path.parts
    for segment in parts:
        if segment in EXCLUDED_DIRS:
            return True
    return False


def redact_preview(secret: str) -> str:
    clean = secret.strip()
    if len(clean) <= 6:
        return "***"
    return f"{clean[:2]}***{clean[-2:]}"


def fingerprint_secret(secret: str, pattern_name: str) -> str:
    digest = hashlib.sha256(f"{pattern_name}|{secret}".encode("utf-8", errors="ignore")).hexdigest()
    return f"sha256:{digest}"


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    freq: Dict[str, int] = {}
    for char in value:
        freq[char] = freq.get(char, 0) + 1
    length = float(len(value))
    entropy = 0.0
    for count in freq.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy


def is_high_entropy(secret: str) -> bool:
    if len(secret) < 24:
        return False
    entropy = shannon_entropy(secret)
    if entropy < 3.5:
        return False
    if not any(c.isupper() for c in secret):
        return False
    categories = 0
    if any(c.islower() for c in secret):
        categories += 1
    if any(c.isdigit() for c in secret):
        categories += 1
    if any(not c.isalnum() for c in secret):
        categories += 1
    return categories >= 2



def scan_worktree(patterns: Sequence[Pattern], root: Path) -> List[Finding]:
    findings: List[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(root)
        if should_exclude(rel_path):
            continue
        if is_binary_path(path):
            continue
        try:
            text = path.read_text("utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern in patterns:
                for match in pattern.regex.finditer(line):
                    secret = match.group(pattern.group) if pattern.group else match.group(0)
                    if pattern.name == "high_entropy_assignment" and not is_high_entropy(secret):
                        continue
                    fingerprint = fingerprint_secret(secret, pattern.name)
                    findings.append(
                        Finding(
                            pattern=pattern.name,
                            fingerprint=fingerprint,
                            path=str(rel_path),
                            line=lineno,
                            commit=None,
                            preview=redact_preview(secret),
                            kind="worktree",
                        )
                    )
    return findings


def parse_new_line_start(hunk_header: str) -> Optional[int]:
    match = re.search(r"\+(\d+)", hunk_header)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def scan_history(patterns: Sequence[Pattern], root: Path) -> List[Finding]:
    findings: List[Finding] = []
    cmd = [
        "git",
        "log",
        "--all",
        "-p",
        "--pretty=format:commit %H",
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
        bufsize=1,
    )
    assert proc.stdout is not None
    current_commit: Optional[str] = None
    current_file: Optional[str] = None
    current_line: Optional[int] = None
    for raw_line in proc.stdout:
        line = raw_line.rstrip("\n")
        if line.startswith("commit "):
            current_commit = line.split(" ", 1)[1]
            current_file = None
            current_line = None
            continue
        if line.startswith("diff --git"):
            current_file = None
            current_line = None
            continue
        if line.startswith("+++ b/"):
            file_path = line[6:]
            if file_path == "/dev/null":
                current_file = None
                current_line = None
            else:
                rel = Path(file_path)
                if should_exclude(rel):
                    current_file = None
                    current_line = None
                else:
                    current_file = file_path
                    current_line = None
            continue
        if line.startswith("@@"):
            current_line = parse_new_line_start(line)
            continue
        if not current_file or current_line is None:
            if line.startswith("Binary files"):
                current_file = None
                current_line = None
            continue
        if line.startswith("+++"):
            continue
        if line.startswith("+"):
            content = line[1:]
            for pattern in patterns:
                for match in pattern.regex.finditer(content):
                    secret = match.group(pattern.group) if pattern.group else match.group(0)
                    if pattern.name == "high_entropy_assignment" and not is_high_entropy(secret):
                        continue
                    fingerprint = fingerprint_secret(secret, pattern.name)
                    findings.append(
                        Finding(
                            pattern=pattern.name,
                            fingerprint=fingerprint,
                            path=current_file,
                            line=current_line,
                            commit=current_commit,
                            preview=redact_preview(secret),
                            kind="history",
                        )
                    )
            current_line += 1
            continue
        if line.startswith(" "):
            current_line += 1
            continue
    proc.wait()
    if proc.returncode not in (0, 141):  # 141 == SIGPIPE when piping output
        err = proc.stderr.read() if proc.stderr else ""
        raise RuntimeError(f"git log scan failed with {proc.returncode}: {err}")
    return findings


@dataclass
class Classification:
    new_findings: List[Finding]
    accepted_findings: List[Tuple[Finding, AllowEntry]]
    expired_findings: List[Tuple[Finding, AllowEntry]]


def classify_findings(
    findings: Iterable[Finding],
    allowlist_index: Dict[str, List[AllowEntry]],
    scope: str,
    now: dt.datetime,
) -> Classification:
    new: List[Finding] = []
    accepted: List[Tuple[Finding, AllowEntry]] = []
    expired: List[Tuple[Finding, AllowEntry]] = []
    scope_key = scope.lower()
    for finding in findings:
        entries = allowlist_index.get(finding.fingerprint, [])
        matched_entry: Optional[AllowEntry] = None
        for entry in entries:
            if entry.scope in ("any", scope_key):
                matched_entry = entry
                break
        if not matched_entry:
            new.append(finding)
            continue
        if matched_entry.is_expired(now):
            expired.append((finding, matched_entry))
        else:
            accepted.append((finding, matched_entry))
    return Classification(new, accepted, expired)


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path: Path, lines: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_summary(
    worktree: Classification,
    history: Classification,
    metadata: Dict[str, object],
    now: dt.datetime,
) -> Dict[str, object]:
    status = "pass"
    if worktree.new_findings or history.new_findings or worktree.expired_findings or history.expired_findings:
        status = "fail"
    elif worktree.accepted_findings or history.accepted_findings:
        status = "warn"
    summary = {
        "generated_at": now.strftime(DEFAULT_TIMESTAMP_FORMAT),
        "status": status,
        "worktree": {
            "new": len(worktree.new_findings),
            "accepted": len(worktree.accepted_findings),
            "expired": len(worktree.expired_findings),
        },
        "history": {
            "new": len(history.new_findings),
            "accepted": len(history.accepted_findings),
            "expired": len(history.expired_findings),
        },
        "metadata": metadata,
    }
    return summary


def classify_to_payload(classification: Classification) -> Dict[str, object]:
    return {
        "new": [finding.as_dict() for finding in classification.new_findings],
        "accepted": [
            {**finding.as_dict(), "allow_reason": entry.reason, "allow_scope": entry.scope, "allow_owner": entry.owner}
            for finding, entry in classification.accepted_findings
        ],
        "expired": [
            {**finding.as_dict(), "allow_reason": entry.reason, "allow_scope": entry.scope, "allow_owner": entry.owner}
            for finding, entry in classification.expired_findings
        ],
    }


def make_pr_comment(summary: Dict[str, object]) -> List[str]:
    status = summary["status"]
    emoji = {"pass": "✅", "warn": "⚠️", "fail": "❌"}.get(status, "ℹ️")
    lines = [
        f"{emoji} **Secrets hygiene status:** {status.upper()}",
        "",
        "| Scope | New | Accepted | Expired |",
        "| --- | --- | --- | --- |",
        f"| Worktree | {summary['worktree']['new']} | {summary['worktree']['accepted']} | {summary['worktree']['expired']} |",
        f"| History | {summary['history']['new']} | {summary['history']['accepted']} | {summary['history']['expired']} |",
    ]
    if status == "fail":
        lines.append("\n> Remove newly detected secrets or extend the allowlist with justification (expired entries count as failures).")
    elif status == "warn":
        lines.append("\n> Allowlisted secrets remain in history. Review `artifacts/security/secrets/` for details and plan remediation.")
    return lines


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run InfoTerminal secrets hygiene checks.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--worktree-only", action="store_true", help="Scan only the current working tree.")
    group.add_argument("--history-only", action="store_true", help="Scan only the Git history.")
    parser.add_argument("--allowlist", default=str(DEFAULT_ALLOWLIST), help="Path to secrets allowlist JSON file.")
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORT_DIR), help="Directory for generated artefacts.")
    parser.add_argument("--dry-run", action="store_true", help="Run detection without writing artefacts.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    allowlist_path = Path(args.allowlist)
    reports_dir = Path(args.reports_dir)
    now = dt.datetime.now(dt.timezone.utc)

    allowlist_index, allowlist_metadata = load_allowlist(allowlist_path)
    patterns = compile_patterns()

    scan_worktree_flag = not args.history_only
    scan_history_flag = not args.worktree_only

    worktree_findings: List[Finding] = []
    history_findings: List[Finding] = []

    if scan_worktree_flag:
        worktree_findings = scan_worktree(patterns, REPO_ROOT)
    if scan_history_flag:
        history_findings = scan_history(patterns, REPO_ROOT)

    worktree_classification = classify_findings(worktree_findings, allowlist_index, "worktree", now)
    history_classification = classify_findings(history_findings, allowlist_index, "history", now)

    summary = build_summary(worktree_classification, history_classification, allowlist_metadata, now)
    metadata_timestamp = allowlist_metadata.get("last_reviewed")
    if isinstance(metadata_timestamp, str) and metadata_timestamp:
        summary["generated_at"] = metadata_timestamp if "T" in metadata_timestamp else f"{metadata_timestamp}T00:00:00Z"

    summary_path = reports_dir / "summary.json"
    if args.dry_run:
        print(json.dumps(summary, indent=2))
    else:
        reports_dir.mkdir(parents=True, exist_ok=True)
        write_json(summary_path, summary)
        write_json(reports_dir / "findings_worktree.json", classify_to_payload(worktree_classification))
        write_json(reports_dir / "findings_history.json", classify_to_payload(history_classification))
        write_markdown(reports_dir / "pr_comment.md", make_pr_comment(summary))
        write_markdown(
            reports_dir / "README.md",
            [
                "# Secrets Hygiene Artefacts",
                "",
                "- `summary.json`: Gate status (pass/warn/fail) and aggregate counts.",
                "- `findings_worktree.json`: Detailed findings for the current working tree.",
                "- `findings_history.json`: Findings discovered in Git history (added lines).",
                "- `pr_comment.md`: Markdown summary used by CI for PR comments.",
                "",
                "Accepted findings are tracked in `policy/secrets_allowlist.json`. Update that file to document false positives or accepted historical exposures.",
            ],
        )

    exit_code = 0
    if summary["status"] == "fail":
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
