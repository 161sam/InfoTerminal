import { test, expect } from '@playwright/test';
import { dummyLogin } from '../helpers/auth';

test('smoke: login, search, open graph', async ({ page }) => {
  await page.goto('/');
  await dummyLogin(page);

  await page.getByPlaceholder('Search').fill('apple');
  await page.getByRole('button', { name: /search/i }).click();
  await expect(page.getByTestId('search-results')).toBeVisible();

  await page.goto('/graph');
  await expect(page.getByTestId('graph-view')).toBeVisible();
});
