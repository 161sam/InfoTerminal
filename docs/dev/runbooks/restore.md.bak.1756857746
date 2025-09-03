# Restore Runbook

Schritte zur Wiederherstellung:

## Postgres
1. Backup herunterladen: `aws --endpoint-url $S3_ENDPOINT s3 cp s3://$S3_BUCKET/postgres/pgdump-<datum>.sql pgdump.sql`
2. `psql -h postgres.default.svc -U app -f pgdump.sql`

## OpenSearch
1. Snapshot registrieren: `curl -u admin:$OPENSEARCH_PASSWORD -XPUT http://opensearch.default.svc:9200/_snapshot/daily`
2. Snapshot laden: `curl -u admin:$OPENSEARCH_PASSWORD -XPOST http://opensearch.default.svc:9200/_snapshot/daily/<snap>/_restore`

## Neo4j
1. Backup laden: `aws --endpoint-url $S3_ENDPOINT s3 cp s3://$S3_BUCKET/neo4j/neo4j-<datum>.dump neo4j.dump`
2. `neo4j-admin database load neo4j --from-path=. --overwrite-destination=true`
