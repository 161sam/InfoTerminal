import { useEffect, useRef, useState } from 'react';
import type { HealthResponse } from '../../pages/api/health';
import type { ServiceState } from '../components/health/StatusDot';

export function useHealth(intervalMs: number = 15000) {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const fetchHealth = async () => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    try {
      setLoading(true);
      const res = await fetch('/api/health', { signal: controller.signal });
      if (!res.ok) throw new Error(res.statusText);
      const json = await res.json();
      setData(json);
      setError(null);
    } catch (e: any) {
      if (e.name === 'AbortError') return;
      setError(e);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const t = setTimeout(() => {
      fetchHealth();
    }, 250);
    return () => {
      clearTimeout(t);
      abortRef.current?.abort();
    };
  }, []);

  useEffect(() => {
    const id = setInterval(fetchHealth, intervalMs);
    return () => clearInterval(id);
  }, [intervalMs]);

  const refresh = () => fetchHealth();

  const aggregate = (): ServiceState => {
    const states = Object.values(data?.services || {}).map((s) => s.state);
    if (states.some((s) => s === 'down' || s === 'unreachable')) return 'unreachable';
    if (states.some((s) => s === 'degraded')) return 'degraded';
    return 'ok';
  };

  return { data, loading, error, refresh, stateAggregate: aggregate() };
}
