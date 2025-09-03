import { test, expect } from '@playwright/test';
import fs from 'fs';
import path from 'path';

test('text annotate flow', async ({ page }) => {
  await page.route('**/api/docs/annotate', async route => {
    await route.fulfill({ json: { id: 't1', text: 'Hello', entities: [{ start: 0, end: 5, label: 'WORD' }] } });
  });
  await page.route('**/docs/t1', async route => {
    await route.fulfill({ json: { id: 't1', text: 'Hello', entities: [{ start: 0, end: 5, label: 'WORD' }] } });
  });
  await page.goto('/docs');
  await page.fill('textarea[name="text"]', 'Hello');
  await page.click('text=Annotieren');
  await page.waitForURL('**/docs/t1');
  await expect(page.locator('mark')).toHaveCount(1);
});

test('file upload flow', async ({ page }, testInfo) => {
  await page.route('**/api/docs/upload', async route => {
    await route.fulfill({ json: { id: 'f1', text: 'Hello', entities: [{ start: 0, end: 5, label: 'WORD' }] } });
  });
  await page.route('**/docs/f1', async route => {
    await route.fulfill({ json: { id: 'f1', text: 'Hello', entities: [{ start: 0, end: 5, label: 'WORD' }] } });
  });
  const filePath = path.join(testInfo.outputDir, 'sample.txt');
  fs.writeFileSync(filePath, 'Hello');
  await page.goto('/docs');
  await page.setInputFiles('input[type="file"]', filePath);
  await page.click('text=Upload');
  await page.waitForURL('**/docs/f1');
  await expect(page.locator('mark')).toHaveCount(1);
});
