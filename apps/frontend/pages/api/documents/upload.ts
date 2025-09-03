import type { NextApiRequest, NextApiResponse } from 'next';
import formidable from 'formidable';
import fs from 'fs';
import pdf from 'pdf-parse';

export const config = { api: { bodyParser: false } };

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  const form = formidable({ multiples: true });
  form.parse(req, async (err, fields, files) => {
    if (err) {
      res.status(500).json({ ok: false, error: 'parse error' });
      return;
    }
    const fileField = files.file;
    const fileArr = Array.isArray(fileField) ? fileField : [fileField].filter(Boolean) as formidable.File[];
    const results: any[] = [];
    for (const file of fileArr) {
      const title = (fields.title && (fields.title as string)) || file.originalFilename || 'Dokument';
      let text = '';
      try {
        if (file.mimetype === 'text/plain') {
          text = fs.readFileSync(file.filepath, 'utf-8');
        } else if (file.mimetype === 'application/pdf') {
          const data = await pdf(fs.readFileSync(file.filepath));
          text = data.text;
        } else {
          results.push({ file: file.originalFilename, status: 'error', message: 'Filetype not supported' });
          continue;
        }
      } catch {
        results.push({ file: file.originalFilename, status: 'error', message: 'extract failed' });
        continue;
      }
      const payload = { text, meta: { title } };
      try {
        const resp = await fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/annotate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!resp.ok) throw new Error('annotation service error');
        const json = await resp.json();
        results.push({ file: file.originalFilename, status: 'uploaded', doc_id: json.id, aleph_id: json.aleph_id });
      } catch (e: any) {
        results.push({ file: file.originalFilename, status: 'error', message: e.message || 'service error' });
      }
    }
    res.status(200).json({ ok: true, results });
  });
}
