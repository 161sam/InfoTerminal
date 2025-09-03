export const SEARCH_API = process.env.NEXT_PUBLIC_SEARCH_API || '';
if (!SEARCH_API) console.warn('NEXT_PUBLIC_SEARCH_API is not set');

export const GRAPH_API = process.env.NEXT_PUBLIC_GRAPH_API || '';
if (!GRAPH_API) console.warn('NEXT_PUBLIC_GRAPH_API is not set');

export const DOCENTITIES_API = process.env.NEXT_PUBLIC_DOCENTITIES_API || '';
if (!DOCENTITIES_API) console.warn('NEXT_PUBLIC_DOCENTITIES_API is not set');

export const NLP_API = process.env.NEXT_PUBLIC_NLP_API || '';
if (!NLP_API) console.warn('NEXT_PUBLIC_NLP_API is not set');

export const GRAFANA_URL = process.env.NEXT_PUBLIC_GRAFANA_URL || '';

export const SEARCH_FILTER_MODE =
  process.env.NEXT_PUBLIC_SEARCH_FILTER_MODE || 'quote_query';
