# Auth Gateway Troubleshooting

## Symptoms

- 401 or 403 responses
- Redirect loops

### Checks

```bash
kubectl logs deployment/gateway -n default
kubectl logs deployment/keycloak -n default
conftest test policy/
```

### Fix

- Verify Keycloak realms and clients.
- Ensure oauth2-proxy is configured.
- Review OPA decisions and update policies if needed.
