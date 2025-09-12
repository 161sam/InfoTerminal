import { useCallback, useEffect, useState } from 'react';
import type { HealthResponse } from '../../pages/api/health';

export function useHealth(pollIntervalMs = 15000) {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const res = await fetch('/api/health');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: HealthResponse = await res.json();
      setData(json);
      setError(null);
    } catch (e: any) {
      setError(e.message || 'health check failed');
    }
  }, []);

  useEffect(() => {
    refresh();
    if (pollIntervalMs > 0) {
      const id = setInterval(refresh, pollIntervalMs);
      return () => clearInterval(id);
    }
  }, [refresh, pollIntervalMs]);

  const stateAggregate = error
    ? 'unreachable'
    : data
    ? Object.values(data.services).some(
        (s) => s.state === 'down' || s.state === 'unreachable'
      )
      ? 'unreachable'
      : Object.values(data.services).some((s) => s.state === 'degraded')
      ? 'degraded'
      : 'ok'
    : 'ok';

  return { data, error, refresh, stateAggregate };
}

export default useHealth;
