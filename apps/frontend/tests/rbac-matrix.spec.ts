import { describe, expect, it } from "vitest";
import { canonicalizeRoles, summarizeFeatureAccess } from "@/lib/auth/rbac";

describe("RBAC feature matrix", () => {
  it("matches expected access per role", () => {
    const roles = ["admin", "ops", "analyst", "viewer"] as const;
    const matrix = roles.map((role) => ({
      role,
      canonical: canonicalizeRoles([role]),
      access: summarizeFeatureAccess([role]),
    }));

    expect(matrix).toMatchInlineSnapshot(`
      [
        {
          "access": {
            "dossierExport": true,
            "opsActions": true,
            "pluginRunner": true,
            "videoAnalysis": true,
          },
          "canonical": [
            "admin",
          ],
          "role": "admin",
        },
        {
          "access": {
            "dossierExport": false,
            "opsActions": true,
            "pluginRunner": true,
            "videoAnalysis": false,
          },
          "canonical": [
            "ops",
          ],
          "role": "ops",
        },
        {
          "access": {
            "dossierExport": true,
            "opsActions": false,
            "pluginRunner": false,
            "videoAnalysis": true,
          },
          "canonical": [
            "analyst",
          ],
          "role": "analyst",
        },
        {
          "access": {
            "dossierExport": false,
            "opsActions": false,
            "pluginRunner": false,
            "videoAnalysis": false,
          },
          "canonical": [
            "viewer",
          ],
          "role": "viewer",
        },
      ]
    `);
  });
});
