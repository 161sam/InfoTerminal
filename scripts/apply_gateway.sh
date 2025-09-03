#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p services/gateway services/policy

# --- server.js ---
cat > services/gateway/server.js <<'JS'
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { expressjwt: jwt } = require('express-jwt');
const jwksRsa = require('jwks-rsa');
const client = require('prom-client');
const morgan = require('morgan');
const crypto = require('crypto');

// -------- config --------
const PORT = process.env.PORT || 8080;

// Upstreams: Docker-Mode (interne Services) – oder Local-Mode (Host-Ports, no standard ports)
const USE_LOCAL_UPSTREAMS = process.env.USE_LOCAL_UPSTREAMS === '1';
const SEARCH_TARGET  = process.env.SEARCH_TARGET  || (USE_LOCAL_UPSTREAMS ? 'http://127.0.0.1:8611' : 'http://search-api:8080');
const GRAPH_TARGET   = process.env.GRAPH_TARGET   || (USE_LOCAL_UPSTREAMS ? 'http://127.0.0.1:8612' : 'http://graph-api:8080');
const FLOWISE_TARGET = process.env.FLOWISE_TARGET || (USE_LOCAL_UPSTREAMS ? 'http://127.0.0.1:3417' : 'http://flowise-connector:8080');

// Security toggles
const OIDC_ENABLED = process.env.OIDC_ENABLED === '1';
const OIDC_ISSUER  = process.env.OIDC_ISSUER || '';
const OIDC_AUDIENCE= process.env.OIDC_AUDIENCE || 'account';

const OPA_ENABLED  = process.env.OPA_ENABLED === '1';
const OPA_URL      = process.env.OPA_URL || 'http://opa:8181/v1/data/access/allow';
const OPA_AUDIT_URL= process.env.OPA_AUDIT_URL || ''; // optional

// -------- app --------
const app = express();
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGINS || '*', credentials: true }));
app.use(express.json({ limit: '1mb' }));
app.use(morgan('combined'));

// request-id
app.use((req, res, next) => {
  const rid = req.headers['x-request-id'] || crypto.randomUUID();
  req.id = rid; res.setHeader('x-request-id', rid); next();
});

// prometheus metrics
const register = new client.Registry();
client.collectDefaultMetrics({ register });
const httpRequests = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method','route','status'],
  buckets: [0.05,0.1,0.3,0.5,1,2,5,10],
});
register.registerMetric(httpRequests);
app.use((req,res,next)=>{
  const start = process.hrtime.bigint();
  res.on('finish', ()=>{
    const dur = Number(process.hrtime.bigint() - start) / 1e9;
    httpRequests.labels(req.method, req.path.replace(/[0-9a-f-]{8,}/g,':id'), String(res.statusCode)).observe(dur);
  });
  next();
});

