// Enhanced configuration for InfoTerminal with Agent integration
// Updated to support new doc-entities service and remove legacy nlp-service references

export const DIRECT_ENDPOINTS = {
  SEARCH_API: process.env.NEXT_PUBLIC_SEARCH_API ?? "http://127.0.0.1:8401",
  GRAPH_API: process.env.NEXT_PUBLIC_GRAPH_API ?? "http://127.0.0.1:8402",
  VIEWS_API: process.env.NEXT_PUBLIC_VIEWS_API ?? "http://127.0.0.1:8403",
} as const;

export const OTHER_ENDPOINTS = {
  // New doc-entities service (replaces legacy nlp-service)
  DOCENTITIES_API: process.env.NEXT_PUBLIC_DOCENTITIES_API ?? "http://127.0.0.1:8613",

  // Agent services
  AGENT_API: process.env.NEXT_PUBLIC_AGENT_API ?? "http://127.0.0.1:8610",
  DOC_ENTITIES_API: process.env.NEXT_PUBLIC_DOC_ENTITIES_API ?? "http://127.0.0.1:8613",

  // External integrations
  FLOWISE_API: process.env.NEXT_PUBLIC_FLOWISE_API ?? "http://127.0.0.1:8620",
  N8N_API: process.env.NEXT_PUBLIC_N8N_URL ?? "http://127.0.0.1:5678",
} as const;

export const GATEWAY_URL = process.env.NEXT_PUBLIC_GATEWAY_URL ?? "http://127.0.0.1:8610";
export const GATEWAY_ENABLED_DEFAULT = (process.env.NEXT_PUBLIC_GATEWAY_ENABLED ?? "0") === "1";
export const GRAPH_DEEPLINK_FALLBACK =
  process.env.NEXT_PUBLIC_GRAPH_DEEPLINK_BASE ?? "/graphx?focus=";

// Agent-specific configuration
export const AGENT_CONFIG = {
  defaultType: process.env.NEXT_PUBLIC_AGENT_DEFAULT_TYPE ?? "research_assistant",
  maxIterations: parseInt(process.env.NEXT_PUBLIC_AGENT_MAX_ITERATIONS ?? "10"),
  includeSteps: process.env.NEXT_PUBLIC_AGENT_INCLUDE_STEPS === "true",
  timeout: parseInt(process.env.NEXT_PUBLIC_AGENT_TIMEOUT ?? "300000"),
  debugMode: process.env.NEXT_PUBLIC_DEBUG_AGENT === "true",
} as const;

// Feature flags
export const FEATURES = {
  agent: process.env.NEXT_PUBLIC_FEATURE_AGENT === "1",
  nlp: process.env.NEXT_PUBLIC_FEATURE_NLP === "1",
  plugins: process.env.NEXT_PUBLIC_FEATURE_PLUGINS === "1",
  workflows: process.env.NEXT_PUBLIC_FEATURE_WORKFLOWS === "1",
  multiAgent: process.env.NEXT_PUBLIC_FEATURE_MULTI_AGENT === "1",
} as const;

// Enhanced API getter with agent support
export function getApis() {
  const agent = process.env.NEXT_PUBLIC_AGENT_API?.trim();
  const docEntities = process.env.NEXT_PUBLIC_DOC_ENTITIES_API?.trim();
  const flowise = process.env.NEXT_PUBLIC_FLOWISE_API?.trim();

  // Fallback to relative API routes for Next.js API integration
  const relAgent = "/api/agent";
  const relDocEntities = "/api/doc-entities";
  const relFlowise = "/api/flowise";

  return {
    // Core APIs
    ...DIRECT_ENDPOINTS,

    // Agent APIs with fallbacks
    AGENT_API: agent && agent.length > 0 ? agent : relAgent,
    DOC_ENTITIES_API: docEntities && docEntities.length > 0 ? docEntities : relDocEntities,
    DOCENTITIES_API: OTHER_ENDPOINTS.DOCENTITIES_API,
    FLOWISE_API: flowise && flowise.length > 0 ? flowise : relFlowise,

    // External APIs
    N8N_API: OTHER_ENDPOINTS.N8N_API,
  } as const;
}

// Agent-specific API configuration
export function getAgentApis() {
  const apis = getApis();
  return {
    primary: apis.AGENT_API,
    docEntities: apis.DOC_ENTITIES_API,
    flowise: apis.FLOWISE_API,
    n8n: apis.N8N_API,
  };
}

// Health check URLs
export function getHealthCheckUrls() {
  const apis = getApis();
  return {
    agent: `${apis.AGENT_API}/healthz`,
    docEntities: `${apis.DOC_ENTITIES_API}/healthz`,
    flowise: `${apis.FLOWISE_API}/health`,
    search: `${apis.SEARCH_API}/healthz`,
    graph: `${apis.GRAPH_API}/healthz`,
    views: `${apis.VIEWS_API}/healthz`,
  };
}

// Check if agent features are enabled
export function isAgentEnabled(): boolean {
  return FEATURES.agent;
}

export function isMultiAgentEnabled(): boolean {
  return FEATURES.multiAgent && FEATURES.agent;
}

export function isWorkflowsEnabled(): boolean {
  return FEATURES.workflows;
}

const config = {
  ...DIRECT_ENDPOINTS,
  ...OTHER_ENDPOINTS,
  GATEWAY_URL,
  GATEWAY_ENABLED_DEFAULT,
  AGENT_CONFIG,
  FEATURES,
} as const;

export type Config = typeof config;
export default config;
