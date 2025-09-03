import { useRouter } from 'next/router';
import { useCallback } from 'react';

/**
 * Helper hook to interact with URL search parameters.
 */
export function useSearchParams() {
  const router = useRouter();
  const params = router.query;

  const get = useCallback(
    (key: string): string | string[] | undefined => {
      return params[key] as any;
    },
    [params],
  );

  const set = useCallback(
    (key: string, value: any) => {
      const q = { ...router.query } as Record<string, any>;
      if (value === undefined || value === null || value === '') delete q[key];
      else q[key] = value;
      router.replace({ pathname: router.pathname, query: q }, undefined, { shallow: true });
    },
    [router],
  );

  const toggleArrayParam = useCallback(
    (key: string, value: string) => {
      const current = router.query[key];
      const arr = Array.isArray(current) ? [...current] : current ? [current] : [];
      const idx = arr.indexOf(value);
      if (idx >= 0) arr.splice(idx, 1);
      else arr.push(value);
      set(key, arr.length ? arr : undefined);
    },
    [router, set],
  );

  const replaceAll = useCallback(
    (next: Record<string, any>) => {
      router.replace({ pathname: router.pathname, query: next }, undefined, { shallow: true });
    },
    [router],
  );

  return { params, get, set, toggleArrayParam, replaceAll };
}
