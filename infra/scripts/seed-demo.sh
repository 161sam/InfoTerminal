#!/usr/bin/env bash
set -euo pipefail

echo "→ Warte auf OpenSearch..."
until curl -s http://localhost:9200 >/dev/null; do sleep 2; done

echo "→ Demo-Index anlegen (docs)"
curl -s -X PUT "http://localhost:9200/docs" -H 'Content-Type: application/json' -d '{
  "mappings": { "properties": { "title":{"type":"text"}, "body":{"type":"text"}, "entities":{"type": "nested","properties":{"name":{"type":"keyword"},"type":{"type":"keyword"}}}}}
}' >/dev/null

echo "→ Beispiel-Dokumente"
curl -s -X POST "http://localhost:9200/docs/_doc" -H 'Content-Type: application/json' -d '{"title":"Hello InfoTerminal","body":"First seeded document for search.","entities":[{"name":"InfoTerminal","type":"Project"}]}' >/dev/null

echo "→ Keycloak Realm import (lightweight)"
KC=http://localhost:8081
until curl -s $KC >/dev/null; do sleep 2; done
echo "   (Hinweis) Realm/Clients kannst du später via UI anlegen: admin/adminadmin"
echo "→ fertig."
