# Smoke Tests: Agent, Graph, Geospatial

```bash
# Agent tools
curl -s http://localhost:8610/tools | jq .

# Playbook
curl -s -X POST http://localhost:8610/playbooks/run -H 'Content-Type: application/json' \
  -d '{"name":"InvestigatePerson","params":{"q":"Alice"}}' | jq .

# Chat (stub if AGENT_BASE_URL unset)
curl -s -X POST http://localhost:8610/chat -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Find links between Alice and ACME."}]}' | jq .

# Graph algorithms
curl -s -X POST http://localhost:8612/alg/degree -H 'Content-Type: application/json' -d '{}' | jq .
curl -s -X POST http://localhost:8612/alg/betweenness -H 'Content-Type: application/json' -d '{}' | jq .
curl -s -X POST http://localhost:8612/alg/communities -H 'Content-Type: application/json' -d '{}' | jq .

# Geo upload
curl -s -X POST http://localhost:8403/geo/upload -F 'file=@examples/sample.geojson' | jq .
curl -s http://localhost:8403/geo/list | jq .
```
