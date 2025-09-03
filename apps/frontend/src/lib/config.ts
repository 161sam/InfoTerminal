export const cfg = {
  BASE_URL: process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3411',
  SEARCH_API: process.env.NEXT_PUBLIC_SEARCH_API ?? 'http://localhost:8401',
  GRAPH_API: process.env.NEXT_PUBLIC_GRAPH_API ?? 'http://localhost:8402',
  DOC_API:
    process.env.NEXT_PUBLIC_DOCENTITIES_API ??
    process.env.NEXT_PUBLIC_DOC_API ??
    'http://localhost:8406',
};
