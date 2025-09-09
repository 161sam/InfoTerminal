---
merged_from:
  - docs/runbooks/RUNBOOK-obs-opa-secrets.md#L1-L28
merged_at: 2025-09-09T13:14:27.281066Z
---
# Observability, OPA Audit and Secrets

## Quick-Run

```bash
# 1) Grafana Dashboard
kubectl apply -f infra/k8s/observability/grafana-dashboard-cm.yaml

# 2) OPA Audit → ClickHouse
# create CH table once:
# clickhouse-client -q "$(cat infra/clickhouse/opa_audit.sql)"
kubectl apply -f infra/k8s/opa/audit-sink.yaml
kubectl -n policy rollout restart deploy/opa

# 3) Secrets Baseline
helm upgrade --install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace
kubectl apply -f infra/k8s/secrets/clustersecretstore-vault-token.yaml  # or vault-k8s.yaml
kubectl apply -f infra/k8s/edge-auth/oauth2-proxy-external-secret.yaml
kubectl apply -f infra/k8s/analytics/superset-admin-external-secret.yaml
# (optional) Sealed Secrets
helm upgrade --install sealed-secrets sealed-secrets/sealed-secrets -n kube-system
```

## Verification

- Grafana Dashboard sichtbar, Metriken vorhanden.
- ClickHouse `SELECT * FROM logs.opa_decisions ORDER BY ts DESC LIMIT 5;` zeigt Einträge.
- `ExternalSecret` Ressourcen zeigen Status **Synced** und Secrets werden erstellt.
