import type { NextApiRequest, NextApiResponse } from 'next';

function graphUrl() {
  return process.env.NEXT_PUBLIC_GRAPH_API || 'http://localhost:8612';
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const params = new URLSearchParams();
    for (const k of ['dimensions','walk_length','walks_per_node','window_size']) {
      if (req.query[k]) params.set(k, String(req.query[k]));
    }
    const r = await fetch(`${graphUrl()}/analytics/embeddings/node2vec?${params.toString()}`);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e: any) {
    res.status(502).json({ error: e?.message || 'graph-api unavailable' });
  }
}

