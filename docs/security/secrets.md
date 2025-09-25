# Secrets Hygiene

InfoTerminal enforces a repository-wide secrets hygiene programme to prevent
credential leakage in both the current working tree and the full Git history.
The `scripts/run_secrets_hygiene.py` scanner runs locally and in CI, writes
artefacts under `artifacts/security/secrets/`, and blocks changes that introduce
new secrets.

## Running the scan

```bash
python3 scripts/run_secrets_hygiene.py
```

Key options:

- `--worktree-only` / `--history-only` – narrow the scan scope.
- `--dry-run` – print the classification without writing artefacts.
- `--allowlist <path>` – point to an alternative allowlist file.

The command exits with status:

- `0` (pass) when no new secrets are detected.
- `0` (warn) when only allowlisted historical secrets remain.
- `1` (fail) when new or expired findings exist.

## Artefacts

```
artifacts/security/secrets/
├── findings_history.json   # Historical findings (added lines in Git history)
├── findings_worktree.json  # Findings in the current working tree
├── pr_comment.md           # Markdown summary consumed by CI
└── summary.json            # Aggregate status (pass/warn/fail)
```

The directory also contains a generated `README.md` describing the files.

## Allowlist governance

Accepted findings live in `policy/secrets_allowlist.json`. Each entry must
include a fingerprint, reason, scope, owner, and expiry (ISO 8601). Only add
entries for:

1. **Historical placeholders** that cannot be removed without rewriting history.
2. **Tool false-positives** where no real secret is present.

All other findings require remediation (rotate the secret if it was real, then
purge it from the repository).

Scopes:

- `history` – suppresses findings in Git history only.
- `worktree` – suppresses findings in the current tree (discouraged; only for
  verified false positives).
- `any` – applies everywhere (rarely justified).

Expired entries fail the gate. Review the file quarterly; this baseline was
last refreshed on **2025-10-05**.

## Redaction policy for logs

The logging/redaction guardrails apply to every service:

1. **Never log credential-like headers or bodies** (`Authorization`, `Cookie`,
   `Set-Cookie`, tokens, passwords, API keys). If logging HTTP requests is
   unavoidable, strip or hash these fields first.
2. **Redact structured payloads** before serialising them. Use helper functions
   to replace sensitive values with stable hashes or `***REDACTED***` markers.
   Example (Python):
   ```python
   import hashlib

   def redact_secret(value: str) -> str:
       return hashlib.sha256(value.encode()).hexdigest()[:12] + "***"
   ```
3. **Use structured logging** with explicit keys so redacted fields are
   discoverable (`{"event":"auth.login","user":"analyst","token":"***"}`).
4. **Guard DEBUG logging** behind feature flags; production defaults must be
   INFO or higher. Do not enable verbose traces that include payload dumps.
5. **Anonymise identifiers** when exporting traces/metrics. Replace user IDs
   with pseudonymous IDs where possible, or drop the field entirely.
6. **Document redaction utilities** in service READMEs so contributors know how
   to instrument new code.

## Environment templates & manifests

`.env.example` now ships without dummy secrets. Populate sensitive variables in
personal `.env` files or secrets managers; never commit real credentials. The
Kubernetes manifest `deploy/kubernetes/production.yaml` uses clearly labelled
placeholders (e.g. `PLACEHOLDER_BASE64_POSTGRES_PASSWORD`). Replace them during
deployment automation only.

## CI integration

The GitHub Actions job `secrets-hygiene` runs `python3 scripts/run_secrets_hygiene.py`
on every push and pull request. It fails on new or expired findings, warns on
allowlisted historical exposures, and publishes
`artifacts/security/secrets/pr_comment.md` as a sticky PR comment. Keep the
artefacts committed to ensure reproducible baselines.

For triage workflows, see `STATUS.md` and `DOCS_DIFF.md` — both reference the new
secrets hygiene gate.
