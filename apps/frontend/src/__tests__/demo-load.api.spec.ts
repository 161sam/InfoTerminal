import fs from 'fs';
import path from 'path';
import { beforeEach, expect, test, vi } from 'vitest';
import { loadDemo } from '../../pages/api/demo/load';
import * as loader from '../../lib/demoLoader';

const loadedFile = loader.paths.LOADED_FILE;
const root = path.join(process.cwd(), '..', '..');

beforeEach(() => {
  fs.mkdirSync(path.dirname(loadedFile), { recursive: true });
  fs.writeFileSync(loadedFile, '{}');
});

test('loads two files and skips on second run', async () => {
  vi.spyOn(loader, 'listDemoFiles').mockReturnValue([
    path.join(root, 'examples', 'docs', 'demo1.pdf'),
    path.join(root, 'examples', 'docs', 'demo2.txt'),
  ]);
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce({ ok: true, json: async () => ({ id: 'a1' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ id: 'b1' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({}) });
  global.fetch = fetchMock as any;
  const r1 = await loadDemo({});
  expect(r1.ingested.length).toBe(2);
  expect(r1.skipped.length).toBe(0);
  fetchMock.mockClear();
  const r2 = await loadDemo({});
  expect(r2.ingested.length).toBe(0);
  expect(r2.skipped.length).toBe(2);
});
