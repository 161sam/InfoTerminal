# Testing Strategy

## Test Levels

- **Unit & Integration (Backend):** Pytest with async support and coverage for `search-api` and `graph-api`.
- **Unit (Frontend):** Vitest + Testing Library with JSDOM environment.
- **End-to-End:** Pytest-backed regression matrix in `tests/e2e/` (Search→Graph→Dossier, NLP→Graph→Map, Agent→Toolcall, Feed→Dashboard) plus Playwright smoke navigation for the UI shell.

## Dummy Login

The frontend respects a `TEST_MODE` via a localStorage token. E2E tests use `E2E_DUMMY_TOKEN` to seed a token before navigation.

## Coverage

All unit-test suites target **100 % line and branch coverage** for project code.
Generated files and framework boilerplate are excluded via configuration.

Key rules:

- Treat 100 % coverage as a hard requirement.
  Configure `coverage.py` and Vitest to fail the build if thresholds are not met.
- Omit generated files and third‑party wrappers using the respective `omit` or
  `exclude` settings so coverage focuses on project code.
- Tests must be repeatable and idempotent; rerunning them should not create additional files or require manual cleanup.
- Never rely on live network services. Mock Neo4j, Postgres, HTTP APIs, and timeouts so suites run fully offline.

Coverage reports are written to `coverage.xml` for Python services and to the `coverage/` directory for the frontend.
CI jobs fail if coverage ever drops below 100 % for the measured source paths.

➡ Consolidated at: guides/frontend-modernization.md#running-locally
# Backend services and CLI
pytest --cov --cov-report=term-missing

# Frontend
npm test -- --coverage
```

### Project commands

Run the suites from the repository root, or change into a service directory
if you want to run a single project. All commands enforce a `100%` coverage
threshold and must execute without any network access:

```bash
# Search API
cd services/search-api && pytest --cov --cov-report=term-missing

# Graph API
cd services/graph-api && pytest --cov --cov-report=term-missing

# Graph Views
cd services/graph-views && pytest --cov --cov-report=term-missing

# CLI
cd cli/it_cli && pytest --cov --cov-report=term-missing

# Frontend
cd apps/frontend && npm test -- --coverage
```

All tests must run without network access. External services (HTTP APIs, Neo4j, Postgres, etc.) are mocked or replaced with
in-memory stubs so that the suite is deterministic and fast.

## Continuous Integration

The CI workflow runs separate jobs for backend, frontend, the E2E regression matrix, and ancillary checks.
`pytest tests/e2e -q` powers the dedicated `e2e` job, and artifacts are uploaded alongside the Playwright smoke results.
It also includes security scans and a performance smoke benchmark.
Artifacts such as coverage reports and Playwright reports are uploaded for inspection.
