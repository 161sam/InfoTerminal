import { describe, expect, it } from "vitest";
import { mapClaimsToUser } from "@/server/oidc";

describe("mapClaimsToUser", () => {
  it("normalizes roles from scopes", () => {
    const user = mapClaimsToUser({
      sub: "user-1",
      email: "user@example.com",
      scope: "openid profile it:role:admin it:role:analyst",
    });

    expect(user?.roles).toEqual(["admin", "analyst"]);
  });

  it("collects roles from various claims and removes duplicates", () => {
    const user = mapClaimsToUser({
      sub: "user-2",
      email: "ops@example.com",
      roles: ["Operations"],
      realm_access: { roles: ["ops"] },
      scp: ["it:role:ops", "it:role:ops"],
    });

    expect(user?.roles).toEqual(["ops"]);
  });

  it("defaults to viewer when no roles are provided", () => {
    const user = mapClaimsToUser({ sub: "user-3", email: "viewer@example.com" });
    expect(user?.roles).toEqual(["viewer"]);
  });
});
