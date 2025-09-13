# PR/Branch Diff & Merge-Conflict Analyzer

Purpose: analyze one or more PRs/branches, capture metadata and diffs (via `gh` when available), simulate merges into a base (e.g. `origin/main`) and cross-merge between the two refs, and generate `reports/DIFF_REPORT.md`. The script prints the report to stdout and cleans up temporary branches.

## Usage

- With defaults (PRS `169 168`, base `origin/main`):
  - `make pr.diff`

- Custom refs and base:
  - `PRS="123 456" BASE_REF="origin/main" make pr.diff`
  - or directly: `PRS="feature-x feature-y" BASE_REF="origin/main" bash scripts/pr_diff_analyzer.sh`

## Requirements

- `git` required. Network access is optional; the script tolerates `git fetch` failures.
- Optional: GitHub CLI `gh` and `jq` for richer PR metadata and PR diffs. Without `gh`, you can pass local branch names instead of PR numbers.

## Output

- Markdown report at `reports/DIFF_REPORT.md` and the same content printed to stdout.
- Temporary branches are created under `tmp/` and deleted afterwards.

## Notes

- The analyzer is idempotent and attempts to restore your previous branch when finished.
- When `gh` is not available or network is restricted, use local branch names in `PRS`.

