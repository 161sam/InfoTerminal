# Security Hardening

Dieses Dokument beschreibt die Sicherheitsmaßnahmen des InfoTerminal:

- **ExternalSecrets** verwalten Passwörter zentral und werden per `envFrom` eingebunden.
- **TLS** wird über `cert-manager` und Let's Encrypt ClusterIssuer ausgerollt.
- **mTLS** kann über das Overlay `infra/k8s/overlays/mtls` aktiviert werden (Istio Beispiel).
- **Ressourcen-Limits** und optionales **HPA** schützen vor Ressourcenkonkurrenz.
- **Replikationsfaktoren** für Postgres, OpenSearch und Neo4j sind konfigurierbar.
- **Backups** laufen als CronJobs und landen in S3/MinIO.
- **OPA/Conftest** verhindert Secrets in Manifests.
