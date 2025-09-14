# ADR-0003: Scalability Principles

## Status
Accepted

## Context
Services should remain stateless and offload long running work.

## Decision
Introduce a lightweight task submission hook with pluggable backends.

## Consequences
Current implementation is a no-op, enabling future workers or queues without breaking APIs.
