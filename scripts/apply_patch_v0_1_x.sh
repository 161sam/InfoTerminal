#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
echo "→ Applying v0.1.x hardening + obs + agents patch in: $ROOT"

mkdir -p scripts deploy/grafana/provisioning/{dashboards,datasources} infra/observability \
         services/flowise-connector charts/infoterminal/templates

# ---------- 1) docker-compose Observability (Profile: obs) ----------
cat > docker-compose.observability.yml <<'YAML'
version: "3.9"
services:
  otel-collector:
    image: otel/opentelemetry-collector:0.106.1
    command: ["--config=/etc/otel/config.yaml"]
    volumes: [ "./infra/observability/otel-collector.yaml:/etc/otel/config.yaml:ro" ]
    ports: ["4317:4317"]  # OTLP gRPC
    profiles: ["obs"]

  loki:
    image: grafana/loki:2.9.8
    command: ["-config.file=/etc/loki/config.yaml"]
    volumes: [ "./infra/observability/loki/values.yaml:/etc/loki/config.yaml:ro" ]
    ports: ["3100:3100"]
    profiles: ["obs"]

  promtail:
    image: grafana/promtail:2.9.8
    volumes:
      - /var/log:/var/log:ro
      - ./infra/observability/promtail/values.yaml:/etc/promtail/config.yaml:ro
    command: ["--config.file=/etc/promtail/config.yaml"]
    profiles: ["obs"]
    depends_on: { loki: { condition: service_started } }

  tempo:
    image: grafana/tempo:2.5.0
    volumes: [ "./infra/observability/tempo/values.yaml:/etc/tempo/config.yaml:ro" ]
    command: ["-config.file=/etc/tempo/config.yaml"]
    ports: ["3200:3200"]
    profiles: ["obs"]

  prometheus:
    image: prom/prometheus:v2.53.0
    volumes: [ "./infra/observability/prometheus/values.yaml:/etc/prometheus/prometheus.yml:ro" ]
    ports: ["9090:9090"]
    profiles: ["obs"]

  grafana:
    image: grafana/grafana:10.4.5
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
    volumes:
      - ./deploy/grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro
      - ./deploy/grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./deploy/grafana/dashboards:/var/lib/grafana/dashboards:ro
    ports: ["3001:3000"]
    profiles: ["obs"]
    depends_on:
      prometheus: { condition: service_started }
      loki:       { condition: service_started }
      tempo:      { condition: service_started }
YAML

# Provisioning (falls nicht vorhanden)
cat > deploy/grafana/provisioning/datasources/datasources.yml <<'YAML'
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
YAML

cat > deploy/grafana/provisioning/dashboards/dashboards.yml <<'YAML'
apiVersion: 1
providers:
  - name: 'infoterminal'
    orgId: 1
    type: file
    disableDeletion: true
    options:
      path: /var/lib/grafana/dashboards
YAML

# ---------- 2) Compose: service env wiring for OTEL + Rerank ----------
# helper to upsert env to a service block
python3 - <<'PY'
import re, sys, pathlib
p = pathlib.Path('docker-compose.yml')
s = p.read_text(encoding='utf-8')

def inject_env(service, env_lines):
    pat = re.compile(rf'^(\s*{re.escape(service)}:\n(?:.+\n)*?)\s*(environment:\n(?:.+\n)*?)?(?=\s*[a-zA-Z0-9_-]+:|\Z)', re.M)
    m = pat.search(s)
    if not m:
        return None
    head = m.group(1)
    env_block = m.group(2) or "    environment:\n"
    # ensure environment: exists
    if "environment:" not in env_block:
        env_block = "    environment:\n"
    # append lines if missing
    for line in env_lines:
        if line.strip() not in env_block:
            env_block += f"      - {line}\n"
    return s[:m.start()] + head + env_block + s[m.end():]

env_common = [
    "OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317",
    "OTEL_TRACES_EXPORTER=otlp",
    "OTEL_METRICS_EXPORTER=none",
    "OTEL_LOGS_EXPORTER=none",
    "OTEL_RESOURCE_ATTRIBUTES=service.name=${COMPOSE_SERVICE_NAME:-unknown}",
    "RERANK_ENABLED=${RERANK_ENABLED:-1}"
]

