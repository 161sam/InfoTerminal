// Hook for timeline data
import { useState, useEffect, useCallback } from 'react';
import { analyticsApi } from '../../lib/api-client';
import { TimelineData, AnalyticsFilters } from '../analytics/types';

export function useTimeline(filters: AnalyticsFilters) {
  const [data, setData] = useState<TimelineData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTimeline = useCallback(async () => {
    if (!filters.timeRange) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getTimeline(filters);
      
      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state
        setData({
          events: [],
          summary: {
            totalEvents: 0,
            timeSpan: '',
            peakPeriod: '',
            categories: {},
          },
          clusters: [],
        });
        
        if (response.error) {
          console.warn('Timeline service unavailable:', response.error);
        }
      }
    } catch (err) {
      console.warn('Error fetching timeline:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      
      setData({
        events: [],
        summary: {
          totalEvents: 0,
          timeSpan: '',
          peakPeriod: '',
          categories: {},
        },
        clusters: [],
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchTimeline();
  }, [fetchTimeline]);

  const refresh = useCallback(() => {
    fetchTimeline();
  }, [fetchTimeline]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
