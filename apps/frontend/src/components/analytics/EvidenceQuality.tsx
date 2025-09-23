// Evidence quality analytics component
import React from 'react';
import { Shield, CheckCircle, AlertTriangle, XCircle, TrendingUp, Users } from 'lucide-react';
import { useEvidenceQuality } from '../../hooks/analytics';
import { AnalyticsFilters } from './types';

interface EvidenceQualityProps {
  filters: AnalyticsFilters;
  className?: string;
}

export function EvidenceQuality({ filters, className = '' }: EvidenceQualityProps) {
  const { data, loading, error } = useEvidenceQuality(filters);

  if (loading) {
    return (
      <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
          <div className="h-40 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}>
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
          <Shield size={20} />
          <span className="text-sm">Evidence quality service unavailable. Showing empty state.</span>
        </div>
      </div>
    );
  }

  const getQualityStatusIcon = (status: string) => {
    switch (status) {
      case 'good': return <CheckCircle size={16} className="text-green-500" />;
      case 'warning': return <AlertTriangle size={16} className="text-yellow-500" />;
      case 'poor': return <XCircle size={16} className="text-red-500" />;
      default: return <Shield size={16} className="text-gray-500" />;
    }
  };

  const getQualityColor = (status: string) => {
    switch (status) {
      case 'good': return 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20';
      case 'warning': return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/20';
      case 'poor': return 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20';
      default: return 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-900/20';
    }
  };

  const getOverallQualityColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getReliabilityColor = (reliability: number) => {
    if (reliability >= 0.8) return 'text-green-600 dark:text-green-400';
    if (reliability >= 0.6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'low': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300';
    }
  };

  const verificationRate = data && data.totalClaims > 0 
    ? Math.round((data.verifiedClaims / data.totalClaims) * 100)
    : 0;

  return (
    <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Shield size={20} className="text-green-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Evidence Quality</h3>
        </div>
        
        {data && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {data.totalClaims} claims analyzed
          </div>
        )}
      </div>

      {!data || data.totalClaims === 0 ? (
        <div className="text-center py-12">
          <Shield size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            No evidence data available for the selected filters.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Overall Score */}
          <div className="text-center">
            <div className={`text-4xl font-bold mb-2 ${getOverallQualityColor(data.overallScore)}`}>
              {data.overallScore}/100
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Overall Evidence Quality Score</div>
            <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all ${
                  data.overallScore >= 80 ? 'bg-green-500' :
                  data.overallScore >= 60 ? 'bg-yellow-500' :
                  'bg-red-500'
                }`}
                style={{ width: `${data.overallScore}%` }}
              />
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {data.totalClaims}
                  </div>
                  <div className="text-xs text-blue-600 dark:text-blue-400">Total Claims</div>
                </div>
                <Shield size={20} className="text-blue-500" />
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {data.verifiedClaims}
                  </div>
                  <div className="text-xs text-green-600 dark:text-green-400">Verified</div>
                </div>
                <CheckCircle size={20} className="text-green-500" />
              </div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {verificationRate}%
                  </div>
                  <div className="text-xs text-purple-600 dark:text-purple-400">Verified Rate</div>
                </div>
                <TrendingUp size={20} className="text-purple-500" />
              </div>
            </div>

            <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                    {data.corroborationStats.averageSources.toFixed(1)}
                  </div>
                  <div className="text-xs text-orange-600 dark:text-orange-400">Avg Sources</div>
                </div>
                <Users size={20} className="text-orange-500" />
              </div>
            </div>
          </div>

          {/* Quality Metrics */}
          {data.qualityMetrics.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                Quality Metrics
              </h4>
              <div className="space-y-3">
                {data.qualityMetrics.map((metric, index) => (
                  <div key={index} className={`border rounded-lg p-4 ${getQualityColor(metric.status)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {getQualityStatusIcon(metric.status)}
                        <span className="font-medium text-sm">{metric.name}</span>
                      </div>
                      <span className="text-lg font-bold">{metric.score}/100</span>
                    </div>
                    
                    <div className="text-xs mb-2">{metric.description}</div>
                    
                    <div className="w-full bg-white dark:bg-gray-800 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          metric.status === 'good' ? 'bg-green-500' :
                          metric.status === 'warning' ? 'bg-yellow-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${metric.score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Corroboration Stats */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
              Corroboration Statistics
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="text-xl font-bold text-gray-900 dark:text-gray-100">
                  {data.corroborationStats.averageSources.toFixed(1)}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400">Avg Sources</div>
              </div>
              
              <div className="text-center p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="text-xl font-bold text-gray-900 dark:text-gray-100">
                  {data.corroborationStats.independentSources}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400">Independent</div>
              </div>
              
              <div className="text-center p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="text-xl font-bold text-gray-900 dark:text-gray-100">
                  {data.corroborationStats.crossReferences}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400">Cross-Refs</div>
              </div>
              
              <div className="text-center p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="text-xl font-bold text-red-600 dark:text-red-400">
                  {data.corroborationStats.conflictingClaims}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400">Conflicts</div>
              </div>
            </div>
          </div>

          {/* Source Reliability */}
          {data.sourceReliability.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                Source Reliability
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">Source</th>
                      <th className="text-left p-2 font-medium text-gray-900 dark:text-gray-100">Category</th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">Claims</th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">Verified</th>
                      <th className="text-right p-2 font-medium text-gray-900 dark:text-gray-100">Reliability</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.sourceReliability.slice(0, 8).map((source, index) => (
                      <tr key={index} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50">
                        <td className="p-2 font-medium text-gray-900 dark:text-gray-100">
                          {source.source}
                        </td>
                        <td className="p-2">
                          <span className="inline-block px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded">
                            {source.category}
                          </span>
                        </td>
                        <td className="p-2 text-right font-mono">
                          {source.claimsCount}
                        </td>
                        <td className="p-2 text-right font-mono">
                          {Math.round(source.verificationRate * 100)}%
                        </td>
                        <td className="p-2 text-right">
                          <span className={`font-medium ${getReliabilityColor(source.reliability)}`}>
                            {Math.round(source.reliability * 100)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Recommendations */}
          {data.recommendations.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
                Quality Recommendations
              </h4>
              <div className="space-y-3">
                {data.recommendations.map((rec, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
                    <div className="flex items-start gap-3">
                      <span className={`inline-block px-2 py-1 text-xs rounded font-medium ${getPriorityColor(rec.priority)}`}>
                        {rec.priority.toUpperCase()}
                      </span>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-1">
                          {rec.type}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          {rec.message}
                        </div>
                        {rec.action && (
                          <div className="text-xs text-blue-600 dark:text-blue-400 mt-2">
                            Action: {rec.action}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default EvidenceQuality;
