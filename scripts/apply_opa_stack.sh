#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p services/policy services/opa-audit-sink/app

# 1) Beispiel-Policy (nur wenn nicht vorhanden)
[ -f services/policy/access.rego ] || cat > services/policy/access.rego <<'REGO'
package access

default allow = false

# Health/Metrics immer frei
allow { input.request.path == "/healthz" }
allow { input.request.path == "/readyz" }
allow { input.request.path == "/metrics" }

viewer {
  some r
  r := input.user.roles[_]
  r == "viewer"
}
analyst {
  some r
  r := input.user.roles[_]
  r == "analyst"
}
admin {
  some r
  r := input.user.roles[_]
  r == "admin"
}

# Search: viewer+
allow {
  startswith(input.request.path, "/api/search")
  viewer
}

# Graph: analyst+
allow {
  startswith(input.request.path, "/api/graph")
  (analyst or admin)
}

# Flowise: analyst+
allow {
  startswith(input.request.path, "/api/flowise")
  (analyst or admin)
}
REGO

# 2) OPA Compose-Override (intern 8181, optional Host 8651)
cat > docker-compose.opa.yml <<'YAML'
version: "3.9"
services:
  opa:
    image: openpolicyagent/opa:0.64.1-rootless
    command:
      - "run"
      - "--server"
      - "--addr=0.0.0.0:8181"
      - "--log-level=info"
      - "--set=decision_logs.console=true"
      - "/policies"
    volumes:
      - ./services/policy:/policies:ro
    # standard: kein Host-Port (nur intern erreichbar)
    # optional Host-Expose per: OPA_EXPOSE=1 docker compose -f ... up -d
    ports:
      - ${OPA_EXPOSE:+8651:8181}
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8181/health?plugins&bundle"]
      interval: 10s
      timeout: 3s
      retries: 10
YAML

# 3) Audit-Sink (optional)
cat > services/opa-audit-sink/app/main.py <<'PY'
import os, time
from fastapi import FastAPI, Request
from typing import Any, Dict

app = FastAPI(title="OPA Audit Sink", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": int(time.time())}

@app.post("/audit")
async def audit(req: Request):
    payload: Dict[str, Any] = await req.json()
    # Hier könntest du in eine DB/Queue schreiben; wir loggen zur Konsole
    print("[AUDIT]", payload)
    return {"ok": True}
PY

cat > services/opa-audit-sink/pyproject.toml <<'TOML'
[project]
name = "opa-audit-sink"
version = "0.1.0"
dependencies = [ "fastapi>=0.111", "uvicorn>=0.30" ]
TOML

cat > services/opa-audit-sink/Dockerfile <<'DOCKER'
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir uvicorn fastapi
COPY app /app/app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
DOCKER

# 4) Optionales Agents-Override für Audit-Sink Host-Port (8652)
# (nutzen wir gleich mit dem Gateway; Host-Expose nur wenn gewünscht)
awk '1' docker-compose.agents.yml 2>/dev/null | cat >/dev/null || true
if [ -f docker-compose.agents.yml ]; then
  if ! grep -q 'opa-audit-sink' docker-compose.agents.yml; then
    cat >> docker-compose.agents.yml <<'YAML'

  opa-audit-sink:
    build: ./services/opa-audit-sink
    profiles: ["agents"]
    ports:
      - ${AUDIT_EXPOSE:+8652:8080}
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/healthz"]
      interval: 10s
      timeout: 3s
      retries: 10
YAML
  fi
fi

# 5) Gateway .env Defaults (nur anhängen, falls nicht vorhanden)
grep -q '^OPA_ENABLED' .env 2>/dev/null || cat >> .env <<'ENV'
# --- Gateway x OPA ---
OPA_ENABLED=1
OPA_URL=http://opa:8181/v1/data/access/allow
# Audit optional:
OPA_AUDIT_URL=
ENV

# 6) dev_up.sh: OPA automatisch mitstarten, wenn GW=1 gesetzt ist
if grep -q 'Starting gateway' scripts/dev_up.sh 2>/dev/null; then
  if ! grep -q 'docker-compose.opa.yml' scripts/dev_up.sh; then
    awk '
      /Starting gateway on 8610/ && !x { 
        print; 
        print "  # bring OPA up (internal only unless OPA_EXPOSE=1)"; 
        print "  docker compose -f docker-compose.yml -f docker-compose.opa.yml up -d opa";
        x=1; next
      } { print }
    ' scripts/dev_up.sh > scripts/dev_up.sh.tmp && mv scripts/dev_up.sh.tmp scripts/dev_up.sh
    chmod +x scripts/dev_up.sh
  fi
fi

echo "✅ OPA + (optional) Audit-Sink eingerichtet (docker-compose.opa.yml, services/policy/*, services/opa-audit-sink/*)."
