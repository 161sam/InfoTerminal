# ADR-0002: Tenancy and Audit Hooks

## Status
Accepted

## Context
Multi-tenant deployments require tenant separation and traceability of actions.

## Decision
Gateway extracts the tenant from a configurable OIDC claim and forwards it via `X-Tenant-Id` header. Plugin invocations emit audit events to a configurable sink.

## Consequences
Services can access `request.state.tenant_id` while audit logs provide an immutable trail.
