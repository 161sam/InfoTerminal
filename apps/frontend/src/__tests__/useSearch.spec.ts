import { renderHook, waitFor } from "@testing-library/react";
import { useSearch } from "../hooks/useSearch";
import * as endpoints from "../hooks/useEndpoints";
import { describe, it, expect, vi } from "vitest";

describe("useSearch", () => {
  it("posts filters and sort", async () => {
    vi.spyOn(endpoints, "default").mockReturnValue({ SEARCH_API: "http://api" } as any);
    const fetchMock = vi
      .fn()
      .mockResolvedValue({ ok: true, json: async () => ({ items: [], total: 0 }) });
    (global as any).fetch = fetchMock;
    renderHook(() => useSearch({ q: "apple", filters: { source: ["osint"] }, sort: "date_desc" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    const body = JSON.parse(fetchMock.mock.calls[0][1].body);
    expect(body.filters.source).toEqual(["osint"]);
    expect(body.sort.order).toBe("desc");
  });
});
