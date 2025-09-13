import { test, expect } from '@playwright/test';

// Ensure sidebar exposes Agent and NLP links and navigation works
// Feature flags default to enabled in dev via ff util

test('sidebar exposes Agent and NLP and navigates', async ({ page }) => {
  await page.goto(process.env.E2E_BASE_URL || 'http://localhost:3411/');
  await expect(page.getByRole('link', { name: 'Agent' })).toBeVisible();
  await page.getByRole('link', { name: 'Agent' }).click();
  await expect(page).toHaveURL(/\/(agent)(\/)?/);
  await expect(page.getByRole('link', { name: 'NLP' })).toBeVisible();
  await page.getByRole('link', { name: 'NLP' }).click();
  await expect(page).toHaveURL(/\/(nlp)(\/)?/);
});
