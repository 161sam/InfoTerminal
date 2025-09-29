# Contributing

## Branching

- Use feature branches off `main`.

## Commit Style

- Follow [Conventional Commits](https://www.conventionalcommits.org/).
- Use `chore(format): …` for formatting-only changes (Prettier/Black/Ruff).

## Development

```bash
make dev-up
make apps-up
npm run lint
npm run lint:docs
gitleaks protect --staged --redact --config .gitleaks.toml
```

Run tests and linters before pushing. `npm run lint` executes Prettier/ESLint for JS/TS and Ruff/Black for Python on files changed against the base branch (set `BASE_SHA` if needed locally).

### Lint & Format Policy

- `npm run lint` is the canonical pre-flight check and is mirrored by the CI `lint` gate.
- `python scripts/lint_python.py [<base>]` and `python scripts/lint_js.py [<base>]` can be used to lint only one stack.
- Use `npx prettier --write` and `python -m black <paths>` to apply formatting fixes locally before committing.

## Phase Flows & Idempotency

- Follow the v1.0 phase cadence: **Phase 1 (Inventory)** → **Phase 2 (Packages A–L)** → **Phase 3 (Hardening)** → **Phase 4 (Release)**. Reference `STATUS.md`, `ROADMAP_STATUS.md`, and `backlog/README.md` when planning work.
- All automation (scripts, CLI, compose overlays) must be **idempotent**. Regenerate inventories via `python scripts/generate_inventory.py` and ensure repeated runs do not duplicate artefacts.
- Update documentation alongside code: consult `DOCS_DIFF.md` for required corrections before merging.
- Observe conventional commits and keep changes scoped to a single artefact/epic when possible.

## No Binary Files

Pull requests must not contain binary assets. A dedicated CI job rejects commits with detected binaries.

## Local Quickstart

```bash
pipx install ./cli
it start -d
it status
```

## ADRs

- Document architectural decisions in `docs/adr` using the provided template.

## Pull Requests

- Update docs and run `npm run lint:docs`.
- Ensure no secrets are committed (`gitleaks protect --staged`).
- Ensure CI is green before requesting review.
