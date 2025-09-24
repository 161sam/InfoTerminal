// Hook for evidence quality analytics
import { useState, useEffect, useCallback } from "react";
import { analyticsApi } from "../../lib/api-client";
import { EvidenceQuality, AnalyticsFilters } from "../analytics/types";

export function useEvidenceQuality(filters: AnalyticsFilters) {
  const [data, setData] = useState<EvidenceQuality | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEvidenceQuality = useCallback(async () => {
    if (!filters.timeRange) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getEvidenceQuality(filters);

      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state
        setData({
          overallScore: 0,
          totalClaims: 0,
          verifiedClaims: 0,
          qualityMetrics: [],
          sourceReliability: [],
          corroborationStats: {
            averageSources: 0,
            independentSources: 0,
            crossReferences: 0,
            conflictingClaims: 0,
          },
          recommendations: [],
        });

        if (response.error) {
          console.warn("Evidence quality service unavailable:", response.error);
        }
      }
    } catch (err) {
      console.warn("Error fetching evidence quality:", err);
      setError(err instanceof Error ? err.message : "Unknown error");

      setData({
        overallScore: 0,
        totalClaims: 0,
        verifiedClaims: 0,
        qualityMetrics: [],
        sourceReliability: [],
        corroborationStats: {
          averageSources: 0,
          independentSources: 0,
          crossReferences: 0,
          conflictingClaims: 0,
        },
        recommendations: [],
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchEvidenceQuality();
  }, [fetchEvidenceQuality]);

  const refresh = useCallback(() => {
    fetchEvidenceQuality();
  }, [fetchEvidenceQuality]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
