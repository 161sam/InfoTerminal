# Secrets Hygiene Artefacts

- `summary.json`: Gate status (pass/warn/fail) and aggregate counts.
- `findings_worktree.json`: Detailed findings for the current working tree.
- `findings_history.json`: Findings discovered in Git history (added lines).
- `pr_comment.md`: Markdown summary used by CI for PR comments.

Accepted findings are tracked in `policy/secrets_allowlist.json`. Update that file to document false positives or accepted historical exposures.
