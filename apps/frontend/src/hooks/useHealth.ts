import { useEffect, useState } from 'react';
import config from '@/lib/config';

type Health = { key: string; name: string; url: string; ok: boolean; status?: number; error?: string };

const SERVICES: Array<{key:string; name:string; base:string}> = [
  { key: 'search', name: 'search-api', base: config.SEARCH_API },
  { key: 'graph',  name: 'graph-api',  base: config.GRAPH_API },
  { key: 'docs',   name: 'doc-entities', base: config.DOCENTITIES_API },
  // { key: 'er', name: 'entity-resolution', base: process.env.NEXT_PUBLIC_ER_API ?? 'http://localhost:8404' }, // TODO: optional einblenden
];

function healthUrl(base: string) {
  return `${base.replace(/\/$/, '')}/healthz`;
}

export function useHealth() {
  const [items, setItems] = useState<Health[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancel = false;
    (async () => {
      try {
        const results: Health[] = await Promise.all(
          SERVICES.map(async (s) => {
            const url = healthUrl(s.base);
            try {
              const res = await fetch(url, { method: 'GET' });
              const ok = res.ok;
              return { key: s.key, name: s.name, url, ok, status: res.status };
            } catch (e: any) {
              return { key: s.key, name: s.name, url, ok: false, error: String(e) };
            }
          }),
        );
        if (!cancel) setItems(results);
      } finally {
        if (!cancel) setLoading(false);
      }
    })();
    return () => {
      cancel = true;
    };
  }, []);

  return { items, loading };
}
