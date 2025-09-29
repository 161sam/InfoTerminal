#!/usr/bin/env python3
"""Run black and ruff on the Python files changed against a base revision."""
from __future__ import annotations

import os
import subprocess
import sys
from typing import Iterable, List, Optional


def _rev_exists(ref: str) -> bool:
    return (
        subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def _merge_base(ref: str) -> Optional[str]:
    result = subprocess.run(
        ["git", "merge-base", "HEAD", ref],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        commit = result.stdout.strip()
        if commit:
            return commit
    return None


def _determine_base() -> Optional[str]:
    candidates: List[Optional[str]] = []
    if len(sys.argv) > 1:
        candidates.append(sys.argv[1])
    env_base = os.environ.get("BASE_SHA") or os.environ.get("GITHUB_BASE_SHA")
    if env_base:
        candidates.append(env_base)
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        candidates.append(f"origin/{base_ref}")

    for candidate in candidates:
        if not candidate:
            continue
        if _rev_exists(candidate):
            return candidate
        origin_candidate = f"origin/{candidate}"
        if _rev_exists(origin_candidate):
            return origin_candidate

    if _rev_exists("origin/main"):
        merged = _merge_base("origin/main")
        if merged:
            return merged

    parent = subprocess.run(
        ["git", "rev-parse", "HEAD^"],
        capture_output=True,
        text=True,
        check=False,
    )
    if parent.returncode == 0:
        commit = parent.stdout.strip()
        if commit:
            return commit

    return None


def _collect_changed(base: str, patterns: Iterable[str]) -> List[str]:
    args = ["git", "diff", "--name-only", f"{base}...HEAD", "--", *patterns]
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return sorted({f for f in files if os.path.isfile(f)})


def _run(cmd: List[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    base = _determine_base()
    if not base:
        print("No base revision detected; skipping Python lint.")
        return 0

    files = _collect_changed(base, ["*.py"])
    if not files:
        print("No Python changes detected; skipping Python lint.")
        return 0

    print(f"Linting {len(files)} Python file(s) against base {base}.")
    _run([sys.executable, "-m", "black", "--check", *files])
    _run([sys.executable, "-m", "ruff", "check", *files])
    return 0


if __name__ == "__main__":
    sys.exit(main())
