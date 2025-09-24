// Hook for workflow runs data
import { useState, useEffect, useCallback } from "react";
import { analyticsApi } from "../../lib/api-client";
import { WorkflowRun, AnalyticsFilters } from "../analytics/types";

export function useWorkflowRuns(filters: AnalyticsFilters) {
  const [data, setData] = useState<WorkflowRun[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWorkflowRuns = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await analyticsApi.getWorkflowRuns({
        limit: 50,
        status: filters.workflows?.length ? undefined : "all",
        ...filters,
      });

      if (response.success && response.data) {
        setData(response.data.runs || response.data || []);
      } else {
        // Fallback to empty state if service unavailable
        setData([]);

        if (response.error) {
          console.warn("Workflow runs service unavailable:", response.error);
        }
      }
    } catch (err) {
      console.warn("Error fetching workflow runs:", err);
      setError(err instanceof Error ? err.message : "Unknown error");
      setData([]);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchWorkflowRuns();
  }, [fetchWorkflowRuns]);

  const refresh = useCallback(() => {
    fetchWorkflowRuns();
  }, [fetchWorkflowRuns]);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
