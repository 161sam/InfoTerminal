import { getEndpoints, saveGateway, loadGateway } from "@/lib/endpoints";

describe("gateway endpoint resolver", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test("direct mode uses service ports", () => {
    saveGateway({ enabled: false, url: "http://127.0.0.1:8610" });
    const eps = getEndpoints();
    expect(eps.SEARCH_API).toBe("http://127.0.0.1:8401");
    expect(eps.GRAPH_API).toBe("http://127.0.0.1:8402");
    expect(eps.VIEWS_API).toBe("http://127.0.0.1:8403");
  });

  test("gateway mode rewrites endpoints", () => {
    saveGateway({ enabled: true, url: "http://gw:8610" });
    const eps = getEndpoints();
    expect(eps.SEARCH_API).toBe("http://gw:8610/api/search");
    expect(eps.GRAPH_API).toBe("http://gw:8610/api/graph");
    expect(eps.VIEWS_API).toBe("http://gw:8610/api/views");
  });

  test("settings persist in localStorage", () => {
    saveGateway({ enabled: true, url: "http://foo" });
    const loaded = loadGateway();
    expect(loaded).toMatchObject({ enabled: true, url: "http://foo" });
  });
});
