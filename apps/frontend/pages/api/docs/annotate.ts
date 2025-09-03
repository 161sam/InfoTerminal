import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  try {
    const { text, title, source } = req.body;
    const payload = { text, meta: { title, source } };
    const resp = await fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/annotate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const json = await resp.json();
    res.status(resp.status).json(json);
  } catch {
    res.status(502).json({ error: 'annotation service error' });
  }
}
