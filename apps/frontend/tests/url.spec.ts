import { describe, it, expect } from "vitest";
import { toSearchParams, toQueryString } from "@/lib/url";

describe("toSearchParams", () => {
  it("serializes primitives & arrays and filters empty", () => {
    const sp = toSearchParams({
      a: "x",
      b: 1,
      c: true,
      d: new Date("2025-01-02T03:04:05Z"),
      e: ["u", "v"],
      f: undefined,
      g: null,
      h: "",
    });
    const s = sp.toString();
    expect(s).toContain("a=x");
    expect(s).toContain("b=1");
    expect(s).toContain("c=true");
    expect(s).toContain("d=2025-01-02T03%3A04%3A05.000Z");
    expect(s).toContain("e=u");
    expect(s).toContain("e=v");
    expect(s).not.toContain("f=");
    expect(s).not.toContain("g=");
    expect(s).not.toContain("h=");
  });

  it("toQueryString returns leading question mark or empty", () => {
    expect(toQueryString({})).toBe("");
    expect(toQueryString({ a: 1 })).toBe("?a=1");
  });
});
