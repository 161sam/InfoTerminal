// Entity analytics component
import React from "react";
import { Users, TrendingUp, TrendingDown, Database, Network } from "lucide-react";
import { useEntityAnalytics } from "../../hooks/analytics";
import { AnalyticsFilters } from "./types";
import { DonutChart, TimeSeriesChart } from "../charts";

interface EntityAnalyticsProps {
  filters: AnalyticsFilters;
  className?: string;
}

export function EntityAnalytics({ filters, className = "" }: EntityAnalyticsProps) {
  const { data, loading, error } = useEntityAnalytics(filters);

  if (loading) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
          <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
          <Database size={20} />
          <span className="text-sm">Service unavailable. Showing empty state.</span>
        </div>
      </div>
    );
  }

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const getEntityTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      Person: "#3b82f6",
      Organization: "#10b981",
      Location: "#f59e0b",
      Email: "#8b5cf6",
      Domain: "#ef4444",
      Phone: "#06b6d4",
      URL: "#84cc16",
      Date: "#f97316",
      Money: "#22c55e",
      Document: "#6366f1",
    };
    return colors[type] || "#6b7280";
  };

  return (
    <div
      className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Users size={20} className="text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Entity Analytics
          </h3>
        </div>

        {data && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {formatNumber(data.totalEntities)} total entities
          </div>
        )}
      </div>

      {!data || data.totalEntities === 0 ? (
        <div className="text-center py-12">
          <Database size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            No entity data available for the selected filters.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {formatNumber(data.totalEntities)}
                  </div>
                  <div className="text-xs text-blue-600 dark:text-blue-400">Total</div>
                </div>
                <Users size={20} className="text-blue-500" />
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {formatNumber(data.newEntities)}
                  </div>
                  <div className="text-xs text-green-600 dark:text-green-400">New</div>
                </div>
                <TrendingUp size={20} className="text-green-500" />
              </div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {data.entityTypes.length}
                  </div>
                  <div className="text-xs text-purple-600 dark:text-purple-400">Types</div>
                </div>
                <Database size={20} className="text-purple-500" />
              </div>
            </div>

            <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                    {data.relationshipDensity.toFixed(2)}
                  </div>
                  <div className="text-xs text-orange-600 dark:text-orange-400">Density</div>
                </div>
                <Network size={20} className="text-orange-500" />
              </div>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Entity Types Distribution */}
            {data.entityTypes.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                  Entity Types Distribution
                </h4>
                <DonutChart
                  data={data.entityTypes.map((type) => ({
                    name: type.type,
                    value: type.count,
                    color: getEntityTypeColor(type.type),
                  }))}
                  valueKey="value"
                  nameKey="name"
                  height={200}
                  centerLabel="Total Types"
                  centerValue={data.entityTypes.length.toString()}
                />
              </div>
            )}

            {/* Trends Chart */}
            {data.trends.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                  Entity Discovery Trend
                </h4>
                <TimeSeriesChart
                  data={data.trends}
                  xKey="date"
                  yKey="count"
                  height={200}
                  showArea
                  color="#3b82f6"
                />
              </div>
            )}
          </div>

          {/* Top Entities Table */}
          {data.topEntities.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                Top Entities by Mentions
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                        Entity
                      </th>
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                        Type
                      </th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                        Mentions
                      </th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                        Sources
                      </th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                        Confidence
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.topEntities.slice(0, 10).map((entity, index) => (
                      <tr
                        key={entity.id}
                        className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50"
                      >
                        <td className="p-2">
                          <div className="font-medium text-gray-900 dark:text-gray-100">
                            {entity.name}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            Last seen: {new Date(entity.lastSeen).toLocaleDateString()}
                          </div>
                        </td>
                        <td className="p-2">
                          <span
                            className="inline-block px-2 py-1 text-xs rounded"
                            style={{
                              backgroundColor: `${getEntityTypeColor(entity.type)}20`,
                              color: getEntityTypeColor(entity.type),
                            }}
                          >
                            {entity.type}
                          </span>
                        </td>
                        <td className="p-2 text-right font-mono">
                          {formatNumber(entity.mentions)}
                        </td>
                        <td className="p-2 text-right font-mono">{entity.sources}</td>
                        <td className="p-2 text-right">
                          <span
                            className={`font-medium ${
                              entity.confidence >= 0.9
                                ? "text-green-600 dark:text-green-400"
                                : entity.confidence >= 0.7
                                  ? "text-yellow-600 dark:text-yellow-400"
                                  : "text-red-600 dark:text-red-400"
                            }`}
                          >
                            {Math.round(entity.confidence * 100)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default EntityAnalytics;
