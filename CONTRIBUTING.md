# Contributing

## Branching

- Use feature branches off `main`.

## Commit Style

- Follow [Conventional Commits](https://www.conventionalcommits.org/).

## Development

```bash
make dev-up
make apps-up
npm run lint:docs
gitleaks protect --staged --redact --config .gitleaks.toml
```

Run tests and linters before pushing.

## ADRs

- Document architectural decisions in `docs/adr` using the provided template.

## Pull Requests

- Update docs and run `npm run lint:docs`.
- Ensure no secrets are committed (`gitleaks protect --staged`).
- Ensure CI is green before requesting review.
