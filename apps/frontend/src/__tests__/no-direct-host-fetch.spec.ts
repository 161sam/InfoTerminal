import { ESLint } from 'eslint';
import path from 'path';
import { expect, test } from 'vitest';

test('no direct host fetch rule triggers', async () => {
  const eslint = new ESLint({ useEslintrc: true, cwd: path.join(__dirname, '..') });
  const results = await eslint.lintText("fetch('http://localhost:1234')\n");
  expect(results[0].errorCount).toBeGreaterThan(0);
});
