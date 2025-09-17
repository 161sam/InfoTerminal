import type { NextApiRequest, NextApiResponse } from 'next';

function xaiUrl() {
  const port = process.env.IT_PORT_XAI || '8626';
  return process.env.XAI_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  try {
    const r = await fetch(`${xaiUrl()}/explain/text`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(req.body || {})
    });
    const data = await r.json();
    return res.status(r.status).json(data);
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || 'xai unavailable' });
  }
}

