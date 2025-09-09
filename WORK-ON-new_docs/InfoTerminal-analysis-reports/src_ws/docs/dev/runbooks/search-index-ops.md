# Search Index Operations

## Reindex

```bash
kubectl exec -it svc/opensearch -n default -- curl -XPOST localhost:9200/_reindex -d @reindex.json
```

## Mappings

```bash
kubectl exec -it svc/opensearch -n default -- curl localhost:9200/index/_mapping
```

## Rollover

```bash
kubectl exec -it svc/opensearch -n default -- curl -XPOST localhost:9200/index/_rollover
```

## Snapshot

```bash
kubectl exec -it svc/opensearch -n default -- curl -XPUT localhost:9200/_snapshot/backup
```
