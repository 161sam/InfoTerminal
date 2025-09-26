import { isBrowser } from "./safe";
import { toSearchParams } from "@/lib/url";
import { GRAPH_DEEPLINK_FALLBACK } from "./config";

export const DEEPLINK_STORAGE_KEY = "it.settings.graph.deeplinkBase";

export function getGraphDeeplinkBase(): string {
  if (isBrowser()) {
    try {
      const v = localStorage.getItem(DEEPLINK_STORAGE_KEY);
      if (v) return v;
    } catch {
      /* ignore */
    }
  }
  return GRAPH_DEEPLINK_FALLBACK;
}

export interface BuildGraphLinkParams {
  id: string;
  base?: string;
  type?: string;
  q?: string;
  highlight?: string[];
  filters?: Record<string, string | string[]>;
  layout?: "force" | "grid" | "tree" | string;
  abs?: boolean;
}

export function buildGraphDeepLink(params: BuildGraphLinkParams): string {
  const base = params.base ?? getGraphDeeplinkBase();
  const isAbsolute = /^https?:\/\//i.test(base);
  let url = base + encodeURIComponent(params.id);
  const qIndex = url.indexOf("?");
  const path = qIndex >= 0 ? url.slice(0, qIndex) : url;
  const query = qIndex >= 0 ? url.slice(qIndex + 1) : "";
  // When a raw query string is provided, construct URLSearchParams directly
  const search = new URLSearchParams(query);

  if (params.type) search.set("type", params.type);
  if (params.layout) search.set("layout", params.layout);
  if (params.q) search.set("q", params.q);
  if (params.highlight && params.highlight.length) {
    search.set("highlight", params.highlight.join(","));
  }
  if (params.filters) {
    for (const [k, v] of Object.entries(params.filters)) {
      const key = `f.${k}`;
      if (Array.isArray(v)) v.forEach((val) => search.append(key, val));
      else search.append(key, v);
    }
  }

  let final = `${path}?${search.toString()}`;
  if (params.abs && !isAbsolute && isBrowser()) {
    final = `${location.origin}${final}`;
  }
  return final;
}

export default buildGraphDeepLink;
