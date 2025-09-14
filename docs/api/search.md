# Search API

`POST /query` executes a document search.

## Request

```json
{
  "q": "acme",
  "filters": { "source": ["osint"], "entity_type": ["Person"] },
  "facets": ["source", "entity_types"],
  "sort": { "field": "meta.created_at", "order": "desc" },
  "knn": { "field": "embedding", "vector": [0.1, 0.2], "k": 10 },
  "limit": 20,
  "offset": 0
}
```

`knn` is only processed when the service runs with `KNN_ENABLED=1`.

## Response

```json
{
  "items": [ { "id": "1", "title": "Doc" } ],
  "total": 1,
  "aggregations": { "source": [ { "key": "osint", "doc_count": 1 } ] },
  "tookMs": 5
}
```
