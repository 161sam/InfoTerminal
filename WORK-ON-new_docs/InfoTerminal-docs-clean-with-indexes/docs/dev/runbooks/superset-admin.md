# Superset Administration

## Users and Roles

```bash
kubectl exec -it svc/superset -n default -- superset fab list-users
kubectl exec -it svc/superset -n default -- superset fab create-user --username admin --password admin --firstname Admin --lastname User --email admin@example.com
```

## Database Connections

```bash
kubectl exec -it svc/superset -n default -- superset set-database-uri mydb postgresql://user:pass@db:5432/db
```

## Dashboards

```bash
kubectl exec -it svc/superset -n default -- superset export-dashboards --dashboard-ids 1
kubectl exec -it svc/superset -n default -- superset import-dashboards -p dashboards.zip
```

## Cache Warmup

```bash
kubectl exec -it svc/superset -n default -- superset warmup -d 1
```
