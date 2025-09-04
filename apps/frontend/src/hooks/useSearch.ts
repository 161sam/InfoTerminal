import { useEffect, useState } from 'react';
import type { SearchResponse } from '../types/search';
import useEndpoints from './useEndpoints';
import { sanitizeUrl } from '../../lib/endpoints';

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
        const query = new URLSearchParams();
        if (params.q) query.set('q', params.q);
        if (params.sort) query.set('sort', params.sort);
        if (params.rerank) query.set('rerank', '1');
        const page = params.page ?? 1;
        const pageSize = params.pageSize ?? 20;
        query.set('limit', String(pageSize));
        query.set('offset', String((page - 1) * pageSize));
        if (params.entity) params.entity.forEach((e) => query.append('entity_type', e));
        if (params.value) params.value.forEach((v) => query.append('value', v));
        if (params.filters && Object.keys(params.filters).length) {
          query.set('filters', JSON.stringify(params.filters));
        }
        const base = sanitizeUrl(SEARCH_API);
        const res = await fetch(`${base}/search?${query.toString()}`, { signal: controller.signal });
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
