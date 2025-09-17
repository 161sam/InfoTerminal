#!/usr/bin/env bash
set -euo pipefail

# SSO smoke test for oauth2-proxy in front of Superset and Airflow.
# Idempotent; uses only HTTP checks. No secrets required.
#
# Usage:
#   ./scripts/sso_smoke.sh [--superset] [--airflow]
#
# Exits non-zero if checks fail. Prints short diagnostics.

SUP=${IT_PORT_SUPERSET:-8644}
AIR=${IT_PORT_AIRFLOW:-8642}
ISSUER=${IT_OIDC_ISSUER:-http://localhost:8080/realms/infoterminal}

DO_SUP=1
DO_AIR=1
for a in "$@"; do
  case "$a" in
    --superset) DO_AIR=0 ;;
    --airflow) DO_SUP=0 ;;
  esac
done

http_code() {
  curl -sS -o /dev/null -w "%{http_code}" "$1"
}

location_header() {
  curl -sS -o /dev/null -D - "$1" | awk '/^Location:/ {print $2}' | tr -d '\r' || true
}

echo "SSO Smoke: Issuer: $ISSUER"
curl -fsS "$ISSUER/.well-known/openid-configuration" >/dev/null || {
  echo "❌ OIDC issuer not reachable: $ISSUER"; exit 1;
}
echo "✅ OIDC issuer reachable"

if [[ "$DO_SUP" == "1" ]]; then
  URL="http://localhost:$SUP/"
  echo "\nChecking Superset SSO at $URL"
  code=$(http_code "$URL")
  loc=$(location_header "$URL")
  echo "→ HTTP $code"
  if [[ "$code" != "302" && "$code" != "401" && "$code" != "403" ]]; then
    echo "❌ Expected redirect to Keycloak (302) or auth error (401/403), got $code"; exit 1;
  fi
  if [[ "$code" == "302" ]]; then
    if [[ "$loc" != *"/protocol/openid-connect/auth"* ]]; then
      echo "❌ Redirect location does not look like Keycloak authorize endpoint: $loc"; exit 1;
    fi
    echo "✅ Redirects to Keycloak ($loc)"
  else
    echo "ℹ️ Received $code (may be due to oauth2-proxy settings); continuing"
  fi
fi

if [[ "$DO_AIR" == "1" ]]; then
  URL="http://localhost:$AIR/"
  echo "\nChecking Airflow SSO at $URL"
  code=$(http_code "$URL")
  loc=$(location_header "$URL")
  echo "→ HTTP $code"
  if [[ "$code" != "302" && "$code" != "401" && "$code" != "403" ]]; then
    echo "❌ Expected redirect to Keycloak (302) or auth error (401/403), got $code"; exit 1;
  fi
  if [[ "$code" == "302" ]]; then
    if [[ "$loc" != *"/protocol/openid-connect/auth"* ]]; then
      echo "❌ Redirect location does not look like Keycloak authorize endpoint: $loc"; exit 1;
    fi
    echo "✅ Redirects to Keycloak ($loc)"
  else
    echo "ℹ️ Received $code (may be due to oauth2-proxy settings); continuing"
  fi
fi

echo "\n✅ SSO smoke checks passed"

