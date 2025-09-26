"use client";

import React, { useState, useEffect, useCallback } from "react";
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
  GraduationCap,
} from "lucide-react";

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
  const [searchClaim, setSearchClaim] = useState(claim || "");
  const [maxSources, setMaxSources] = useState(5);
  const [sourceTypes, setSourceTypes] = useState<string[]>(["web", "wikipedia", "news"]);

  const handleFindEvidence = useCallback(async (claimText: string = searchClaim) => {
    if (!claimText.trim()) {
      setError("Please enter a claim to find evidence for");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/verification/find-evidence", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          claim: claimText,
          max_sources: maxSources,
          source_types: sourceTypes,
          language: "en",
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to find evidence");
      }

      const evidenceData = await response.json();
      setEvidence(evidenceData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  }, [searchClaim, maxSources, sourceTypes]);

  useEffect(() => {
    if (claim && claim !== searchClaim) {
      setSearchClaim(claim);
      handleFindEvidence(claim);
    }
  }, [claim, searchClaim, handleFindEvidence]);

  const getSourceIcon = (sourceType: string) => {
    switch (sourceType) {
      case "wikipedia":
        return <BookOpen className="h-4 w-4" />;
      case "news":
        return <Newspaper className="h-4 w-4" />;
      case "academic":
        return <GraduationCap className="h-4 w-4" />;
      case "web":
        return <Globe className="h-4 w-4" />;
      default:
        return <ExternalLink className="h-4 w-4" />;
    }
  };

  const getSourceTypeColor = (sourceType: string) => {
    switch (sourceType) {
      case "wikipedia":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
      case "news":
        return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
      case "academic":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300";
      case "web":
        return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
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
              star <= stars ? "text-yellow-400 fill-current" : "text-gray-300"
            }`}
          />
        ))}
      </div>
    );
  };

  const handleSourceTypeToggle = (type: string) => {
    setSourceTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type],
    );
  };

  return (
    <Panel title="Evidence Retrieval" className={className}>
      <div className="space-y-6">
        {/* Search Configuration */}
        <div className="space-y-4">
          <div>
            <label className={`${textStyles.body} font-medium`}>Claim to Verify</label>
            <textarea
              value={searchClaim}
              onChange={(e) => setSearchClaim(e.target.value)}
              placeholder="Enter the claim you want to find evidence for..."
              className={`${inputStyles.base} mt-1 min-h-20`}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={`${textStyles.body} font-medium`}>Max Sources</label>
              <select
                value={maxSources}
                onChange={(e) => setMaxSources(Number(e.target.value))}
                className={`${inputStyles.base} mt-1`}
              >
                <option value={3}>3 sources</option>
                <option value={5}>5 sources</option>
                <option value={10}>10 sources</option>
                <option value={15}>15 sources</option>
              </select>
            </div>

            <div>
              <label className={`${textStyles.body} font-medium`}>Source Types</label>
              <div className="flex flex-wrap gap-2 mt-1">
                {["web", "wikipedia", "news", "academic"].map((type) => (
                  <button
                    key={type}
                    onClick={() => handleSourceTypeToggle(type)}
                    className={`px-2 py-1 text-xs border rounded ${
                      sourceTypes.includes(type)
                        ? "bg-blue-100 border-blue-300 text-blue-800 dark:bg-blue-900/30 dark:border-blue-600 dark:text-blue-300"
                        : "bg-gray-100 border-gray-300 text-gray-600 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400"
                    }`}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button
            onClick={() => handleFindEvidence()}
            disabled={isLoading || !searchClaim.trim()}
            className={`w-full ${compose.button("primary", isLoading || !searchClaim.trim() ? "opacity-50 cursor-not-allowed" : "")}`}
          >
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" variant="primary" layout="inline" />
                Finding Evidence...
              </>
            ) : (
              <>
                <Search className="h-4 w-4 mr-2" />
                Find Evidence
              </>
            )}
          </button>
        </div>

        {/* Error Alert */}
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
        {evidence.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className={textStyles.h3}>Evidence Found</h3>
              <span className={`${statusStyles.info} px-3 py-1 rounded-full text-sm font-medium`}>
                {evidence.length} source{evidence.length !== 1 ? "s" : ""}
              </span>
            </div>

            <div className="space-y-4">
              {evidence.map((item) => (
                <div
                  key={item.id}
                  className={`${cardStyles.base} ${cardStyles.padding} hover:shadow-md transition-all`}
                >
                  <div className="space-y-3">
                    {/* Header */}
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-2">
                        {getSourceIcon(item.source_type)}
                        <span
                          className={`${getSourceTypeColor(item.source_type)} px-2 py-1 rounded text-sm font-medium`}
                        >
                          {item.source_type}
                        </span>
                        {item.domain && <span className={textStyles.bodySmall}>{item.domain}</span>}
                      </div>
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </div>

                    {/* Title */}
                    <h4 className={`${textStyles.body} font-medium`}>{item.source_title}</h4>

                    {/* Snippet */}
                    <p className={`${textStyles.body} line-clamp-3`}>{item.snippet}</p>

                    {/* Metadata */}
                    {(item.author || item.publication_date) && (
                      <div className={`flex gap-4 ${textStyles.bodySmall}`}>
                        {item.author && <span>By: {item.author}</span>}
                        {item.publication_date && <span>Published: {item.publication_date}</span>}
                      </div>
                    )}

                    {/* Scores */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-1">
                          <span className={textStyles.bodySmall}>Relevance:</span>
                          {getRelevanceStars(item.relevance_score)}
                          <span className={`${textStyles.bodySmall} ml-1`}>
                            ({(item.relevance_score * 100).toFixed(0)}%)
                          </span>
                        </div>

                        <div className="flex items-center gap-1">
                          {getCredibilityIcon(item.credibility_score)}
                          <span className={textStyles.bodySmall}>
                            Credibility: {(item.credibility_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>

                      <button
                        className={compose.button("secondary", "text-sm px-3 py-1.5")}
                        onClick={() => {
                          if (onStanceClassification) {
                            onStanceClassification(item);
                          }
                        }}
                      >
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Check Stance
                      </button>
                    </div>

                    {/* Progress bars for scores */}
                    <div className="space-y-2">
                      <div>
                        <div className={`flex justify-between ${textStyles.bodySmall} mb-1`}>
                          <span>Relevance</span>
                          <span>{(item.relevance_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                          <div
                            className="bg-blue-600 h-1 rounded-full transition-all duration-300"
                            style={{ width: `${item.relevance_score * 100}%` }}
                          />
                        </div>
                      </div>

                      <div>
                        <div className={`flex justify-between ${textStyles.bodySmall} mb-1`}>
                          <span>Credibility</span>
                          <span>{(item.credibility_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                          <div
                            className="bg-green-600 h-1 rounded-full transition-all duration-300"
                            style={{ width: `${item.credibility_score * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className={`${cardStyles.base} p-3 bg-gray-50 dark:bg-gray-900/20`}>
              <h4 className={`${textStyles.body} font-medium mb-2`}>Evidence Summary</h4>
              <div className={`grid grid-cols-4 gap-4 ${textStyles.bodySmall}`}>
                <div>
                  <span>Total Sources:</span>
                  <span className="ml-1 font-medium">{evidence.length}</span>
                </div>
                <div>
                  <span>Avg Relevance:</span>
                  <span className="ml-1 font-medium">
                    {(
                      (evidence.reduce((sum, e) => sum + e.relevance_score, 0) / evidence.length) *
                      100
                    ).toFixed(0)}
                    %
                  </span>
                </div>
                <div>
                  <span>Avg Credibility:</span>
                  <span className="ml-1 font-medium">
                    {(
                      (evidence.reduce((sum, e) => sum + e.credibility_score, 0) /
                        evidence.length) *
                      100
                    ).toFixed(0)}
                    %
                  </span>
                </div>
                <div>
                  <span>High Quality:</span>
                  <span className="ml-1 font-medium">
                    {
                      evidence.filter((e) => e.relevance_score > 0.7 && e.credibility_score > 0.7)
                        .length
                    }
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Panel>
  );
}
