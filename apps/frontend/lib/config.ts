export const config = {
  SEARCH_API:      process.env.NEXT_PUBLIC_SEARCH_API      ?? "http://localhost:8611",
  GRAPH_API:       process.env.NEXT_PUBLIC_GRAPH_API       ?? "http://localhost:8612",
  DOCENTITIES_API: process.env.NEXT_PUBLIC_DOCENTITIES_API ?? "http://localhost:8613",
  NLP_API:         process.env.NEXT_PUBLIC_NLP_API         ?? "http://localhost:8404",
  VIEWS_API:       process.env.NEXT_PUBLIC_VIEWS_API       ?? "http://localhost:8403",
} as const;
export default config;
