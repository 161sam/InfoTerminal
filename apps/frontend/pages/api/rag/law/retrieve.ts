import type { NextApiRequest, NextApiResponse } from 'next';

function ragUrl() {
  const port = process.env.IT_PORT_RAG_API || '8622';
  return process.env.RAG_API_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { q, top_k } = req.query as { q?: string; top_k?: string };
  if (!q) return res.status(400).json({ error: 'Missing q' });
  try {
    const r = await fetch(`${ragUrl()}/law/retrieve?q=${encodeURIComponent(q)}&top_k=${top_k || '10'}`);
    const data = await r.json();
    return res.status(r.status).json(data);
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || 'rag-api unavailable' });
  }
}

