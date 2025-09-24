// Hook for geospatial entities data
import { useState, useEffect, useCallback } from "react";
import { analyticsApi } from "../../lib/api-client";
import { GeoAnalytics, AnalyticsFilters } from "../analytics/types";

export function useGeoEntities(filters: AnalyticsFilters) {
  const [data, setData] = useState<GeoAnalytics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGeoEntities = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getGeoEntities(filters);

      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state
        setData({
          entities: [],
          clusters: [],
          heatmap: [],
          coverage: {
            countries: 0,
            regions: 0,
            cities: 0,
            coverage: [],
          },
        });

        if (response.error) {
          console.warn("Geospatial service unavailable:", response.error);
        }
      }
    } catch (err) {
      console.warn("Error fetching geo entities:", err);
      setError(err instanceof Error ? err.message : "Unknown error");

      setData({
        entities: [],
        clusters: [],
        heatmap: [],
        coverage: {
          countries: 0,
          regions: 0,
          cities: 0,
          coverage: [],
        },
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchGeoEntities();
  }, [fetchGeoEntities]);

  const refresh = useCallback(() => {
    fetchGeoEntities();
  }, [fetchGeoEntities]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
