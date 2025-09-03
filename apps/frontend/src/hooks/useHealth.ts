// apps/frontend/src/hooks/useHealth.ts
import { useEffect, useState, useCallback } from 'react';
import type { HealthResponse, ServiceState } from '../../pages/api/health';

export function useHealth(pollIntervalMs: number = 15000) {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = useCallback(async () => {
    try {
      const response = await fetch('/api/health');
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }
      const healthData = await response.json() as HealthResponse;
      setData(healthData);
      setError(null);
    } catch (err: any) {
      setError(err?.message || 'Health check failed');
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, pollIntervalMs);
    return () => clearInterval(interval);
  }, [fetchHealth, pollIntervalMs]);

  // Calculate aggregate state
  const stateAggregate: ServiceState = data ? 
    Object.values(data.services).some(service => service.state === 'down') ? 'down' :
    Object.values(data.services).some(service => service.state === 'unreachable') ? 'unreachable' :
    Object.values(data.services).some(service => service.state === 'degraded') ? 'degraded' :
    'ok' : 'unreachable';

  return {
    data,
    loading,
    error,
    stateAggregate,
    refresh: fetchHealth
  };
}
