// Hook for graph metrics data
import { useState, useEffect, useCallback } from "react";
import { analyticsApi } from "../../lib/api-client";
import { AnalyticsFilters } from "../analytics/types";

export interface GraphMetrics {
  nodeCount: number;
  edgeCount: number;
  density: number;
  clustering: number;
  avgPathLength: number;
  centrality: {
    nodes: Array<{
      id: string;
      name: string;
      score: number;
      type: string;
    }>;
  };
  communities: Array<{
    id: string;
    size: number;
    modularity: number;
    nodes: string[];
  }>;
  pathStats: {
    avgLength: number;
    maxLength: number;
    distribution: Record<number, number>;
  };
}

export function useGraphMetrics(filters: AnalyticsFilters) {
  const [data, setData] = useState<GraphMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGraphMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getGraphMetrics({
        algorithm: "pagerank",
        limit: 20,
        ...filters,
      });

      if (response.success && response.data) {
        setData(response.data);
      } else {
        // Fallback to empty state
        setData({
          nodeCount: 0,
          edgeCount: 0,
          density: 0,
          clustering: 0,
          avgPathLength: 0,
          centrality: { nodes: [] },
          communities: [],
          pathStats: {
            avgLength: 0,
            maxLength: 0,
            distribution: {},
          },
        });

        if (response.error) {
          console.warn("Graph metrics service unavailable:", response.error);
        }
      }
    } catch (err) {
      console.warn("Error fetching graph metrics:", err);
      setError(err instanceof Error ? err.message : "Unknown error");

      setData({
        nodeCount: 0,
        edgeCount: 0,
        density: 0,
        clustering: 0,
        avgPathLength: 0,
        centrality: { nodes: [] },
        communities: [],
        pathStats: {
          avgLength: 0,
          maxLength: 0,
          distribution: {},
        },
      });
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchGraphMetrics();
  }, [fetchGraphMetrics]);

  const refresh = useCallback(() => {
    fetchGraphMetrics();
  }, [fetchGraphMetrics]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
