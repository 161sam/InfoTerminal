import { render, screen, waitFor } from "@testing-library/react";
import type { NextRouter } from "next/router";
import SearchPage from "../../pages/search";

function createMockRouter(router: Partial<NextRouter>): NextRouter {
  return {
    basePath: "",
    pathname: "/search",
    route: "/search",
    query: {},
    asPath: "/search",
    push: vi.fn(),
    replace: vi.fn(),
    reload: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn().mockResolvedValue(undefined),
    beforePopState: vi.fn(),
    events: { on: vi.fn(), off: vi.fn(), emit: vi.fn() },
    isFallback: false,
    isReady: true,
    isLocaleDomain: false,
    isPreview: false,
    forward: vi.fn(),
    ...router,
  } as NextRouter;
}

vi.mock("next/router", () => ({
  useRouter: () => createMockRouter({ query: { q: "acme" } }),
}));

test("renders search results from API", async () => {
  (global as any).fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ items: [{ id: "1", title: "Doc 1" }], total: 1, aggregations: {} }),
  });
  render(<SearchPage />);
  await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  await waitFor(() => expect(screen.getByText("Doc 1")).toBeInTheDocument());
});
