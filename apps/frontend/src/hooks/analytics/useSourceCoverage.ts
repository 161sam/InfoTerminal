// Hook for source coverage analytics
import { useState, useEffect, useCallback } from 'react';
import { analyticsApi } from '../../lib/api-client';
import { SourceCoverage, AnalyticsFilters } from '../analytics/types';

export function useSourceCoverage(filters: AnalyticsFilters) {
  const [data, setData] = useState<SourceCoverage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSourceCoverage = useCallback(async () => {
    if (!filters.timeRange) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getSourceCoverage(filters);
      
      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state
        setData({
          totalSources: 0,
          activeSources: 0,
          sourceTypes: [],
          topSources: [],
          coverage: [],
          timeline: [],
        });
        
        if (response.error) {
          console.warn('Source coverage service unavailable:', response.error);
        }
      }
    } catch (err) {
      console.warn('Error fetching source coverage:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      
      setData({
        totalSources: 0,
        activeSources: 0,
        sourceTypes: [],
        topSources: [],
        coverage: [],
        timeline: [],
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchSourceCoverage();
  }, [fetchSourceCoverage]);

  const refresh = useCallback(() => {
    fetchSourceCoverage();
  }, [fetchSourceCoverage]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
