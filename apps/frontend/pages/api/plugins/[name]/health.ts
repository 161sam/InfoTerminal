import type { NextApiRequest, NextApiResponse } from 'next';

function envInt(name: string, def: number): number {
  const v = process.env[name];
  if (!v) return def;
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : def;
}

async function timedFetch(url: string, init?: RequestInit & { timeoutMs?: number }) {
  const { timeoutMs = 2500, ...rest } = init || {};
  const ctrl = new AbortController();
  const id = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...rest, signal: ctrl.signal });
    return res;
  } finally {
    clearTimeout(id);
  }
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { name } = req.query as { name: string };
  try {
    let ok = false;
    let version: string | undefined;
    switch (name) {
      case 'aleph': {
        const port = envInt('IT_PORT_ALEPH', 8641);
        const r = await timedFetch(`http://localhost:${port}/`, { timeoutMs: 2500 });
        ok = r.ok;
        break;
      }
      case 'superset': {
        const port = envInt('IT_PORT_SUPERSET', 8644);
        const r = await timedFetch(`http://localhost:${port}/health`, { timeoutMs: 2500 });
        ok = r.ok;
        break;
      }
      case 'nifi': {
        const port = envInt('IT_PORT_NIFI', 8619);
        const r = await timedFetch(`http://localhost:${port}/nifi-api/system-diagnostics`, { timeoutMs: 2500 });
        ok = r.ok;
        break;
      }
      case 'airflow': {
        const port = envInt('IT_PORT_AIRFLOW', 8642);
        const r = await timedFetch(`http://localhost:${port}/health`, { timeoutMs: 2500 });
        ok = r.ok;
        break;
      }
      default: {
        // Proxy health to plugin-runner for tool plugins if needed in future
        return res.status(404).json({ status: 'unknown' });
      }
    }
    return res.status(200).json({ status: ok ? 'up' : 'down', version });
  } catch {
    return res.status(200).json({ status: 'down' });
  }
}

