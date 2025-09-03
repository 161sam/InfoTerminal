export type SearchHit = {
  id: string;
  title?: string;
  snippet?: string;
  score?: number;
  entity_types?: string[];
  node_id?: string;
  source?: string;
  meta?: Record<string, any>;
  highlights?: { field: string; fragments: string[] }[];
};

export type FacetBucket = { key: string; doc_count: number };
export type Aggregations = Record<string, FacetBucket[]>;

export type SearchResponse = {
  items: SearchHit[];
  total: number;
  aggregations?: Aggregations;
};
