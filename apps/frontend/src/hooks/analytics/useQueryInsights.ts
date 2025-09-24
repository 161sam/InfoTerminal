// Hook for query insights data
import { useState, useEffect, useCallback } from "react";
import { analyticsApi } from "../../lib/api-client";
import { QueryInsights, AnalyticsFilters } from "../analytics/types";

export function useQueryInsights(filters: AnalyticsFilters) {
  const [data, setData] = useState<QueryInsights | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchQueryInsights = useCallback(async () => {
    if (!filters.timeRange) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getQueryInsights(filters);

      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state - this feature might not be available
        setData({
          totalQueries: 0,
          uniqueQueries: 0,
          topQueries: [],
          searchPatterns: [],
          clickthrough: {
            averageRate: 0,
            topResults: 0,
            documentTypes: {},
          },
          performance: {
            averageResponseTime: 0,
            slowQueries: [],
            errorRate: 0,
          },
        });

        if (response.error) {
          console.warn("Query insights service unavailable:", response.error);
        }
      }
    } catch (err) {
      console.warn("Error fetching query insights:", err);
      setError(err instanceof Error ? err.message : "Unknown error");

      setData({
        totalQueries: 0,
        uniqueQueries: 0,
        topQueries: [],
        searchPatterns: [],
        clickthrough: {
          averageRate: 0,
          topResults: 0,
          documentTypes: {},
        },
        performance: {
          averageResponseTime: 0,
          slowQueries: [],
          errorRate: 0,
        },
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchQueryInsights();
  }, [fetchQueryInsights]);

  const refresh = useCallback(() => {
    fetchQueryInsights();
  }, [fetchQueryInsights]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
