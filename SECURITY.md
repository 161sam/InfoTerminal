# Security

- Never commit real secrets. Use `.env` files for local development and keep them out of version control.
- Scan changes with [`gitleaks`](https://github.com/gitleaks/gitleaks) using the provided `.gitleaks.toml` config:

```bash
gitleaks protect --staged --redact --config .gitleaks.toml
```

- Optional: install the pre-commit hook to run gitleaks automatically before each commit.
