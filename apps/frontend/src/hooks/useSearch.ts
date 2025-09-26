import { useEffect, useState, useMemo } from "react";
import type { SearchResponse } from "../types/search";
import useEndpoints from "./useEndpoints";
import { sanitizeUrl } from "@/lib/endpoints";

const DEFAULT_FACETS = ["entity_types", "source"];

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

  const filtersKey = useMemo(() => JSON.stringify(params.filters || {}), [params.filters]);
  const entityKey = useMemo(() => (params.entity || []).join(","), [params.entity]);
  const valueKey = useMemo(() => (params.value || []).join(","), [params.value]);

  const computedFilters = useMemo(() => {
    const base: Record<string, string[]> = JSON.parse(filtersKey || "{}");
    const entityArr = entityKey ? entityKey.split(",").filter(Boolean) : undefined;
    const valueArr = valueKey ? valueKey.split(",").filter(Boolean) : undefined;
    const f: Record<string, string[]> = { ...base };
    if (entityArr && entityArr.length) f["entity_type"] = entityArr;
    if (valueArr && valueArr.length) f["value"] = valueArr;
    return f;
  }, [filtersKey, entityKey, valueKey]);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    const controller = new AbortController();
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const page = params.page ?? 1;
        const pageSize = params.pageSize ?? 20;

        const filters: Record<string, string[]> = computedFilters;

        let sort: any = undefined;
        if (params.sort && params.sort !== "relevance") {
          sort = { field: "meta.created_at", order: params.sort === "date_desc" ? "desc" : "asc" };
        }

        const body: any = {
          q: params.q,
          filters,
          facets: DEFAULT_FACETS,
          limit: pageSize,
          offset: (page - 1) * pageSize,
        };
        if (sort) body.sort = sort;

        const headers: Record<string, string> = { "Content-Type": "application/json" };
        if (params.rerank) headers["X-Rerank"] = "1";

        const base = sanitizeUrl(SEARCH_API);
        const res = await fetch(`${base}/query`, {
          method: "POST",
          headers,
          body: JSON.stringify(body),
          signal: controller.signal,
        });
        if (!res.ok) throw new Error(await res.text());
        const json = (await res.json()) as SearchResponse;
        setData(json);
      } catch (e: any) {
        if (e.name !== "AbortError") {
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
    computedFilters,
    SEARCH_API,
  ]);

  return { data, loading, error };
}
