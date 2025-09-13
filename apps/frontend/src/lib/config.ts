export const DIRECT_ENDPOINTS = {
  SEARCH_API: process.env.NEXT_PUBLIC_SEARCH_API ?? 'http://127.0.0.1:8401',
  GRAPH_API: process.env.NEXT_PUBLIC_GRAPH_API ?? 'http://127.0.0.1:8402',
  VIEWS_API: process.env.NEXT_PUBLIC_VIEWS_API ?? 'http://127.0.0.1:8403',
} as const;

export const OTHER_ENDPOINTS = {
  DOCENTITIES_API: process.env.NEXT_PUBLIC_DOCENTITIES_API ?? 'http://127.0.0.1:8613',
  NLP_API: process.env.NEXT_PUBLIC_NLP_API ?? 'http://127.0.0.1:8404',
  AGENT_API: process.env.NEXT_PUBLIC_AGENT_API ?? 'http://127.0.0.1:8610',
} as const;

export const GATEWAY_URL = process.env.NEXT_PUBLIC_GATEWAY_URL ?? 'http://127.0.0.1:8610';
export const GATEWAY_ENABLED_DEFAULT =
  (process.env.NEXT_PUBLIC_GATEWAY_ENABLED ?? '0') === '1';
export const GRAPH_DEEPLINK_FALLBACK =
  process.env.NEXT_PUBLIC_GRAPH_DEEPLINK_BASE ?? '/graphx?focus=';

export function getApis() {
  const agent = process.env.NEXT_PUBLIC_AGENT_API?.trim();
  const nlp = process.env.NEXT_PUBLIC_DOC_ENTITIES_API?.trim();
  const relAgent = '/api/agent';
  const relNlp = '/api/doc-entities';
  return {
    AGENT_API: agent && agent.length > 0 ? agent : relAgent,
    DOC_ENTITIES_API: nlp && nlp.length > 0 ? nlp : relNlp,
  } as const;
}

const config = {
  ...DIRECT_ENDPOINTS,
  ...OTHER_ENDPOINTS,
  GATEWAY_URL,
  GATEWAY_ENABLED_DEFAULT,
} as const;

export type Config = typeof config;
export default config;
