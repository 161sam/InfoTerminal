import config from './config';
import { isBrowser } from './safe';

export interface EndpointSettings {
  SEARCH_API: string;
  GRAPH_API: string;
  VIEWS_API: string;
  DOCENTITIES_API?: string;
  NLP_API?: string;
  [key: string]: string | undefined;
}

const STORAGE_KEY = 'it.settings.endpoints';

export const defaultEndpoints: EndpointSettings = {
  SEARCH_API: config.SEARCH_API,
  GRAPH_API: config.GRAPH_API,
  VIEWS_API: config.VIEWS_API,
  DOCENTITIES_API: config.DOCENTITIES_API,
  NLP_API: config.NLP_API,
};

export function loadEndpoints(): EndpointSettings {
  if (!isBrowser()) return { ...defaultEndpoints };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? { ...defaultEndpoints, ...JSON.parse(raw) } : { ...defaultEndpoints };
  } catch {
    return { ...defaultEndpoints };
  }
}

export function saveEndpoints(values: EndpointSettings) {
  if (!isBrowser()) return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(values));
}

export function sanitizeUrl(url: string): string {
  return url.trim().replace(/\/$/, '');
}

export function validateUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch {
    return false;
  }
}

export { STORAGE_KEY };
