// Import as any to avoid type dependency on ESLint
// Types are provided by @types/eslint if available
// eslint-disable-next-line
const rule = require("../../../../tools/eslint-rules/no-direct-host-fetch.js");
import { expect, test } from "vitest";

test("no direct host fetch rule triggers", () => {
  const reports: any[] = [];
  const context = {
    report: (info: any) => reports.push(info),
  } as any;

  const listeners = rule.create(context);
  listeners.CallExpression({
    callee: { name: "fetch" },
    arguments: [{ type: "Literal", value: "http://localhost:1234" }],
  });

  expect(reports.length).toBeGreaterThan(0);
});
