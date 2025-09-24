import config, {
  DIRECT_ENDPOINTS,
  OTHER_ENDPOINTS,
  GATEWAY_URL,
  GATEWAY_ENABLED_DEFAULT,
} from "./config";
import { isBrowser } from "./safe";

export interface EndpointSettings {
  SEARCH_API: string;
  GRAPH_API: string;
  VIEWS_API: string;
  DOCENTITIES_API?: string;
  NLP_API?: string;
  [key: string]: string | undefined;
}

export interface GatewaySetting {
  enabled: boolean;
  url: string;
}

const STORAGE_KEY_ENDPOINTS = "it.settings.endpoints";
export const GATEWAY_STORAGE_KEY = "it.settings.gateway";

export const defaultEndpoints: EndpointSettings = {
  ...DIRECT_ENDPOINTS,
  ...OTHER_ENDPOINTS,
};

export const defaultGateway: GatewaySetting = {
  enabled: GATEWAY_ENABLED_DEFAULT,
  url: GATEWAY_URL,
};

export function loadEndpoints(): EndpointSettings {
  if (!isBrowser()) return { ...defaultEndpoints };
  try {
    const raw = localStorage.getItem(STORAGE_KEY_ENDPOINTS);
    return raw ? { ...defaultEndpoints, ...JSON.parse(raw) } : { ...defaultEndpoints };
  } catch {
    return { ...defaultEndpoints };
  }
}

export function saveEndpoints(values: EndpointSettings) {
  if (!isBrowser()) return;
  localStorage.setItem(STORAGE_KEY_ENDPOINTS, JSON.stringify(values));
}

export function loadGateway(): GatewaySetting {
  if (!isBrowser()) return { ...defaultGateway };
  try {
    const raw = localStorage.getItem(GATEWAY_STORAGE_KEY);
    return raw ? { ...defaultGateway, ...JSON.parse(raw) } : { ...defaultGateway };
  } catch {
    return { ...defaultGateway };
  }
}

export function saveGateway(setting: GatewaySetting) {
  if (!isBrowser()) return;
  localStorage.setItem(GATEWAY_STORAGE_KEY, JSON.stringify(setting));
  window.dispatchEvent(new Event("it-gateway-change"));
}

export function sanitizeUrl(url: string): string {
  return url.trim().replace(/\/$/, "");
}

export function validateUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

export function getEndpoints(): EndpointSettings {
  const gw = loadGateway();
  if (gw.enabled) {
    const base = sanitizeUrl(gw.url || GATEWAY_URL);
    return {
      SEARCH_API: `${base}/api/search`,
      GRAPH_API: `${base}/api/graph`,
      VIEWS_API: `${base}/api/views`,
      ...OTHER_ENDPOINTS,
    };
  }
  return { ...DIRECT_ENDPOINTS, ...OTHER_ENDPOINTS };
}

export { STORAGE_KEY_ENDPOINTS as STORAGE_KEY };
