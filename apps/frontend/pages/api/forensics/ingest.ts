import type { NextApiRequest, NextApiResponse } from 'next';

function forensicsUrl() {
  const port = process.env.IT_PORT_FORENSICS || '8627';
  return process.env.FORENSICS_URL || `http://localhost:${port}`;
}

export const config = { api: { bodyParser: false } };

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  try {
    const form = await (await import('formidable')).default;
    const parser = form({ multiples: false });
    parser.parse(req, async (err: any, _fields: any, files: any) => {
      if (err) return res.status(400).json({ error: 'parse error' });
      const f = files.file || files.upload || Object.values(files)[0];
      if (!f) return res.status(400).json({ error: 'no file' });
      const fs = await import('fs');
      const data = fs.readFileSync(Array.isArray(f) ? f[0].filepath : f.filepath);
      const r = await fetch(`${forensicsUrl()}/ingest`, { method: 'POST', body: data, headers: { 'Content-Type': 'application/octet-stream' } });
      const json = await r.json();
      return res.status(r.status).json(json);
    });
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || 'forensics unavailable' });
  }
}

