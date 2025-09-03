import type { NextApiRequest, NextApiResponse } from 'next';
import { SEARCH_API, GRAPH_API, DOCENTITIES_API, NLP_API } from '../../lib/config';

type ServiceState = 'ok' | 'degraded' | 'down' | 'unreachable';
export type HealthResponse = {
  timestamp: string;
  services: {
    search: { state: ServiceState; latencyMs: number | null; info?: any };
    graph: { state: ServiceState; latencyMs: number | null; info?: any };
    docentities: { state: ServiceState; latencyMs: number | null; info?: any };
    nlp: { state: ServiceState; latencyMs: number | null; info?: any };
  };
};

async function ping(url: string): Promise<{ state: ServiceState; latencyMs: number | null; info?: any }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  const start = Date.now();
  try {
    const res = await fetch(url + '/healthz', { signal: controller.signal });
    const latencyMs = Date.now() - start;
    clearTimeout(timeout);
    if (!res.ok) {
      return { state: 'unreachable', latencyMs };
    }
    const info = await res.json().catch(() => ({}));
    let state: ServiceState = 'ok';
    if (info.status === 'degraded') state = 'degraded';
    else if (info.status === 'down') state = 'down';
    else if (info.status !== 'ok') state = 'unreachable';
    return { state, latencyMs, info };
  } catch {
    return { state: 'unreachable', latencyMs: null };
  }
}

export async function getHealth(): Promise<HealthResponse> {
  const services = await Promise.all([
    ping(SEARCH_API),
    ping(GRAPH_API),
    ping(DOCENTITIES_API),
    ping(NLP_API),
  ]);
  return {
    timestamp: new Date().toISOString(),
    services: {
      search: services[0],
      graph: services[1],
      docentities: services[2],
      nlp: services[3],
    },
  };
}

export default async function handler(_req: NextApiRequest, res: NextApiResponse) {
  const data = await getHealth();
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).json(data);
}
