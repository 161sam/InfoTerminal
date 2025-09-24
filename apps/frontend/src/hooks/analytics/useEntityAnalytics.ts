// Hook for entity analytics data
import { useState, useEffect, useCallback } from "react";
import { analyticsApi } from "../../lib/api-client";
import { EntityStats, AnalyticsFilters } from "../analytics/types";

export function useEntityAnalytics(filters: AnalyticsFilters) {
  const [data, setData] = useState<EntityStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEntityAnalytics = useCallback(async () => {
    if (!filters.timeRange) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getEntityStats(filters);

      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state if service unavailable
        setData({
          totalEntities: 0,
          newEntities: 0,
          entityTypes: [],
          topEntities: [],
          relationshipDensity: 0,
          trends: [],
        });

        if (response.error) {
          console.warn("Entity analytics service unavailable:", response.error);
        }
      }
    } catch (err) {
      console.warn("Error fetching entity analytics:", err);
      setError(err instanceof Error ? err.message : "Unknown error");

      // Provide empty state on error
      setData({
        totalEntities: 0,
        newEntities: 0,
        entityTypes: [],
        topEntities: [],
        relationshipDensity: 0,
        trends: [],
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchEntityAnalytics();
  }, [fetchEntityAnalytics]);

  const refresh = useCallback(() => {
    fetchEntityAnalytics();
  }, [fetchEntityAnalytics]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
