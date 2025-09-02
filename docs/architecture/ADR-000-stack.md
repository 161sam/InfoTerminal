# ADR-000: Baseline Stack
- Auth: Keycloak (OIDC)
- Ingress: Traefik
- Search: OpenSearch (ES API)
- RDBMS: PostgreSQL
- Object Store: MinIO
- Dev Orchestration: Kind + Helmfile
Rationale: OSS-first, lokal reproduzierbar, geringe Reibung für MVP.
