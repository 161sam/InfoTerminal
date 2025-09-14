# ADR-0001: Plugin System v1

## Status
Accepted

## Context
Plugins are discovered via manifest files that declare capabilities and endpoints.

## Decision
Adopt a manifest-driven plugin system with apiVersion `v1` and optional health endpoint references.

## Consequences
Services can load tools dynamically while keeping a versioned contract for future changes.