services = ["search-api","graph-api","graph-views","doc-entities","entity-resolution","gateway","opa-audit-sink","openbb-connector"]
txt = s
for svc in services:
    new_txt = inject_env(svc, env_common)
    if new_txt:
        txt = new_txt
s = txt
p.write_text(s, encoding='utf-8')
print("compose env wiring done")
PY

# ---------- 3) Gateway Härtung: OIDC + OPA ----------
# server.js ersetzen/erweitern (idempotent)
cat > services/gateway/server.js <<'JS'
const express = require('express');
const rateLimit = require('express-rate-limit');
const cors = require('cors');
const jwt = require('express-jwt');
const jwks = require('jwks-rsa');
const fetch = require('node-fetch');
const client = require('prom-client');

const app = express();
app.use(cors({ origin: process.env.CORS_ORIGINS || '*', credentials: true }));
app.use(express.json({ limit: '1mb' }));

// Metrics
const register = new client.Registry();
client.collectDefaultMetrics({ register });
app.get('/metrics', async (_, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// Basic rate limit
app.use(rateLimit({ windowMs: 60_000, max: 600 }));

// OIDC (Keycloak) – optional per env toggle
if (process.env.OIDC_ENABLED === '1') {
  const issuer = process.env.OIDC_ISSUER; // z.B. https://keycloak/auth/realms/infoterminal
  const audience = process.env.OIDC_AUDIENCE || 'account';
  app.use(jwt({
    secret: jwks.expressJwtSecret({
      cache: true, rateLimit: true,
      jwksUri: `${issuer}/protocol/openid-connect/certs`
    }),
    algorithms: ['RS256'],
    audience,
    issuer: issuer
  }).unless({ path: ['/healthz','/metrics'] }));
}

// OPA authorize middleware
async function opaAllow(req, user) {
  const input = {
    user: { roles: (user?.realm_access?.roles) || (user?.roles) || [] },
    action: req.method.toLowerCase(),
    resource: { path: req.path, classification: req.headers['x-classification'] || 'public' }
  };
  const opaURL = process.env.OPA_URL || 'http://opa:8181/v1/data/access/allow';
  const r = await fetch(opaURL, { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ input }) });
  const j = await r.json();
  return j?.result === true;
}

app.get('/healthz', (_, res) => res.json({ ok: true }));

app.use(async (req, res, next) => {
  if (process.env.OPA_ENABLED !== '1') return next();
  try {
    const user = req.user || {};
    const allow = await opaAllow(req, user);
    if (!allow) return res.status(403).json({ error: 'forbidden' });
    next();
  } catch (e) {
    console.error('OPA error', e);
    return res.status(500).json({ error: 'opa_error' });
  }
});

// Proxy skeleton (extend as needed)
app.all('/api/*', (req, res) => {
  res.json({ ok: true, msg: 'gateway up (wire upstreams next)' });
});

const port = process.env.PORT || 8080;
app.listen(port, () => console.log(`gateway listening on ${port}`));
JS

# package.json – sichergehen, dass deps da sind
cat > services/gateway/package.json <<'JSON'
{
  "name": "infoterminal-gateway",
  "private": true,
  "type": "module",
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.19.2",
    "express-jwt": "^8.4.1",
    "express-rate-limit": "^7.3.1",
    "jwks-rsa": "^3.1.0",
    "node-fetch": "^3.3.2",
    "prom-client": "^15.1.3"
  }
}
JSON

# ---------- 4) Flowise Connector (FastAPI) ----------
cat > services/flowise-connector/pyproject.toml <<'TOML'
[project]
name = "flowise-connector"
version = "0.1.0"
dependencies = [
  "fastapi>=0.111",
  "uvicorn>=0.30",
  "httpx>=0.27",
  "python-jose[cryptography]>=3.3",
  "prometheus-client==0.20.*",
  "opentelemetry-sdk",
  "opentelemetry-instrumentation-fastapi",
  "opentelemetry-exporter-otlp"
]
TOML

