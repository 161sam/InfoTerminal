"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { 
  ExternalLink, 
  Search, 
  Shield, 
  Star,
  AlertTriangle,
  CheckCircle,
  Clock,
  Globe,
  BookOpen,
  Newspaper,
  GraduationCap
} from 'lucide-react';

interface Evidence {
  id: string;
  source_url: string;
  source_title: string;
  source_type: string;
  snippet: string;
  relevance_score: number;
  credibility_score: number;
  publication_date?: string;
  author?: string;
  domain?: string;
}

interface EvidenceViewerProps {
  claim?: string;
  onStanceClassification?: (evidence: Evidence) => void;
  className?: string;
}

export function EvidenceViewer({ claim, onStanceClassification, className }: EvidenceViewerProps) {
  const [evidence, setEvidence] = useState<Evidence[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchClaim, setSearchClaim] = useState(claim || '');
  const [maxSources, setMaxSources] = useState(5);
  const [sourceTypes, setSourceTypes] = useState<string[]>(['web', 'wikipedia', 'news']);

  useEffect(() => {
    if (claim && claim !== searchClaim) {
      setSearchClaim(claim);
      handleFindEvidence(claim);
    }
  }, [claim]);

  const handleFindEvidence = async (claimText: string = searchClaim) => {
    if (!claimText.trim()) {
      setError('Please enter a claim to find evidence for');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/verification/find-evidence', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claim: claimText,
          max_sources: maxSources,
          source_types: sourceTypes,
          language: 'en'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to find evidence');
      }

      const evidenceData = await response.json();
      setEvidence(evidenceData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getSourceIcon = (sourceType: string) => {
    switch (sourceType) {
      case 'wikipedia': return <BookOpen className="h-4 w-4" />;
      case 'news': return <Newspaper className="h-4 w-4" />;
      case 'academic': return <GraduationCap className="h-4 w-4" />;
      case 'web': return <Globe className="h-4 w-4" />;
      default: return <ExternalLink className="h-4 w-4" />;
    }
  };

  const getSourceTypeColor = (sourceType: string) => {
    switch (sourceType) {
      case 'wikipedia': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'news': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'academic': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300';
      case 'web': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getCredibilityIcon = (score: number) => {
    if (score >= 0.8) return <Shield className="h-4 w-4 text-green-500" />;
    if (score >= 0.6) return <CheckCircle className="h-4 w-4 text-yellow-500" />;
    return <AlertTriangle className="h-4 w-4 text-red-500" />;
  };

  const getRelevanceStars = (score: number) => {
    const stars = Math.round(score * 5);
    return (
      <div className="flex">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`h-3 w-3 ${
              star <= stars ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
          />
        ))}
      </div>
    );
  };

  const handleSourceTypeToggle = (type: string) => {
    setSourceTypes(prev => 
      prev.includes(type) 
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Search className="h-5 w-5" />
          <CardTitle>Evidence Retrieval</CardTitle>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Search Configuration */}
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">Claim to Verify</label>
            <textarea
              value={searchClaim}
              onChange={(e) => setSearchClaim(e.target.value)}
              placeholder="Enter the claim you want to find evidence for..."
              className="w-full p-3 border rounded mt-1 min-h-20"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Max Sources</label>
              <select
                value={maxSources}
                onChange={(e) => setMaxSources(Number(e.target.value))}
                className="w-full p-2 border rounded mt-1"
              >
                <option value={3}>3 sources</option>
                <option value={5}>5 sources</option>
                <option value={10}>10 sources</option>
                <option value={15}>15 sources</option>
              </select>
            </div>

            <div>
              <label className="text-sm font-medium">Source Types</label>
              <div className="flex flex-wrap gap-2 mt-1">
                {['web', 'wikipedia', 'news', 'academic'].map((type) => (
                  <button
                    key={type}
                    onClick={() => handleSourceTypeToggle(type)}
                    className={`px-2 py-1 text-xs border rounded ${
                      sourceTypes.includes(type)
                        ? 'bg-blue-100 border-blue-300 text-blue-800'
                        : 'bg-gray-100 border-gray-300 text-gray-600'
                    }`}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <Button
            onClick={() => handleFindEvidence()}
            disabled={isLoading || !searchClaim.trim()}
            className="w-full"
          >
            {isLoading ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                Finding Evidence...
              </>
            ) : (
              <>
                <Search className="h-4 w-4 mr-2" />
                Find Evidence
              </>
            )}
          </Button>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Results */}
        {evidence.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium">Evidence Found</h3>
              <Badge variant="outline">
                {evidence.length} source{evidence.length !== 1 ? 's' : ''}
              </Badge>
            </div>

            <div className="space-y-4">
              {evidence.map((item) => (
                <div
                  key={item.id}
                  className="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors"
                >
                  <div className="space-y-3">
                    {/* Header */}
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-2">
                        {getSourceIcon(item.source_type)}
                        <Badge className={getSourceTypeColor(item.source_type)}>
                          {item.source_type}
                        </Badge>
                        {item.domain && (
                          <span className="text-xs text-muted-foreground">
                            {item.domain}
                          </span>
                        )}
                      </div>
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </div>

                    {/* Title */}
                    <h4 className="font-medium text-sm">{item.source_title}</h4>

                    {/* Snippet */}
                    <p className="text-sm text-gray-600 dark:text-gray-300 line-clamp-3">
                      {item.snippet}
                    </p>

                    {/* Metadata */}
                    {(item.author || item.publication_date) && (
                      <div className="flex gap-4 text-xs text-muted-foreground">
                        {item.author && (
                          <span>By: {item.author}</span>
                        )}
                        {item.publication_date && (
                          <span>Published: {item.publication_date}</span>
                        )}
                      </div>
                    )}

                    {/* Scores */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-1">
                          <span className="text-xs text-muted-foreground">Relevance:</span>
                          {getRelevanceStars(item.relevance_score)}
                          <span className="text-xs text-muted-foreground ml-1">
                            ({(item.relevance_score * 100).toFixed(0)}%)
                          </span>
                        </div>
                        
                        <div className="flex items-center gap-1">
                          {getCredibilityIcon(item.credibility_score)}
                          <span className="text-xs text-muted-foreground">
                            Credibility: {(item.credibility_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>

                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          if (onStanceClassification) {
                            onStanceClassification(item);
                          }
                        }}
                      >
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Check Stance
                      </Button>
                    </div>

                    {/* Progress bars for scores */}
                    <div className="space-y-2">
                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span>Relevance</span>
                          <span>{(item.relevance_score * 100).toFixed(0)}%</span>
                        </div>
                        <Progress 
                          value={item.relevance_score * 100} 
                          className="h-1"
                        />
                      </div>
                      
                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span>Credibility</span>
                          <span>{(item.credibility_score * 100).toFixed(0)}%</span>
                        </div>
                        <Progress 
                          value={item.credibility_score * 100} 
                          className="h-1"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="p-3 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
              <h4 className="text-sm font-medium mb-2">Evidence Summary</h4>
              <div className="grid grid-cols-4 gap-4 text-xs">
                <div>
                  <span className="text-muted-foreground">Total Sources:</span>
                  <span className="ml-1 font-medium">{evidence.length}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Avg Relevance:</span>
                  <span className="ml-1 font-medium">
                    {(evidence.reduce((sum, e) => sum + e.relevance_score, 0) / evidence.length * 100).toFixed(0)}%
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Avg Credibility:</span>
                  <span className="ml-1 font-medium">
                    {(evidence.reduce((sum, e) => sum + e.credibility_score, 0) / evidence.length * 100).toFixed(0)}%
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">High Quality:</span>
                  <span className="ml-1 font-medium">
                    {evidence.filter(e => e.relevance_score > 0.7 && e.credibility_score > 0.7).length}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
