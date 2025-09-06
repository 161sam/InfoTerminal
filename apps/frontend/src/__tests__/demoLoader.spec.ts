import path from 'path';
import { expect, test } from 'vitest';
import { fileSha1, readLoaded, writeLoaded, paths } from '@/lib/demoLoader';
import fs from 'fs';

const root = path.join(process.cwd(), '..', '..');

test('hashing and idempotence', () => {
  fs.writeFileSync(paths.LOADED_FILE, '{}');
  const file = path.join(root, 'examples', 'docs', 'demo2.txt');
  const h = fileSha1(file);
  let state = readLoaded();
  expect(state[h]).toBeUndefined();
  state[h] = { file: path.basename(file) };
  writeLoaded(state);
  state = readLoaded();
  expect(state[h].file).toBe(path.basename(file));
});
