// Query insights analytics component
import React, { useState } from "react";
import { Search, TrendingUp, BarChart3, Clock, MousePointer } from "lucide-react";
import { useQueryInsights } from "../../hooks/analytics";
import { AnalyticsFilters } from "./types";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface QueryInsightsProps {
  filters: AnalyticsFilters;
  className?: string;
}

export function QueryInsights({ filters, className = "" }: QueryInsightsProps) {
  const { data, loading, error } = useQueryInsights(filters);
  const [selectedTab, setSelectedTab] = useState<"queries" | "patterns" | "performance">("queries");

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
          <Search size={20} />
          <span className="text-sm">
            Query insights service unavailable. Feature may not be enabled.
          </span>
        </div>
      </div>
    );
  }

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const getEffectivenessColor = (effectiveness: number) => {
    if (effectiveness >= 0.8) return "text-green-600 dark:text-green-400";
    if (effectiveness >= 0.6) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getPatternCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      entity: "#3b82f6",
      temporal: "#10b981",
      location: "#f59e0b",
      boolean: "#8b5cf6",
      wildcard: "#ef4444",
      phrase: "#06b6d4",
    };
    return colors[category] || "#6b7280";
  };

  return (
    <div
      className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Search size={20} className="text-green-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Query Insights</h3>
        </div>

        {data && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {formatNumber(data.totalQueries)} queries • {formatNumber(data.uniqueQueries)} unique
          </div>
        )}
      </div>

      {!data || data.totalQueries === 0 ? (
        <div className="text-center py-12">
          <Search size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            Query tracking may not be enabled or no data available for the selected period.
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
                    {formatNumber(data.totalQueries)}
                  </div>
                  <div className="text-xs text-blue-600 dark:text-blue-400">Total Queries</div>
                </div>
                <Search size={20} className="text-blue-500" />
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {formatNumber(data.uniqueQueries)}
                  </div>
                  <div className="text-xs text-green-600 dark:text-green-400">Unique</div>
                </div>
                <TrendingUp size={20} className="text-green-500" />
              </div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {Math.round(data.clickthrough.averageRate * 100)}%
                  </div>
                  <div className="text-xs text-purple-600 dark:text-purple-400">CTR</div>
                </div>
                <MousePointer size={20} className="text-purple-500" />
              </div>
            </div>

            <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                    {data.performance.averageResponseTime}ms
                  </div>
                  <div className="text-xs text-orange-600 dark:text-orange-400">Avg Time</div>
                </div>
                <Clock size={20} className="text-orange-500" />
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex space-x-8">
              {[
                { id: "queries", label: "Top Queries", icon: Search },
                { id: "patterns", label: "Search Patterns", icon: BarChart3 },
                { id: "performance", label: "Performance", icon: Clock },
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setSelectedTab(tab.id as any)}
                    className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm ${
                      selectedTab === tab.id
                        ? "border-green-500 text-green-600 dark:text-green-400"
                        : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    <Icon size={16} />
                    {tab.label}
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div>
            {selectedTab === "queries" && (
              <div className="space-y-6">
                {/* Top Queries Chart */}
                {data.topQueries.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                      Most Popular Queries
                    </h4>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={data.topQueries.slice(0, 10)}
                          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                          <XAxis
                            dataKey="query"
                            angle={-45}
                            textAnchor="end"
                            height={80}
                            interval={0}
                            className="text-xs"
                          />
                          <YAxis className="text-xs" />
                          <Tooltip
                            formatter={(value, name) => [value, "Query Count"]}
                            labelFormatter={(query) => `Query: ${query}`}
                          />
                          <Bar dataKey="count" fill="#22c55e" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}

                {/* Top Queries Table */}
                {data.topQueries.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                      Query Details
                    </h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-gray-200 dark:border-gray-700">
                            <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                              Query
                            </th>
                            <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                              Count
                            </th>
                            <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                              Avg Results
                            </th>
                            <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                              CTR
                            </th>
                            <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                              Last Used
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {data.topQueries.slice(0, 15).map((query, index) => (
                            <tr
                              key={index}
                              className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50"
                            >
                              <td className="p-2 max-w-xs">
                                <div className="font-medium text-gray-900 dark:text-gray-100 truncate">
                                  {query.query}
                                </div>
                              </td>
                              <td className="p-2 text-right font-mono">{query.count}</td>
                              <td className="p-2 text-right font-mono">{query.averageResults}</td>
                              <td className="p-2 text-right">
                                <span
                                  className={`font-medium ${
                                    query.clickthrough >= 0.5
                                      ? "text-green-600 dark:text-green-400"
                                      : query.clickthrough >= 0.2
                                        ? "text-yellow-600 dark:text-yellow-400"
                                        : "text-red-600 dark:text-red-400"
                                  }`}
                                >
                                  {Math.round(query.clickthrough * 100)}%
                                </span>
                              </td>
                              <td className="p-2 text-xs text-gray-600 dark:text-gray-400">
                                {new Date(query.lastUsed).toLocaleDateString()}
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

            {selectedTab === "patterns" && (
              <div className="space-y-6">
                {/* Search Patterns */}
                {data.searchPatterns.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                      Search Pattern Categories
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {data.searchPatterns.map((pattern, index) => (
                        <div
                          key={index}
                          className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              <div
                                className="w-3 h-3 rounded"
                                style={{
                                  backgroundColor: getPatternCategoryColor(pattern.category),
                                }}
                              />
                              <span className="text-sm font-medium text-gray-900 dark:text-gray-100 capitalize">
                                {pattern.category}
                              </span>
                            </div>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {pattern.frequency} uses
                            </span>
                          </div>

                          <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                            {pattern.pattern}
                          </div>

                          <div className="flex items-center justify-between">
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              Effectiveness:
                            </span>
                            <span
                              className={`text-xs font-medium ${getEffectivenessColor(pattern.effectiveness)}`}
                            >
                              {Math.round(pattern.effectiveness * 100)}%
                            </span>
                          </div>

                          <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                            <div
                              className="h-1 rounded-full transition-all"
                              style={{
                                backgroundColor: getPatternCategoryColor(pattern.category),
                                width: `${pattern.effectiveness * 100}%`,
                              }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Clickthrough Stats */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                    Document Type Preferences
                  </h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(data.clickthrough.documentTypes).map(([type, count]) => (
                      <div
                        key={type}
                        className="text-center p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg"
                      >
                        <div className="text-lg font-bold text-gray-900 dark:text-gray-100">
                          {count}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400 capitalize">
                          {type}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {selectedTab === "performance" && (
              <div className="space-y-6">
                {/* Performance Stats */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                      {data.performance.averageResponseTime}ms
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Average Response</div>
                  </div>

                  <div className="text-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                      {Math.round(data.performance.errorRate * 100)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Error Rate</div>
                  </div>

                  <div className="text-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                      {data.performance.slowQueries.length}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Slow Queries</div>
                  </div>
                </div>

                {/* Slow Queries */}
                {data.performance.slowQueries.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                      Slowest Queries
                    </h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-gray-200 dark:border-gray-700">
                            <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                              Query
                            </th>
                            <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                              Response Time
                            </th>
                            <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">
                              Timestamp
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {data.performance.slowQueries.slice(0, 10).map((slowQuery, index) => (
                            <tr
                              key={index}
                              className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50"
                            >
                              <td className="p-2 max-w-xs">
                                <div className="font-medium text-gray-900 dark:text-gray-100 truncate">
                                  {slowQuery.query}
                                </div>
                              </td>
                              <td className="p-2 text-right">
                                <span
                                  className={`font-mono ${
                                    slowQuery.responseTime > 5000
                                      ? "text-red-600 dark:text-red-400"
                                      : slowQuery.responseTime > 2000
                                        ? "text-yellow-600 dark:text-yellow-400"
                                        : "text-gray-900 dark:text-gray-100"
                                  }`}
                                >
                                  {slowQuery.responseTime}ms
                                </span>
                              </td>
                              <td className="p-2 text-xs text-gray-600 dark:text-gray-400">
                                {new Date(slowQuery.timestamp).toLocaleString()}
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
        </div>
      )}
    </div>
  );
}

export default QueryInsights;
