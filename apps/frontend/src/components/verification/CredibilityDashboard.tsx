"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Shield, 
  ExternalLink,
  AlertTriangle,
  CheckCircle,
  Star,
  TrendingUp,
  TrendingDown,
  Eye,
  Globe
} from 'lucide-react';

interface CredibilityData {
  credibility_score: number;
  bias_rating: string;
  factual_reporting: string;
  transparency_score: number;
  authority_indicators: string[];
  red_flags: string[];
}

interface CredibilityDashboardProps {
  sourceUrl?: string;
  className?: string;
}

export function CredibilityDashboard({ sourceUrl, className }: CredibilityDashboardProps) {
  const [credibilityData, setCredibilityData] = useState<CredibilityData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputUrl, setInputUrl] = useState(sourceUrl || '');

  useEffect(() => {
    if (sourceUrl && sourceUrl !== inputUrl) {
      setInputUrl(sourceUrl);
      handleAssessCredibility(sourceUrl);
    }
  }, [sourceUrl]);

  const handleAssessCredibility = async (url: string = inputUrl) => {
    if (!url.trim()) {
      setError('Please enter a URL to assess');
      return;
    }

    // Basic URL validation
    try {
      new URL(url);
    } catch {
      setError('Please enter a valid URL');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/verification/credibility?url=${encodeURIComponent(url)}`);
      
      if (!response.ok) {
        throw new Error('Failed to assess credibility');
      }

      const data = await response.json();
      setCredibilityData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getBiasIcon = (bias: string) => {
    switch (bias.toLowerCase()) {
      case 'left': return <TrendingDown className="h-4 w-4 text-blue-500" />;
      case 'right': return <TrendingUp className="h-4 w-4 text-red-500" />;
      case 'center': return <Eye className="h-4 w-4 text-green-500" />;
      default: return <Globe className="h-4 w-4 text-gray-500" />;
    }
  };

  const getBiasColor = (bias: string) => {
    switch (bias.toLowerCase()) {
      case 'left': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'right': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'center': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getFactualColor = (factual: string) => {
    switch (factual.toLowerCase()) {
      case 'high': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'low': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getCredibilityLevel = (score: number) => {
    if (score >= 0.8) return { level: 'Very High', color: 'text-green-600', bgColor: 'bg-green-50 dark:bg-green-900/20' };
    if (score >= 0.6) return { level: 'High', color: 'text-green-600', bgColor: 'bg-green-50 dark:bg-green-900/20' };
    if (score >= 0.4) return { level: 'Medium', color: 'text-yellow-600', bgColor: 'bg-yellow-50 dark:bg-yellow-900/20' };
    if (score >= 0.2) return { level: 'Low', color: 'text-red-600', bgColor: 'bg-red-50 dark:bg-red-900/20' };
    return { level: 'Very Low', color: 'text-red-600', bgColor: 'bg-red-50 dark:bg-red-900/20' };
  };

  const getOverallRating = (data: CredibilityData) => {
    const avgScore = (data.credibility_score + data.transparency_score) / 2;
    return getCredibilityLevel(avgScore);
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          <CardTitle>Source Credibility Assessment</CardTitle>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* URL Input */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Source URL</label>
          <div className="flex gap-2">
            <input
              type="url"
              value={inputUrl}
              onChange={(e) => setInputUrl(e.target.value)}
              placeholder="https://example.com/article"
              className="flex-1 p-2 border rounded"
            />
            <button
              onClick={() => handleAssessCredibility()}
              disabled={isLoading || !inputUrl.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? 'Analyzing...' : 'Assess'}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900/30 rounded-lg">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-red-600" />
              <span className="text-sm text-red-800 dark:text-red-300">{error}</span>
            </div>
          </div>
        )}

        {/* Results */}
        {credibilityData && (
          <div className="space-y-6">
            {/* Overall Rating */}
            <div className={`p-4 rounded-lg ${getOverallRating(credibilityData).bgColor}`}>
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium">Overall Credibility Rating</h3>
                <Badge className={`${getOverallRating(credibilityData).color}`}>
                  {getOverallRating(credibilityData).level}
                </Badge>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Shield className="h-4 w-4" />
                    <span className="text-sm font-medium">Credibility Score</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Progress value={credibilityData.credibility_score * 100} className="flex-1 h-2" />
                    <span className="text-sm font-medium">
                      {(credibilityData.credibility_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Eye className="h-4 w-4" />
                    <span className="text-sm font-medium">Transparency Score</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Progress value={credibilityData.transparency_score * 100} className="flex-1 h-2" />
                    <span className="text-sm font-medium">
                      {(credibilityData.transparency_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Bias and Factual Reporting */}
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    {getBiasIcon(credibilityData.bias_rating)}
                    <span className="font-medium">Political Bias</span>
                  </div>
                  <Badge className={getBiasColor(credibilityData.bias_rating)}>
                    {credibilityData.bias_rating.charAt(0).toUpperCase() + credibilityData.bias_rating.slice(1)}
                  </Badge>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="h-4 w-4" />
                    <span className="font-medium">Factual Reporting</span>
                  </div>
                  <Badge className={getFactualColor(credibilityData.factual_reporting)}>
                    {credibilityData.factual_reporting.charAt(0).toUpperCase() + credibilityData.factual_reporting.slice(1)}
                  </Badge>
                </CardContent>
              </Card>
            </div>

            {/* Authority Indicators */}
            {credibilityData.authority_indicators.length > 0 && (
              <div>
                <h4 className="font-medium mb-2 flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Authority Indicators
                </h4>
                <div className="space-y-2">
                  {credibilityData.authority_indicators.map((indicator, index) => (
                    <div key={index} className="flex items-center gap-2 p-2 bg-green-50 dark:bg-green-900/20 rounded">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className="text-sm">{indicator}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Red Flags */}
            {credibilityData.red_flags.length > 0 && (
              <div>
                <h4 className="font-medium mb-2 flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                  Red Flags
                </h4>
                <div className="space-y-2">
                  {credibilityData.red_flags.map((flag, index) => (
                    <div key={index} className="flex items-center gap-2 p-2 bg-red-50 dark:bg-red-900/20 rounded">
                      <AlertTriangle className="h-4 w-4 text-red-500" />
                      <span className="text-sm">{flag}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Credibility Guide */}
            <div className="p-3 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
              <h4 className="text-sm font-medium mb-2">Credibility Assessment Guide</h4>
              <div className="grid grid-cols-1 gap-2 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full" />
                  <span><strong>80-100%:</strong> Highly credible, well-established source</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                  <span><strong>40-79%:</strong> Moderately credible, verify with other sources</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full" />
                  <span><strong>0-39%:</strong> Low credibility, use with extreme caution</span>
                </div>
              </div>
            </div>

            {/* Source Link */}
            {inputUrl && (
              <div className="flex items-center gap-2 p-3 border rounded-lg">
                <ExternalLink className="h-4 w-4" />
                <span className="text-sm font-medium">Source:</span>
                <a
                  href={inputUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 text-sm truncate flex-1"
                >
                  {inputUrl}
                </a>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
