import { useEffect, useState } from 'react';
import type { SearchResponse } from '../types/search';
import useEndpoints from './useEndpoints';
import { sanitizeUrl } from '@/lib/endpoints';

const DEFAULT_FACETS = ['entity_types', 'source'];

export interface UseSearchInput {
  q?: string;
  filters?: Record<string, string[]>;
  entity?: string[];
  value?: string[];
  sort?: string;
  rerank?: boolean;
  page?: number;
  pageSize?: number;
}

export function useSearch(params: UseSearchInput) {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const { SEARCH_API } = useEndpoints();

  useEffect(() => {
    const controller = new AbortController();
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const page = params.page ?? 1;
        const pageSize = params.pageSize ?? 20;

        const filters: Record<string, string[]> = { ...(params.filters || {}) };
        if (params.entity) filters['entity_type'] = params.entity;
        if (params.value) filters['value'] = params.value;

        let sort: any = undefined;
        if (params.sort && params.sort !== 'relevance') {
            sort = { field: 'meta.created_at', order: params.sort === 'date_desc' ? 'desc' : 'asc' };
        }

        const body: any = {
          q: params.q,
          filters,
          facets: DEFAULT_FACETS,
          limit: pageSize,
          offset: (page - 1) * pageSize,
        };
        if (sort) body.sort = sort;

        const headers: Record<string, string> = { 'Content-Type': 'application/json' };
        if (params.rerank) headers['X-Rerank'] = '1';

        const base = sanitizeUrl(SEARCH_API);
        const res = await fetch(`${base}/query`, {
          method: 'POST',
          headers,
          body: JSON.stringify(body),
          signal: controller.signal,
        });
        if (!res.ok) throw new Error(await res.text());
        const json = (await res.json()) as SearchResponse;
        setData(json);
      } catch (e: any) {
        if (e.name !== 'AbortError') {
          setError(e);
        }
      } finally {
        setLoading(false);
      }
    };
    run();
    return () => controller.abort();
  }, [
    params.q,
    params.sort,
    params.rerank,
    params.page,
    params.pageSize,
    JSON.stringify(params.filters),
    params.entity?.join(','),
    params.value?.join(','),
    SEARCH_API,
  ]);

  return { data, loading, error };
}
