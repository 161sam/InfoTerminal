# v0.2 Smoke Tests

```bash
# Gateway Auth (dev-fallback)
curl -i http://localhost:8610/healthz

# Ontology
curl -s http://localhost:8403/ontology/entities | jq .
curl -s -X POST http://localhost:8403/ontology/validate \
  -H 'Content-Type: application/json' \
  -d '{"type":"Person","data":{"id":"p1","name":"Alice"}}' | jq .

# Graph algos
curl -s -X POST http://localhost:8612/alg/degree -H 'Content-Type: application/json' -d '{}' | jq .
curl -s -X POST http://localhost:8612/shortest -H 'Content-Type: application/json' -d '{"sourceId":1,"targetId":2}' | jq .

# NLP
curl -s -X POST http://localhost:8613/ner -H 'Content-Type: application/json' \
  -d '{"text":"Max Mustermann lebt in Berlin.","lang":"de"}' | jq .

# Dossier
curl -s -X POST http://localhost:8403/dossier -H 'Content-Type: application/json' \
  -d '{"query":"bank transfer","entities":["Person:p1"],"graphSelection":{"nodes":["p1","p2"],"edges":[]}}' | jq .
```
