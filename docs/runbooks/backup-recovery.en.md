# Backup and Recovery

These scripts create timestamped backups for Neo4j, OpenSearch and Postgres.

## Backup
```
DRY_RUN=1 scripts/backup_neo4j.sh
DRY_RUN=1 scripts/backup_opensearch.sh
DRY_RUN=1 scripts/backup_postgres.sh
```

## Restore
```
DRY_RUN=1 scripts/restore_neo4j.sh backups/neo4j_<ts>.dump
DRY_RUN=1 scripts/restore_opensearch.sh <snapshot_id>
DRY_RUN=1 scripts/restore_postgres.sh backups/postgres_<ts>.sql
```