mkdir -p services/flowise-connector/app
cat > services/flowise-connector/app/main.py <<'PY'
import os, time
from typing import Optional, Dict, Any
import httpx
from fastapi import FastAPI, HTTPException, Header, Depends
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:
    FastAPIInstrumentor = None

FLOWISE_URL = os.getenv("FLOWISE_URL", "http://flowise:3000")
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY", "")
TIMEOUT = float(os.getenv("FLOWISE_TIMEOUT_S", "30"))

app = FastAPI(title="Flowise Connector", version="0.1.0")

if FastAPIInstrumentor:
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": int(time.time())}

@app.post("/chat/{agent_id}")
async def chat(agent_id: str, body: Dict[str, Any], authorization: Optional[str] = Header(None)):
    headers = {"Content-Type": "application/json"}
    if FLOWISE_API_KEY:
        headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
    # Optional: forward caller auth (keycloak) if needed
    if authorization:
        headers["X-Caller-Authorization"] = authorization

    url = f"{FLOWISE_URL}/api/v1/prediction/{agent_id}"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(url, json=body, headers=headers)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
PY

cat > services/flowise-connector/dev_run.sh <<'SH'
#!/usr/bin/env bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
SH
chmod +x services/flowise-connector/dev_run.sh

# Compose-Service
python3 - <<'PY'
import yaml, sys, pathlib
f = pathlib.Path('docker-compose.yml')
data = yaml.safe_load(f.read_text())
svc = data.setdefault('services', {})
if 'flowise-connector' not in svc:
    svc['flowise-connector'] = {
        'build': './services/flowise-connector',
        'ports': ['8615:8080'],
        'env_file': '.env',
        'environment': [
            'FLOWISE_URL=${FLOWISE_URL:-http://flowise:3000}',
            'FLOWISE_TIMEOUT_S=30',
            'OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317',
            'OTEL_TRACES_EXPORTER=otlp'
        ],
        'profiles': ['agents'],
        'healthcheck': {
            'test': ['CMD', 'curl', '-fsS', 'http://localhost:8080/healthz'],
            'interval': '10s', 'timeout': '3s', 'retries': 10
        }
    }
f.write_text(yaml.dump(data, sort_keys=False))
print("flowise-connector added to docker-compose")
PY

# ---------- 5) Helm: OTEL + Rerank + Agents env ----------
# values.yaml upsert
python3 - <<'PY'
import re, pathlib
p = pathlib.Path('charts/infoterminal/values.yaml')
s = p.read_text()
def upsert_block(s, key, lines):
    if key in s:
        return s
    return s + "\n" + key + ":\n" + "\n".join([f"  {l}" for l in lines]) + "\n"

s = s.replace("RERANK_ENABLED: \"0\"", "RERANK_ENABLED: \"1\"")
s = upsert_block(s, "otel", [
  "enabled: true",
  "endpoint: http://otel-collector.observability:4317"
])
if "FLOWISE_URL" not in s:
    s += "\nflowise:\n  url: http://flowise:3000\n"
p.write_text(s)
print("helm values updated")
PY

# deployment templates: add env from .Values.env + otel/flowise extras
for DEP in charts/infoterminal/templates/deployment-*.yaml; do
  sed -i '/envFrom:/a \            - name: OTEL_EXPORTER_OTLP_ENDPOINT\n              value: {{ .Values.otel.endpoint }}' "$DEP" || true
  sed -i '/envFrom:/a \            - name: RERANK_ENABLED\n              value: {{ .Values.env.RERANK_ENABLED | quote }}' "$DEP" || true
done

# ---------- 6) .env dev hints ----------
grep -q '^OIDC_ENABLED' .env 2>/dev/null || cat >> .env <<'ENV'
# --- Security / Gateway ---
OIDC_ENABLED=0
OIDC_ISSUER=http://keycloak:8080/realms/infoterminal
OIDC_AUDIENCE=account
OPA_ENABLED=1
OPA_URL=http://opa:8181/v1/data/access/allow

# --- Observability ---
RERANK_ENABLED=1
ENV

echo "✅ Patch applied."

