# Backup & Restore Runbook

This runbook describes the backup and disaster recovery workflow for the
InfoTerminal data stores (OpenSearch, Neo4j, Postgres). The automation is
implemented as idempotent scripts located in `scripts/` and validated by a
synthetic test harness.

## Recovery Objectives

| Objective | Target | Notes |
| --- | --- | --- |
| **RPO (Recovery Point Objective)** | ≤ 24h | Daily backups via `scripts/backup.sh` are sufficient to cover current data freshness requirements. Additional ad-hoc runs can be triggered before major changes. |
| **RTO (Recovery Time Objective)** | ≤ 30 min | Combined restore (`scripts/restore.sh`) completes within ~15–20 minutes on a developer workstation, leaving headroom for verification and service restarts. |

## Prerequisites

* Docker Compose services are healthy (`docker compose ps`).
* Required credentials and ports:
  * Neo4j admin password exposed via `NEO4J_PASSWORD` (defaults to `test12345`).
  * OpenSearch security disabled in dev images (no credentials necessary).
  * Postgres superuser accessible as `postgres` (password from compose env).
* Host has sufficient disk space under `artifacts/backup/` to store compressed
tarballs and SQL dumps.

## Backup Procedure

1. Ensure services are running and healthy.
2. Execute the orchestration script:
   ```bash
   IT_COMPOSE_FILES=docker-compose.yml \
   scripts/backup.sh --out artifacts/backup/$(date +%Y%m%d_%H%M%S)
   ```
   * `--services` allows selecting a subset (`opensearch,neo4j,postgres`).
   * `--timestamp` enforces deterministic filenames when bundling backups with
a deployment package.
3. Inspect the generated `backup-manifest.json` to confirm artefacts:
   ```json
   {
     "timestamp": "20250201_101500",
     "services": {
       "neo4j": "neo4j_20250201_101500.dump",
       "opensearch": "opensearch_20250201_101500.tar.gz",
       "postgres": "postgres_20250201_101500.sql"
     }
   }
   ```
4. Upload or archive the directory under `artifacts/backup/<timestamp>` to the
selected remote storage (S3/minio/artifactory). Include the manifest for traceability.

## Restore Procedure

1. Stop user-facing workloads or place the platform in maintenance mode.
2. Retrieve and extract the desired backup directory under `artifacts/backup/`.
3. Run the restore orchestration:
   ```bash
   scripts/restore.sh --path artifacts/backup/20250201_101500
   ```
   * Override compose targets via `IT_COMPOSE_FILES` / `IT_COMPOSE_PROJECT` if the
stack runs under a non-default profile.
   * To restore only a subset, supply `--services neo4j,postgres` etc.
4. Monitor script output – each helper script restarts the corresponding
service after applying the data.
5. Perform smoke checks:
   * Postgres: `psql -U postgres -c "\dt"`
   * Neo4j: `cypher-shell "MATCH (n) RETURN count(n) LIMIT 5"`
   * OpenSearch: `curl http://localhost:9200/_cluster/health`

## Synthetic Validation Flow

`tests/backup_restore_synthetic.sh` automates a minimal recovery rehearsal:

```bash
# Populate → Backup → Wipe → Restore → Verify
./tests/backup_restore_synthetic.sh
```

The script inserts sample rows/nodes/documents, invokes the orchestration,
and writes `synthetic-validation.json` with the final counts, enabling quick
regression checks in CI or during on-call drills.

## Troubleshooting

* **Docker permission errors** – ensure the user belongs to the `docker` group
or run scripts via `sudo`.
* **Neo4j restore fails** – confirm the main container is stopped; the helper
script stops the service but external orchestrators may restart it. Retry after
running `docker compose stop neo4j`.
* **OpenSearch snapshot fails** – verify disk space and that the `opensearch`
container can create files under `/usr/share/opensearch/data`.
* **Postgres restore errors about existing objects** – the dump is created with
`--clean --if-exists`. If manual changes were applied between backup and
restore, drop the conflicting objects or run `scripts/backup.sh` again to capture the
latest schema.

## References

* `scripts/backup.sh`, `scripts/restore.sh`
* `scripts/backup_<service>.sh`, `scripts/restore_<service>.sh`
* `tests/backup_restore_synthetic.sh`
* Artefacts stored under `artifacts/backup/`
