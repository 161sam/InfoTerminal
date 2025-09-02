import { Page } from '@playwright/test';

export async function dummyLogin(page: Page) {
  await page.addInitScript(token => {
    localStorage.setItem('auth.token', token as string);
  }, process.env.E2E_DUMMY_TOKEN || 'test-token');
}
