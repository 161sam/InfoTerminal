# Testing Strategy

## Test Levels

- **Unit & Integration (Backend):** Pytest with async support and coverage for `search-api` and `graph-api`.
- **Unit (Frontend):** Vitest + Testing Library with JSDOM environment.
- **End-to-End:** Playwright runs a smoke test that performs a dummy login, executes a search, and opens the graph view.

## Dummy Login

The frontend respects a `TEST_MODE` via a localStorage token. E2E tests use `E2E_DUMMY_TOKEN` to seed a token before navigation.

## Coverage

All unit-test suites target **100 % line and branch coverage** for project code. Generated files and framework boilerplate are excluded via configuration.

Coverage reports are written to `coverage.xml` for Python services and to the `coverage/` directory for the frontend.
CI jobs fail if coverage ever drops below 100 % for the measured source paths.

### Running locally

```bash
# Backend services and CLI
pytest --cov --cov-report=term-missing

# Frontend
npm test -- --coverage
```

All tests must run without network access. External services (HTTP APIs, Neo4j, Postgres, etc.) are mocked or replaced with in-memory stubs so that the suite is deterministic and fast.

## Continuous Integration

The CI workflow runs separate jobs for backend, frontend, and E2E tests.
It also includes security scans and a performance smoke benchmark.
Artifacts such as coverage reports and Playwright reports are uploaded for inspection.
