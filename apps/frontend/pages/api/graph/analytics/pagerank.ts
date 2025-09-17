import type { NextApiRequest, NextApiResponse } from 'next';

function graphUrl() {
  return process.env.NEXT_PUBLIC_GRAPH_API || 'http://localhost:8612';
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const params = new URLSearchParams();
    if (req.query.node_type) params.set('node_type', String(req.query.node_type));
    if (req.query.limit) params.set('limit', String(req.query.limit));
    const r = await fetch(`${graphUrl()}/analytics/pagerank?${params.toString()}`);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e: any) {
    res.status(502).json({ error: e?.message || 'graph-api unavailable' });
  }
}

