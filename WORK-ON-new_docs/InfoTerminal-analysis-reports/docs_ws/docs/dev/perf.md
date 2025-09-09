# Performance Smoke Tests

These tests provide quick feedback on API performance during pull requests. They are not full load tests.

## Tools

- `autocannon` for simple HTTP benchmarking
- Optional: `k6` for more advanced scenarios

## Configuration

Endpoints and ports used during CI can be adjusted in the workflow or via environment variables.
