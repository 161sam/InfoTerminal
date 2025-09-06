import type { NextApiRequest, NextApiResponse } from 'next';
import formidable from 'formidable';
import fs from 'fs';
import pdf from 'pdf-parse';

export const config = { api: { bodyParser: false } };

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  const form = formidable();
  form.parse(req, async (err: any, fields: any, files: any) => {
    if (err) {
      res.status(500).json({ error: 'parse error' });
      return;
    }
    const file = files.file as any;
    const title = (fields.title && (fields.title as string)) || file.originalFilename || 'Dokument';
    let text = '';
    try {
      if (file.mimetype === 'text/plain') {
        text = fs.readFileSync(file.filepath, 'utf-8');
      } else if (file.mimetype === 'application/pdf') {
        const data = await pdf(fs.readFileSync(file.filepath));
        text = data.text;
      } else {
        res.status(400).json({ error: 'Unsupported file type' });
        return;
      }
    } catch {
      res.status(500).json({ error: 'extract failed' });
      return;
    }

    const payload = { text, meta: { title } };
    try {
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
  });
}
