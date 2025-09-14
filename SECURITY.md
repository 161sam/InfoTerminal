# Security

- Never commit real secrets. Use `.env` files for local development and keep them out of version control.
- Scan changes with [`gitleaks`](https://github.com/gitleaks/gitleaks) using the provided `.gitleaks.toml` config:

```bash
gitleaks protect --staged --redact --config .gitleaks.toml
```

- Optional: install the pre-commit hook to run gitleaks automatically before each commit.
- Gateway enforces OIDC JWTs (`iss`, `aud`, JWKS cache, clock skew via `IT_OIDC_SKEW`) and calls OPA for sensitive paths.
- Security relevant actions emit structured entries via `audit_log`.
- Backup and recovery scripts live under `scripts/` with `DRY_RUN` support; see runbook in `docs/runbooks/`.
