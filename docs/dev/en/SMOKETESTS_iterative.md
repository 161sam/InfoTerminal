```bash
# NLP
curl -s -X POST http://localhost:8613/ner -H 'Content-Type: application/json' \
  -d '{"text":"Alice works at ACME in Berlin.","lang":"en"}' | jq .

# Agent playbook
curl -s -X POST http://localhost:8610/playbooks/run -H 'Content-Type: application/json' \
  -d '{"name":"InvestigatePerson","params":{"q":"Alice"}}' | jq .

# Graph algos
curl -s -X POST http://localhost:8612/alg/degree -H 'Content-Type: application/json' -d '{}' | jq .
curl -s -X POST http://localhost:8612/alg/betweenness -H 'Content-Type: application/json' -d '{}' | jq .
curl -s -X POST http://localhost:8612/alg/communities -H 'Content-Type: application/json' -d '{}' | jq .

# Dossier
curl -s -X POST http://localhost:8403/dossier -H 'Content-Type: application/json' \
  -d '{"query":"payments","entities":["Person:Alice"],"graphSelection":{"nodes":["p1","p2"],"edges":["e1"]},"format":"md"}' | jq .
```
