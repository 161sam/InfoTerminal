import { test, expect } from "@playwright/test";

const BASE = process.env.E2E_BASE_URL || "http://localhost:3411";

test("Agent and NLP pages render without public env via proxy rewrites", async ({ page }) => {
  await page.goto(`${BASE}/agent`);
  await expect(page.getByText(/Agent/i)).toBeVisible();
  await expect(page.getByText(/nicht konfiguriert/i)).toHaveCount(0);

  await page.goto(`${BASE}/nlp`);
  await expect(page.getByText(/NLP/i)).toBeVisible();
  await expect(page.getByText(/nicht konfiguriert/i)).toHaveCount(0);
});
