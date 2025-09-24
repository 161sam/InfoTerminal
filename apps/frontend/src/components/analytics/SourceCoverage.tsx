// Source coverage analytics component
import React from "react";
import { Globe, Database, CheckCircle, AlertTriangle, TrendingUp } from "lucide-react";
import { useSourceCoverage } from "../../hooks/analytics";
import { AnalyticsFilters } from "./types";
import { DonutChart, MultiSeriesChart } from "../charts";

interface SourceCoverageProps {
  filters: AnalyticsFilters;
  className?: string;
}

export function SourceCoverage({ filters, className = "" }: SourceCoverageProps) {
  const { data, loading, error } = useSourceCoverage(filters);

  if (loading) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
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

  const getSourceTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      Web: "#3b82f6",
      Document: "#10b981",
      Social: "#f59e0b",
      News: "#ef4444",
      Academic: "#8b5cf6",
      Government: "#06b6d4",
      Database: "#84cc16",
      API: "#f97316",
    };
    return colors[type] || "#6b7280";
  };

  const getCoverageStatusColor = (status: string) => {
    switch (status) {
      case "good":
        return "text-green-600 dark:text-green-400";
      case "warning":
        return "text-yellow-600 dark:text-yellow-400";
      case "critical":
        return "text-red-600 dark:text-red-400";
      default:
        return "text-gray-600 dark:text-gray-400";
    }
  };

  const getCoverageIcon = (status: string) => {
    switch (status) {
      case "good":
        return <CheckCircle size={16} className="text-green-500" />;
      case "warning":
        return <AlertTriangle size={16} className="text-yellow-500" />;
      case "critical":
        return <AlertTriangle size={16} className="text-red-500" />;
      default:
        return <Database size={16} className="text-gray-500" />;
    }
  };

  return (
    <div
      className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Globe size={20} className="text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Source Coverage
          </h3>
        </div>

        {data && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {formatNumber(data.totalSources)} sources ({data.activeSources} active)
          </div>
        )}
      </div>

      {!data || data.totalSources === 0 ? (
        <div className="text-center py-12">
          <Globe size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            No source data available for the selected filters.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {formatNumber(data.totalSources)}
                  </div>
                  <div className="text-xs text-blue-600 dark:text-blue-400">Total Sources</div>
                </div>
                <Globe size={20} className="text-blue-500" />
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {formatNumber(data.activeSources)}
                  </div>
                  <div className="text-xs text-green-600 dark:text-green-400">Active</div>
                </div>
                <CheckCircle size={20} className="text-green-500" />
              </div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {data.sourceTypes.length}
                  </div>
                  <div className="text-xs text-purple-600 dark:text-purple-400">Types</div>
                </div>
                <Database size={20} className="text-purple-500" />
              </div>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Source Types Distribution */}
            {data.sourceTypes.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                  Source Types Distribution
                </h4>
                <DonutChart
                  data={data.sourceTypes.map((type) => ({
                    name: type.type,
                    value: type.count,
                    color: getSourceTypeColor(type.type),
                  }))}
                  valueKey="value"
                  nameKey="name"
                  height={200}
                  centerLabel="Total Types"
                  centerValue={data.sourceTypes.length.toString()}
                />
              </div>
            )}

            {/* Timeline Chart */}
            {data.timeline.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                  Source Activity Timeline
                </h4>
                <MultiSeriesChart
                  data={data.timeline}
                  xKey="date"
                  series={[
                    { key: "sources", name: "Active Sources", color: "#3b82f6", type: "line" },
                    { key: "newSources", name: "New Sources", color: "#10b981", type: "bar" },
                  ]}
                  height={200}
                  showLegend
                />
              </div>
            )}
          </div>

          {/* Coverage Metrics */}
          {data.coverage.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                Coverage Metrics
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {data.coverage.map((metric, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {metric.category}
                      </span>
                      {getCoverageIcon(metric.status)}
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-600 dark:text-gray-400">Coverage</span>
                        <span className={getCoverageStatusColor(metric.status)}>
                          {metric.coverage}% / {metric.target}%
                        </span>
                      </div>

                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all ${
                            metric.status === "good"
                              ? "bg-green-500"
                              : metric.status === "warning"
                                ? "bg-yellow-500"
                                : "bg-red-500"
                          }`}
                          style={{
                            width: `${Math.min((metric.coverage / metric.target) * 100, 100)}%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Top Sources Table */}
          {data.topSources.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                Top Sources by Document Count
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                        Source
                      </th>
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                        Type
                      </th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                        Documents
                      </th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                        Reliability
                      </th>
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                        Last Updated
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.topSources.slice(0, 10).map((source, index) => (
                      <tr
                        key={source.id}
                        className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50"
                      >
                        <td className="p-2">
                          <div className="font-medium text-gray-900 dark:text-gray-100">
                            {source.name}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            {source.domain}
                          </div>
                        </td>
                        <td className="p-2">
                          <span
                            className="inline-block px-2 py-1 text-xs rounded"
                            style={{
                              backgroundColor: `${getSourceTypeColor(source.type)}20`,
                              color: getSourceTypeColor(source.type),
                            }}
                          >
                            {source.type}
                          </span>
                        </td>
                        <td className="p-2 text-right font-mono">
                          {formatNumber(source.documents)}
                        </td>
                        <td className="p-2 text-right">
                          <span
                            className={`font-medium ${
                              source.reliability >= 0.8
                                ? "text-green-600 dark:text-green-400"
                                : source.reliability >= 0.6
                                  ? "text-yellow-600 dark:text-yellow-400"
                                  : "text-red-600 dark:text-red-400"
                            }`}
                          >
                            {Math.round(source.reliability * 100)}%
                          </span>
                        </td>
                        <td className="p-2 text-xs text-gray-600 dark:text-gray-400">
                          {new Date(source.lastUpdated).toLocaleDateString()}
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

export default SourceCoverage;
