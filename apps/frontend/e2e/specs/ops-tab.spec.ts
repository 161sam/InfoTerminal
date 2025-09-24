import { test, expect } from "@playwright/test";
import { dummyLogin } from "../helpers/auth";

test("ops tab shows stacks and logs", async ({ page }) => {
  test.skip(process.env.NEXT_PUBLIC_FEATURE_OPS !== "1", "ops feature disabled");

  await page.route("**/api/ops/stacks", (route) =>
    route.fulfill({ body: JSON.stringify({ stacks: { core: { title: "Core", files: [] } } }) }),
  );
  await page.route("**/api/ops/stacks/core/status", (route) =>
    route.fulfill({ body: JSON.stringify({ stack: "core", services: [] }) }),
  );
  await page.route("**/api/ops/stacks/core/up", (route) =>
    route.fulfill({ body: JSON.stringify({ ok: true }) }),
  );
  await page.route("**/api/ops/stacks/core/logs", (route) => route.fulfill({ body: "line1\n" }));

  await page.goto("/settings");
  await dummyLogin(page);
  await page.goto("/settings");
  await page.getByRole("tab", { name: "Ops" }).click();
  await expect(page.getByText("Core")).toBeVisible();
  await page.getByText("Logs").click();
  await expect(page.getByText("line1")).toBeVisible();
});
