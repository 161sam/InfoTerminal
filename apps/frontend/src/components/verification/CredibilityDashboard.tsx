"use client";

import React, { useState, useEffect } from "react";
import Panel from "@/components/layout/Panel";
import { LoadingSpinner } from "@/components/ui/loading";
import {
  inputStyles,
  buttonStyles,
  textStyles,
  cardStyles,
  statusStyles,
  compose,
} from "@/styles/design-tokens";
import {
  Shield,
  ExternalLink,
  AlertTriangle,
  CheckCircle,
  Star,
  TrendingUp,
  TrendingDown,
  Eye,
  Globe,
} from "lucide-react";

interface CredibilityData {
  credibility_score: number;
  bias_rating: string;
  factual_reporting: string;
  transparency_score: number;
  authority_indicators: string[];
  red_flags: string[];
}

interface PerformanceMetrics {
  response_time_ms: number;
  cache_hit: boolean;
  timestamp: number;
}

interface AnalyticsData {
  assessment_count: number;
  average_response_time: number;
  cache_hit_rate: number;
  recent_assessments: Array<{
    url: string;
    credibility_score: number;
    timestamp: number;
  }>;
}

interface CredibilityDashboardProps {
  sourceUrl?: string;
  className?: string;
  showAnalytics?: boolean;
}

