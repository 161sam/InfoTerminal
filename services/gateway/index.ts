import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import morgan from 'morgan';
import crypto from 'crypto';
import { enableMetrics } from './obs/metricsBoot';
import { setupOtel } from './obs/otelBoot';

const PORT = Number(process.env.PORT) || 8080;
const USE_LOCAL_UPSTREAMS = process.env.USE_LOCAL_UPSTREAMS === '1';
const TARGET_SEARCH =
  process.env.TARGET_SEARCH ||
  (USE_LOCAL_UPSTREAMS ? 'http://127.0.0.1:8611' : 'http://search-api:8080');
const TARGET_GRAPH =
  process.env.TARGET_GRAPH ||
  (USE_LOCAL_UPSTREAMS ? 'http://127.0.0.1:8612' : 'http://graph-api:8080');
const TARGET_VIEWS =
  process.env.TARGET_VIEWS ||
  (USE_LOCAL_UPSTREAMS ? 'http://127.0.0.1:8613' : 'http://graph-views:8000');

const origins = (process.env.CORS_ORIGINS || 'http://localhost:3411,http://127.0.0.1:3411').split(',');

const pkg = require('./package.json');
const startTs = Date.now();

const app = express();
app.use(helmet());
app.use(cors({ origin: origins, credentials: true }));
app.use(express.json({ limit: '1mb' }));
app.use(morgan('combined'));

setupOtel(process.env.OTEL_SERVICE_NAME || 'gateway');
enableMetrics(app, process.env.IT_METRICS_PATH || '/metrics');

app.use((req, res, next) => {
  const rid = (req.headers['x-request-id'] as string) || crypto.randomUUID();
  (req as any).id = rid;
  res.setHeader('x-request-id', rid);
  next();
});

app.get('/healthz', (_req, res) => {
  res.json({
    service: 'gateway',
    version: pkg.version || '0',
    status: 'ok',
    time: new Date().toISOString(),
    uptime_s: (Date.now() - startTs) / 1000,
  });
});

app.get('/readyz', (_req, res) => res.json({ status: 'ok' }));

app.use('/api', rateLimit({ windowMs: 60_000, max: 600 }));

const baseProxy = (target: string, prefix: RegExp) =>
  createProxyMiddleware({
    target,
    changeOrigin: true,
    pathRewrite: (p) => p.replace(prefix, ''),
    onProxyReq: (proxyReq, req) => {
      proxyReq.setHeader('x-request-id', (req as any).id || '');
    },
    onError: (_err, _req, res) => {
      res.status(502).json({ error: 'bad_gateway' });
    },
    proxyTimeout: 30000,
    timeout: 30000,
  });

app.use('/api/search', baseProxy(TARGET_SEARCH, /^\/api\/search/));
app.use('/api/graph', baseProxy(TARGET_GRAPH, /^\/api\/graph/));
app.use('/api/views', baseProxy(TARGET_VIEWS, /^\/api\/views/));

app.use((_, res) => res.status(404).json({ error: 'not_found' }));

app.listen(PORT, () =>
  console.log(`[gateway] listening on ${PORT} (local_upstreams=${USE_LOCAL_UPSTREAMS})`)
);
