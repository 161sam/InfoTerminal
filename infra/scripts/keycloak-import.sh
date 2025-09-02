#!/usr/bin/env bash
set -euo pipefail
KC_URL=${KC_URL:-http://localhost:8081}
ADMIN_USER=${ADMIN_USER:-admin}
ADMIN_PASS=${ADMIN_PASS:-adminadmin}

echo "→ Keycloak Token holen…"
TOKEN=$(curl -s -X POST "$KC_URL/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=admin-cli" \
  -d "username=$ADMIN_USER" \
  -d "password=$ADMIN_PASS" \
  -d "grant_type=password" | jq -r .access_token)

echo "→ Realm importieren…"
curl -s -X POST "$KC_URL/admin/realms" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @infra/keycloak/realm-infoterminal.json >/dev/null || true

echo "→ Done. Realm 'infoterminal'."
