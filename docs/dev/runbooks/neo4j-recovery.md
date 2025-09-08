# Neo4j Recovery

## Backup

```bash
kubectl exec -it svc/neo4j -n default -- neo4j-admin database dump neo4j --to-path=/backups
```

## Restore

```bash
kubectl cp backup.dump default/neo4j-0:/var/lib/neo4j/import/
kubectl exec -it neo4j-0 -n default -- neo4j-admin database load neo4j --from-path=/var/lib/neo4j/import/ --force
```

## Reindex

```bash
kubectl exec -it svc/neo4j -n default -- cypher-shell "CALL db.index.fulltext.createNodeIndex('idx', ['Label'], ['prop'])"
```

## Notes

- Ensure leader election completed before writes.
