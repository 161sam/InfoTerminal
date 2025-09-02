# Backups

Regelmäßige Backups werden als CronJobs ausgeführt (siehe `infra/k8s/backups`).

- Postgres: täglicher Dump nach S3
- OpenSearch: Snapshot in S3
- Neo4j: `neo4j-admin` Dump in S3

Die Jobs verwenden Credentials aus `infoterminal-app-secrets`.

Weitere Details zur Wiederherstellung im [Runbook](runbooks/restore.md).
