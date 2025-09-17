#!/usr/bin/env bash
set -euo pipefail

# Import/Update Keycloak realm via kcadm (inside ephemeral container)
# - Idempotent: creates realm if missing, otherwise updates
# - DRY_RUN=1 to print commands only
#
# Env:
#   KC_URL           (default: http://localhost:8643)
#   KC_REALM_FILE    (default: infra/keycloak/realm-infoterminal.json)
#   KC_REALM         (default: infoterminal)
#   KC_ADMIN         (default: admin)
#   KC_PASS          (default: adminadmin)
#   IMAGE            (default: quay.io/keycloak/keycloak:24.0.1)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

KC_URL=${KC_URL:-http://localhost:8643}
KC_REALM_FILE=${KC_REALM_FILE:-infra/keycloak/realm-infoterminal.json}
KC_REALM=${KC_REALM:-infoterminal}
KC_ADMIN=${KC_ADMIN:-admin}
KC_PASS=${KC_PASS:-adminadmin}
IMAGE=${IMAGE:-quay.io/keycloak/keycloak:24.0.1}

if [ ! -f "$KC_REALM_FILE" ]; then
  echo "❌ Realm file not found: $KC_REALM_FILE" >&2
  exit 1
fi

run() {
  echo "> $*"
  [ "${DRY_RUN:-0}" = "1" ] || eval "$@"
}

# Wait for Keycloak to be reachable
echo "⏳ Waiting for Keycloak at $KC_URL ..."
for i in {1..60}; do
  if curl -fsS "$KC_URL/realms/master/.well-known/openid-configuration" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

# Shared volume for realm file
TMP_VOL="it-kc-realm-$(date +%s)"
run docker volume create "$TMP_VOL" >/dev/null
run docker run --rm -v "$TMP_VOL:/data" -v "$PWD:/ws:ro" alpine sh -lc "cp /ws/$KC_REALM_FILE /data/realm.json"

KC="/opt/keycloak/bin/kcadm.sh"
BASE="${KC_URL%/}"

CMD_LOGIN=(docker run --rm --network host -v "$TMP_VOL:/data:ro" "$IMAGE" \
  bash -lc "$KC config credentials --server '$BASE' --realm master --user '$KC_ADMIN' --password '$KC_PASS' && $KC get realms/$KC_REALM >/dev/null 2>&1 || exit 42")

if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "> docker run --network host $IMAGE ... (login + probe realm)"
else
  if ! "${CMD_LOGIN[@]}"; then
    STATUS=$?
    if [ "$STATUS" != "42" ]; then
      echo "❌ Failed to authenticate with Keycloak (status $STATUS)." >&2
      exit 1
    fi
  fi
fi

# Create if missing
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "> [idempotent] create realm if missing"
else
  docker run --rm --network host -v "$TMP_VOL:/data:ro" "$IMAGE" bash -lc "\
    $KC config credentials --server '$BASE' --realm master --user '$KC_ADMIN' --password '$KC_PASS' && \
    ( $KC get realms/$KC_REALM >/dev/null 2>&1 || $KC create realms -f /data/realm.json )"
fi

# Update realm from file (merge/replace semantics per Keycloak)
run docker run --rm --network host -v "$TMP_VOL:/data:ro" "$IMAGE" bash -lc "\
  $KC config credentials --server '$BASE' --realm master --user '$KC_ADMIN' --password '$KC_PASS' && \
  $KC update realms/$KC_REALM -f /data/realm.json"

run docker volume rm "$TMP_VOL" >/dev/null
echo "✅ Realm '$KC_REALM' upserted at $KC_URL"

