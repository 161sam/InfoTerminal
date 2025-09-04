export const config = {
  SEARCH_API:      process.env.NEXT_PUBLIC_SEARCH_API      ?? "http://127.0.0.1:8401",
  GRAPH_API:       process.env.NEXT_PUBLIC_GRAPH_API       ?? "http://127.0.0.1:8402",
  DOCENTITIES_API: process.env.NEXT_PUBLIC_DOCENTITIES_API ?? "http://127.0.0.1:8403",
  VIEWS_API:       process.env.NEXT_PUBLIC_VIEWS_API       ?? "http://127.0.0.1:8403",
  NLP_API:         process.env.NEXT_PUBLIC_NLP_API         ?? "http://127.0.0.1:8404",
  GRAFANA_URL:     process.env.NEXT_PUBLIC_GRAFANA_URL,
} as const;
export default config;
