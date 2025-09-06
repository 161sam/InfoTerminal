import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import {
  listDemoFiles,
  fileSha1,
  readLoaded,
  writeLoaded,
  ingestToAleph,
  annotateText,
  loadSeeds,
} from '@/lib/demoLoader';

type LoadOpts = {
  ingestAleph?: boolean;
  annotate?: boolean;
  seedGraph?: boolean;
  seedSearch?: boolean;
  reset?: boolean;
};

const defaults: LoadOpts = {
  ingestAleph: true,
  annotate: true,
  seedGraph: false,
  seedSearch: false,
  reset: false,
};

export async function loadDemo(opts: LoadOpts) {
  const o = { ...defaults, ...opts };
  let state = o.reset ? {} : readLoaded();
  const files = listDemoFiles();
  const ingested: any[] = [];
  const skipped: any[] = [];
  const notes: string[] = [];

  for (const file of files) {
    const hash = fileSha1(file);
    const filename = path.basename(file);
    if (state[hash]) {
      skipped.push({ file: filename });
      continue;
    }
    let aleph_id: string | undefined;
    if (o.ingestAleph) {
      try {
        const r = await ingestToAleph(file);
        aleph_id = r.id || r.aleph_id;
      } catch (e: any) {
        notes.push(`ingest failed for ${filename}: ${e.message}`);
        continue;
      }
    }
    if (o.annotate) {
      if (file.endsWith('.txt')) {
        try {
          const text = fs.readFileSync(file, 'utf-8');
          await annotateText(text, { title: filename, aleph_id, source: 'demo-loader' });
        } catch (e: any) {
          notes.push(`annotate failed for ${filename}: ${e.message}`);
        }
      } else {
        notes.push('pdf has no text, skipped annotate');
      }
    }
    state[hash] = { file: filename, aleph_id };
    ingested.push({ file: filename, aleph_id });
  }

  writeLoaded(state);

  if (o.seedGraph || o.seedSearch) {
    const seedNotes = await loadSeeds({ seedGraph: o.seedGraph, seedSearch: o.seedSearch });
    notes.push(...seedNotes);
  }

  return { ok: true, count: ingested.length, ingested, skipped, notes };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (process.env.NODE_ENV === 'production' && process.env.ALLOW_DEMO_LOADER !== '1') {
    res.status(403).json({ ok: false, error: 'disabled' });
    return;
  }
  if (req.method !== 'POST') {
    res.status(405).json({ ok: false });
    return;
  }
  try {
    const data = await loadDemo(req.body || {});
    res.status(200).json(data);
  } catch (e: any) {
    res.status(500).json({ ok: false, error: e.message });
  }
}
