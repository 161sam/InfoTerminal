import { describe, expect, it } from "vitest";
import { normalizeLabel, uniqueEntities } from "@/lib/entities";

describe("entities utils", () => {
  it("normalizes labels", () => {
    expect(normalizeLabel("PER")).toBe("Person");
    expect(normalizeLabel("org")).toBe("Organization");
    expect(normalizeLabel("Loc")).toBe("Location");
    expect(normalizeLabel("email")).toBe("Email");
    expect(normalizeLabel("ipv4")).toBe("IP");
    expect(normalizeLabel("unknown")).toBe("Misc");
  });

  it("deduplicates entities case-insensitively", () => {
    const result = uniqueEntities([
      { label: "PER", value: "Alice" },
      { label: "Person", value: "alice" },
      { label: "ORG", value: "ACME" },
    ]);
    expect(result).toEqual([
      { label: "Organization", value: "ACME", count: 1 },
      { label: "Person", value: "Alice", count: 2 },
    ]);
  });
});
