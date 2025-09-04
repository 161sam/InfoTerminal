# Testing and Coverage

This repository targets **100% line and branch coverage** for all project code. Generated files and third-party boilerplate are excluded via coverage configuration.

## Running tests locally

### Python services and CLI

```bash
pytest --cov --cov-report=term-missing
```

### Frontend

```bash
npm test -- --coverage
```

## Continuous integration

CI executes separate jobs for Python and frontend. Each job fails if coverage drops below 100%. Coverage reports are stored as `coverage.xml` for Python and `coverage/lcov.info` for the frontend.

## Offline requirement

Unit tests must run without network or container dependencies. Mock all external systems such as Neo4j, Postgres, and HTTP APIs.

