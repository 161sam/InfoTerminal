# Storage

Die Datenbanken verwenden konfigurierbare Replikation.

- **Postgres**: Werte in `infra/k8s/overlays/storage/postgres-values.yaml`
- **OpenSearch**: Werte in `infra/k8s/overlays/storage/opensearch-values.yaml`
- **Neo4j**: Werte in `infra/k8s/overlays/storage/neo4j-values.yaml`

Größe und Replikationsfaktoren können über diese Files angepasst werden.
