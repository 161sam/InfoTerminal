# Tests

Run the full test suite from the repository root:

```bash
pytest -q
```

Run tests for an individual service:

```bash
pytest -q services/search-api
pytest -q services/graph-api
pytest -q services/graph-views
```

These commands are used both locally and in CI.
