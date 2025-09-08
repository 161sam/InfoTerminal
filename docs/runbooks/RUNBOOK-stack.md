# Health-Checks

- Search: curl [localhost:9200](http://localhost:9200)
- Keycloak: [localhost:8081](http://localhost:8081) (admin/adminadmin)
- API: [127.0.0.1:8001](http://127.0.0.1:8001/healthz)

## Common Issues

- Ports belegt → `lsof -i :PORT`
- OpenSearch grün → `GET /_cluster/health?wait_for_status=yellow`
