import { loadEndpoints, saveEndpoints, sanitizeUrl, validateUrl } from "@/lib/endpoints";
import { getEndpoints, defaultEndpoints } from "@/lib/endpoints";

test("persist and load endpoints", () => {
  const vals = { SEARCH_API: "http://a", GRAPH_API: "http://b", VIEWS_API: "http://c" };
  saveEndpoints(vals as any);
  expect(loadEndpoints()).toMatchObject(vals);
});

test("sanitize and validate urls", () => {
  expect(sanitizeUrl("http://foo/")).toBe("http://foo");
  expect(validateUrl("http://foo")).toBe(true);
  expect(validateUrl("bad")).toBe(false);
});

test("deeplink setting does not affect endpoints", () => {
  localStorage.setItem("it.settings.graph.deeplinkBase", "/graphx?focus=");
  expect(getEndpoints()).toMatchObject(defaultEndpoints);
});