app.get('/healthz', (_,res)=>res.json({ok:true}));
app.get('/readyz', (_,res)=>res.json({ready:true}));
app.get('/metrics', async (_,res)=>{
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// -------- OIDC (optional) --------
if (OIDC_ENABLED) {
  const jwtCheck = jwt({
    secret: jwksRsa.expressJwtSecret({
      cache: true, rateLimit: true,
      jwksUri: `${OIDC_ISSUER}/protocol/openid-connect/certs`
    }),
    algorithms: ['RS256'],
    audience: OIDC_AUDIENCE,
    issuer: OIDC_ISSUER
  });
  // schützen alles außer Health/Metrics
  app.use(jwtCheck.unless({ path: ['/healthz','/readyz','/metrics'] }));
}

// -------- OPA middleware (optional) --------
async function opaAllow(req){
  const auth = req.auth || {};
  // Keycloak: roles unter realm_access.roles
  const roles = (auth.realm_access && auth.realm_access.roles) || auth.roles || [];
  const subject = auth.sub || null;
  const email = auth.email || null;

  const input = {
    request: {
      method: req.method.toLowerCase(),
      path: req.path,
      query: req.query,
      headers: { classification: req.headers['x-classification'] || 'public' },
    },
    user: { sub: subject, email, roles }
  };

  const r = await fetch(OPA_URL, {
    method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({ input })
  });
  const j = await r.json().catch(()=> ({}));
  const allow = j && j.result === true;

  // optional audit
  try{
    if (OPA_AUDIT_URL){
      fetch(OPA_AUDIT_URL, {
        method:'POST', headers:{'content-type':'application/json'},
        body: JSON.stringify({ allow, input, ts: Date.now(), rid: req.id })
      }).catch(()=>{});
    }
  }catch(e){/* ignore */}

  return allow;
}

// apply OPA on API routes only
if (OPA_ENABLED) {
  app.use('/api', async (req,res,next) => {
    try{
      const ok = await opaAllow(req);
      if (!ok) return res.status(403).json({ error:'forbidden' });
      next();
    }catch(e){
      console.error('OPA error', e);
      return res.status(500).json({ error:'opa_error' });
    }
  });
}

// -------- Rate limit --------
app.use('/api', rateLimit({ windowMs: 60_000, max: 600 }));

// -------- Proxies --------
const baseProxyOpts = (target, stripPrefixRe) => ({
  target, changeOrigin: true, ws: true,
  pathRewrite: (path) => path.replace(stripPrefixRe, ''),
  onProxyReq: (proxyReq, req) => {
    proxyReq.setHeader('x-request-id', req.id || '');
    if (req.auth?.sub) proxyReq.setHeader('x-user-sub', req.auth.sub);
    if (req.auth?.email) proxyReq.setHeader('x-user-email', req.auth.email);
  },
  onError: (err, req, res) => {
    console.error('proxy error', err?.message);
    res.status(502).json({ error:'bad_gateway' });
  },
  proxyTimeout: 30_000,
  timeout: 30_000,
});

app.use('/api/search',  createProxyMiddleware(baseProxyOpts(SEARCH_TARGET,  /^\/api\/search/)));
app.use('/api/graph',   createProxyMiddleware(baseProxyOpts(GRAPH_TARGET,   /^\/api\/graph/)));
app.use('/api/flowise', createProxyMiddleware(baseProxyOpts(FLOWISE_TARGET, /^\/api\/flowise/)));

app.use((_,res)=>res.status(404).json({error:'not_found'}));

app.listen(PORT, ()=> console.log(`[gateway] listening on ${PORT} (local_upstreams=${USE_LOCAL_UPSTREAMS})`));
JS

# --- package.json ---
cat > services/gateway/package.json <<'JSON'
{
  "name": "infoterminal-gateway",
  "private": true,
  "main": "server.js",
  "engines": { "node": ">=20" },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.19.2",
    "express-jwt": "^8.4.1",
    "express-rate-limit": "^7.3.1",
    "helmet": "^7.1.0",
    "http-proxy-middleware": "^3.0.2",
    "jwks-rsa": "^3.1.0",
    "morgan": "^1.10.0",
    "prom-client": "^15.1.3"
  }
}
JSON

# --- Dockerfile ---
cat > services/gateway/Dockerfile <<'DOCKER'
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm i --omit=dev
COPY server.js ./
ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.js"]
DOCKER

# --- docker-compose override für Gateway (8610:8080) ---
cat > docker-compose.gateway.yml <<'YAML'
version: "3.9"
services:
  gateway:
    build: ./services/gateway
    env_file:
      - .env
    environment:
      - PORT=8080
      # Umschalten der Upstreams (Local-Mode nutzt Host-Ports 8611/8612/3417)
      - USE_LOCAL_UPSTREAMS=${USE_LOCAL_UPSTREAMS:-0}
      - SEARCH_TARGET=${SEARCH_TARGET:-}
      - GRAPH_TARGET=${GRAPH_TARGET:-}
      - FLOWISE_TARGET=${FLOWISE_TARGET:-}
      # Security
      - OIDC_ENABLED=${OIDC_ENABLED:-0}
      - OIDC_ISSUER=${OIDC_ISSUER:-}
      - OIDC_AUDIENCE=${OIDC_AUDIENCE:-account}
      - OPA_ENABLED=${OPA_ENABLED:-1}
      - OPA_URL=${OPA_URL:-http://opa:8181/v1/data/access/allow}
      - OPA_AUDIT_URL=${OPA_AUDIT_URL:-}
      # Observability (Services exportieren selbst; Gateway liefert /metrics)
    ports:
      - "8610:8080"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/healthz"]
      interval: 10s
      timeout: 3s
      retries: 10
YAML

# --- Beispiel OPA policy (best effort) ---
cat > services/policy/access.rego <<'REGO'
package access

default allow = false

# Always allow health/metrics
allow { input.request.path == "/healthz" }
allow { input.request.path == "/readyz" }
allow { input.request.path == "/metrics" }

# Example RBAC:
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

# Search: allow viewer+
allow {
  startswith(input.request.path, "/api/search")
  viewer
}

# Graph: allow analyst+
allow {
  startswith(input.request.path, "/api/graph")
  (analyst or admin)
}

# Flowise: allow analyst+
allow {
  startswith(input.request.path, "/api/flowise")
  (analyst or admin)
}
REGO

echo "✅ Gateway files written (services/gateway, docker-compose.gateway.yml, policy example)."
