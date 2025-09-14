# Ontologie v1

Die Graph-Ontologie wird als YAML unter `services/graph-views/ontology/*.yaml` gepflegt.

## Endpunkte

- `GET /ontology/entities` – Liste der Entitäten
- `GET /ontology/relations` – Liste der Relationen
- `POST /ontology/validate` – Validierung einer Entität

## Beispiel

```bash
curl -s $VIEWS/ontology/entities | jq '.[] | .name'
```
