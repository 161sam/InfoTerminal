import { test, expect } from '@playwright/test';
import { dummyLogin } from '../helpers/auth';

test('sidebar exposes /agent and /nlp', async ({ page }) => {
  await page.goto('/');
  await dummyLogin(page);
  await page.goto('/');
  await expect(page.getByRole('link', { name: 'Agent' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'NLP' })).toBeVisible();
  await page.getByRole('link', { name: 'Agent' }).click();
  await expect(page).toHaveURL(/\/agent/);
});
