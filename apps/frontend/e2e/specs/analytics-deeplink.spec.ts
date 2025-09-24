import { test, expect } from "@playwright/test";

test("superset deeplink opens asset page", async ({ page }) => {
  await page.goto("/test/superset-mock.html");
  await page.click('[data-testid="deeplink"]');
  await expect(page).toHaveURL(/\/asset\/A1/);
  await expect(page.getByTestId("asset-page")).toBeVisible();
});