export function CredibilityDashboard({
  sourceUrl,
  className,
  showAnalytics = false,
}: CredibilityDashboardProps) {
  const [credibilityData, setCredibilityData] = useState<CredibilityData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputUrl, setInputUrl] = useState(sourceUrl || "");

  // Analytics state (v0.3.0+)
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics | null>(null);
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [showPerformancePanel, setShowPerformancePanel] = useState(false);

  const handleAssessCredibility = React.useCallback(async (url: string = inputUrl) => {
    if (!url.trim()) {
      setError("Please enter a URL to assess");
      return;
    }

    // Basic URL validation
    try {
      new URL(url);
    } catch {
      setError("Please enter a valid URL");
      return;
    }

    setIsLoading(true);
    setError(null);

    // Performance tracking (v0.3.0+)
    const startTime = performance.now();

    try {
      const response = await fetch(`/api/verification/credibility?url=${encodeURIComponent(url)}`);

      if (!response.ok) {
        throw new Error("Failed to assess credibility");
      }

      const data = await response.json();
      const endTime = performance.now();
      const responseTime = endTime - startTime;

      setCredibilityData(data);

      // Update performance metrics
      const metrics: PerformanceMetrics = {
        response_time_ms: responseTime,
        cache_hit: response.headers.get("x-cache-status") === "hit",
        timestamp: Date.now(),
      };
      setPerformanceMetrics(metrics);

      // Update analytics if enabled
      if (showAnalytics) {
        await updateAnalytics(url, data.credibility_score, metrics);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  }, [inputUrl, showAnalytics]);

  useEffect(() => {
    if (sourceUrl && sourceUrl !== inputUrl) {
      setInputUrl(sourceUrl);
      handleAssessCredibility(sourceUrl);
    }
  }, [sourceUrl, inputUrl, handleAssessCredibility]);

  // Analytics functions (v0.3.0+)
  const updateAnalytics = async (
    url: string,
    credibilityScore: number,
    metrics: PerformanceMetrics,
  ) => {
    try {
      // Store assessment in local analytics
      const stored = localStorage.getItem("credibility-analytics") || "{}";
      const analytics = JSON.parse(stored) as Partial<AnalyticsData>;

      analytics.assessment_count = (analytics.assessment_count || 0) + 1;
      analytics.recent_assessments = analytics.recent_assessments || [];

      // Add new assessment
      analytics.recent_assessments.unshift({
        url: url,
        credibility_score: credibilityScore,
        timestamp: Date.now(),
      });

      // Keep only last 50 assessments
      analytics.recent_assessments = analytics.recent_assessments.slice(0, 50);

      // Update performance stats
      const responseTimes = analytics.recent_assessments.map(() => metrics.response_time_ms);
      analytics.average_response_time =
        responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;

      // Calculate cache hit rate (simplified)
      analytics.cache_hit_rate = 0.8; // This would be calculated from actual metrics

      localStorage.setItem("credibility-analytics", JSON.stringify(analytics));
      setAnalyticsData(analytics as AnalyticsData);
    } catch (err) {
      console.warn("Failed to update analytics:", err);
    }
  };

  // Load analytics on component mount
  useEffect(() => {
    if (showAnalytics) {
      const stored = localStorage.getItem("credibility-analytics");
      if (stored) {
        try {
          setAnalyticsData(JSON.parse(stored));
        } catch (err) {
          console.warn("Failed to load analytics:", err);
        }
      }
    }
  }, [showAnalytics]);

  const getBiasIcon = (bias: string) => {
    switch (bias.toLowerCase()) {
      case "left":
        return <TrendingDown className="h-4 w-4 text-blue-500" />;
      case "right":
        return <TrendingUp className="h-4 w-4 text-red-500" />;
      case "center":
        return <Eye className="h-4 w-4 text-green-500" />;
      default:
        return <Globe className="h-4 w-4 text-gray-500" />;
    }
  };

  const getBiasColor = (bias: string) => {
    switch (bias.toLowerCase()) {
      case "left":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
      case "right":
        return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
      case "center":
        return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
    }
  };

  const getFactualColor = (factual: string) => {
    switch (factual.toLowerCase()) {
      case "high":
        return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
      case "medium":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300";
      case "low":
        return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
    }
  };

  const getCredibilityLevel = (score: number) => {
    if (score >= 0.8)
      return {
        level: "Very High",
        color: "text-green-600",
        bgColor: "bg-green-50 dark:bg-green-900/20",
      };
    if (score >= 0.6)
      return {
        level: "High",
        color: "text-green-600",
        bgColor: "bg-green-50 dark:bg-green-900/20",
      };
    if (score >= 0.4)
      return {
        level: "Medium",
        color: "text-yellow-600",
        bgColor: "bg-yellow-50 dark:bg-yellow-900/20",
      };
    if (score >= 0.2)
      return { level: "Low", color: "text-red-600", bgColor: "bg-red-50 dark:bg-red-900/20" };
    return { level: "Very Low", color: "text-red-600", bgColor: "bg-red-50 dark:bg-red-900/20" };
  };

  const getOverallRating = (data: CredibilityData) => {
    const avgScore = (data.credibility_score + data.transparency_score) / 2;
    return getCredibilityLevel(avgScore);
  };

  return (
    <Panel title="Source Credibility Assessment" className={className}>
      <div className="space-y-6">
        {/* URL Input */}
        <div className="space-y-2">
          <label className={`${textStyles.body} font-medium`}>Source URL</label>
          <div className="flex gap-2">
            <input
              type="url"
              value={inputUrl}
              onChange={(e) => setInputUrl(e.target.value)}
              placeholder="https://example.com/article"
              className={`${inputStyles.base} flex-1`}
            />
            <button
              onClick={() => handleAssessCredibility()}
              disabled={isLoading || !inputUrl.trim()}
              className={compose.button(
                "primary",
                isLoading || !inputUrl.trim() ? "opacity-50 cursor-not-allowed" : "",
              )}
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" variant="primary" layout="inline" />
                  Analyzing...
                </>
              ) : (
                "Assess"
              )}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div
            className={`${cardStyles.base} ${cardStyles.padding} ${statusStyles.error} border-red-200 dark:border-red-800`}
          >
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              <span className={textStyles.body}>{error}</span>
            </div>
          </div>
        )}

        {/* Results */}
        {credibilityData && (
          <div className="space-y-6">
            {/* Overall Rating */}
            <div
              className={`${cardStyles.base} ${cardStyles.padding} ${getOverallRating(credibilityData).bgColor}`}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className={`${textStyles.body} font-medium`}>Overall Credibility Rating</h3>
                <span
                  className={`${getOverallRating(credibilityData).color} ${statusStyles.info} px-3 py-1 rounded-full text-sm font-medium`}
                >
                  {getOverallRating(credibilityData).level}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Shield className="h-4 w-4" />
                    <span className={`${textStyles.body} font-medium`}>Credibility Score</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${credibilityData.credibility_score * 100}%` }}
                      />
                    </div>
                    <span className={`${textStyles.body} font-medium`}>
                      {(credibilityData.credibility_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Eye className="h-4 w-4" />
                    <span className={`${textStyles.body} font-medium`}>Transparency Score</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-green-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${credibilityData.transparency_score * 100}%` }}
                      />
                    </div>
                    <span className={`${textStyles.body} font-medium`}>
                      {(credibilityData.transparency_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Bias and Factual Reporting */}
            <div className="grid grid-cols-2 gap-4">
              <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                <div className="flex items-center gap-2 mb-2">
                  {getBiasIcon(credibilityData.bias_rating)}
                  <span className={`${textStyles.body} font-medium`}>Political Bias</span>
                </div>
                <span
                  className={`${getBiasColor(credibilityData.bias_rating)} px-2 py-1 rounded text-sm font-medium`}
                >
                  {credibilityData.bias_rating.charAt(0).toUpperCase() +
                    credibilityData.bias_rating.slice(1)}
                </span>
              </div>

              <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="h-4 w-4" />
                  <span className={`${textStyles.body} font-medium`}>Factual Reporting</span>
                </div>
                <span
                  className={`${getFactualColor(credibilityData.factual_reporting)} px-2 py-1 rounded text-sm font-medium`}
                >
                  {credibilityData.factual_reporting.charAt(0).toUpperCase() +
                    credibilityData.factual_reporting.slice(1)}
                </span>
              </div>
            </div>

            {/* Authority Indicators */}
            {credibilityData.authority_indicators.length > 0 && (
              <div>
                <h4 className={`${textStyles.body} font-medium mb-2 flex items-center gap-2`}>
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Authority Indicators
                </h4>
                <div className="space-y-2">
                  {credibilityData.authority_indicators.map((indicator, index) => (
                    <div
                      key={index}
                      className={`flex items-center gap-2 ${cardStyles.base} p-2 ${statusStyles.success} border-green-200 dark:border-green-800`}
                    >
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className={textStyles.body}>{indicator}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Red Flags */}
            {credibilityData.red_flags.length > 0 && (
              <div>
                <h4 className={`${textStyles.body} font-medium mb-2 flex items-center gap-2`}>
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                  Red Flags
                </h4>
                <div className="space-y-2">
                  {credibilityData.red_flags.map((flag, index) => (
                    <div
                      key={index}
                      className={`flex items-center gap-2 ${cardStyles.base} p-2 ${statusStyles.error} border-red-200 dark:border-red-800`}
                    >
                      <AlertTriangle className="h-4 w-4 text-red-500" />
                      <span className={textStyles.body}>{flag}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Credibility Guide */}
            <div className={`${cardStyles.base} p-3 bg-gray-50 dark:bg-gray-900/20`}>
              <h4 className={`${textStyles.body} font-medium mb-2`}>
                Credibility Assessment Guide
              </h4>
              <div className="grid grid-cols-1 gap-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full" />
                  <span className={textStyles.bodySmall}>
                    <strong>80-100%:</strong> Highly credible, well-established source
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                  <span className={textStyles.bodySmall}>
                    <strong>40-79%:</strong> Moderately credible, verify with other sources
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full" />
                  <span className={textStyles.bodySmall}>
                    <strong>0-39%:</strong> Low credibility, use with extreme caution
                  </span>
                </div>
              </div>
            </div>

            {/* Source Link */}
            {inputUrl && (
              <div className={`flex items-center gap-2 ${cardStyles.base} ${cardStyles.padding}`}>
                <ExternalLink className="h-4 w-4" />
                <span className={`${textStyles.body} font-medium`}>Source:</span>
                <a
                  href={inputUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`${textStyles.link} truncate flex-1`}
                >
                  {inputUrl}
                </a>
              </div>
            )}

            {/* Performance Metrics Panel (v0.3.0+) */}
            {performanceMetrics && (
              <div className={`${cardStyles.base} p-3 bg-gray-50 dark:bg-gray-900/20`}>
                <div className="flex items-center justify-between mb-2">
                  <h4 className={`${textStyles.body} font-medium`}>Performance Metrics</h4>
                  <button
                    onClick={() => setShowPerformancePanel(!showPerformancePanel)}
                    className={`${textStyles.link} text-sm`}
                  >
                    {showPerformancePanel ? "Hide" : "Show"} Details
                  </button>
                </div>

                <div className={`grid grid-cols-3 gap-2 ${textStyles.bodySmall}`}>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full" />
                    <span>Response: {performanceMetrics.response_time_ms.toFixed(0)}ms</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div
                      className={`w-2 h-2 rounded-full ${performanceMetrics.cache_hit ? "bg-green-500" : "bg-gray-400"}`}
                    />
                    <span>{performanceMetrics.cache_hit ? "Cache Hit" : "Cache Miss"}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-purple-500 rounded-full" />
                    <span>{new Date(performanceMetrics.timestamp).toLocaleTimeString()}</span>
                  </div>
                </div>

                {showPerformancePanel && (
                  <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
                    <div className={textStyles.bodySmall}>
                      <div>
                        Cache Status:{" "}
                        {performanceMetrics.cache_hit
                          ? "Hit (data served from cache)"
                          : "Miss (fresh data retrieved)"}
                      </div>
                      <div>
                        Response Speed:{" "}
                        {performanceMetrics.response_time_ms < 500
                          ? "Fast"
                          : performanceMetrics.response_time_ms < 1000
                            ? "Normal"
                            : "Slow"}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Analytics Panel (v0.3.0+) */}
            {showAnalytics && analyticsData && (
              <div className={`${cardStyles.base} p-3 bg-blue-50 dark:bg-blue-900/20`}>
                <h4 className={`${textStyles.body} font-medium mb-2`}>Assessment Analytics</h4>

                <div className="grid grid-cols-3 gap-4 mb-3">
                  <div className="text-center">
                    <div className="text-lg font-bold text-blue-600">
                      {analyticsData.assessment_count}
                    </div>
                    <div className={textStyles.bodySmall}>Total Assessments</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-green-600">
                      {analyticsData.average_response_time.toFixed(0)}ms
                    </div>
                    <div className={textStyles.bodySmall}>Avg Response</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-purple-600">
                      {(analyticsData.cache_hit_rate * 100).toFixed(0)}%
                    </div>
                    <div className={textStyles.bodySmall}>Cache Hit Rate</div>
                  </div>
                </div>

                {analyticsData.recent_assessments &&
                  analyticsData.recent_assessments.length > 0 && (
                    <div>
                      <h5 className={`${textStyles.bodySmall} font-medium mb-1`}>
                        Recent Assessments
                      </h5>
                      <div className="space-y-1 max-h-32 overflow-y-auto">
                        {analyticsData.recent_assessments.slice(0, 5).map((assessment, index) => (
                          <div
                            key={index}
                            className={`flex items-center justify-between ${textStyles.bodySmall}`}
                          >
                            <span className="truncate flex-1 pr-2">{assessment.url}</span>
                            <span
                              className={`font-medium ${
                                assessment.credibility_score >= 0.7
                                  ? "text-green-600"
                                  : assessment.credibility_score >= 0.4
                                    ? "text-yellow-600"
                                    : "text-red-600"
                              }`}
                            >
                              {(assessment.credibility_score * 100).toFixed(0)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
              </div>
            )}
          </div>
        )}
      </div>
    </Panel>
  );
}
