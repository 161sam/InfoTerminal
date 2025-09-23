"use client";

import React, { useState } from 'react';
import Panel from '@/components/layout/Panel';
import { LoadingSpinner } from '@/components/ui/loading';
import { inputStyles, buttonStyles, textStyles, cardStyles, statusStyles, compose } from '@/styles/design-tokens';
import { 
  Search, 
  FileText, 
  AlertCircle,
  CheckCircle,
  XCircle,
  Clock,
  Zap
} from 'lucide-react';

interface Claim {
  id: string;
  text: string;
  confidence: number;
  claim_type: string;
  subject: string;
  predicate: string;
  object: string;
  temporal?: string;
  location?: string;
}

interface ClaimExtractorProps {
  onClaimsExtracted?: (claims: Claim[]) => void;
  className?: string;
}

export function ClaimExtractor({ onClaimsExtracted, className }: ClaimExtractorProps) {
  const [inputText, setInputText] = useState('');
  const [claims, setClaims] = useState<Claim[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.7);
  const [maxClaims, setMaxClaims] = useState(10);

  const handleExtractClaims = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/verification/extract-claims', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          confidence_threshold: confidenceThreshold,
          max_claims: maxClaims
        })
      });

      if (!response.ok) {
        throw new Error('Failed to extract claims');
      }

      const extractedClaims = await response.json();
      setClaims(extractedClaims);
      
      if (onClaimsExtracted) {
        onClaimsExtracted(extractedClaims);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getClaimTypeColor = (type: string) => {
    switch (type) {
      case 'factual': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'opinion': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'prediction': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300';
      case 'causal': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getConfidenceIcon = (confidence: number) => {
    if (confidence >= 0.8) return <CheckCircle className="h-4 w-4 text-green-500" />;
    if (confidence >= 0.6) return <Clock className="h-4 w-4 text-yellow-500" />;
    return <AlertCircle className="h-4 w-4 text-red-500" />;
  };

  return (
    <Panel title="Claim Extraction" className={className}>
      <div className="space-y-6">
        {/* Input Section */}
        <div className="space-y-4">
          <div>
            <label className={`${textStyles.body} font-medium`}>Text to Analyze</label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter or paste text to extract verifiable claims from..."
              className={`${inputStyles.base} min-h-32`}
            />
            <div className={`${textStyles.bodySmall} mt-1`}>
              {inputText.length} characters
            </div>
          </div>

          {/* Settings */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={`${textStyles.body} font-medium`}>Confidence Threshold</label>
              <select
                value={confidenceThreshold}
                onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                className={`${inputStyles.base} mt-1`}
              >
                <option value={0.5}>0.5 - More claims</option>
                <option value={0.7}>0.7 - Balanced</option>
                <option value={0.8}>0.8 - High confidence</option>
                <option value={0.9}>0.9 - Very high confidence</option>
              </select>
            </div>
            
            <div>
              <label className={`${textStyles.body} font-medium`}>Max Claims</label>
              <select
                value={maxClaims}
                onChange={(e) => setMaxClaims(Number(e.target.value))}
                className={`${inputStyles.base} mt-1`}
              >
                <option value={5}>5 claims</option>
                <option value={10}>10 claims</option>
                <option value={20}>20 claims</option>
                <option value={50}>50 claims</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleExtractClaims}
            disabled={isLoading || !inputText.trim()}
            className={`w-full ${compose.button('primary', (isLoading || !inputText.trim()) ? 'opacity-50 cursor-not-allowed' : '')}`}
          >
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" variant="primary" layout="inline" />
                Extracting Claims...
              </>
            ) : (
              <>
                <Zap className="h-4 w-4 mr-2" />
                Extract Claims
              </>
            )}
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className={`${cardStyles.base} ${cardStyles.padding} ${statusStyles.error} border-red-200 dark:border-red-800`}>
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4" />
              <span className={textStyles.body}>{error}</span>
            </div>
          </div>
        )}

        {/* Results */}
        {claims.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className={textStyles.h3}>Extracted Claims</h3>
              <span className={`${statusStyles.info} px-3 py-1 rounded-full text-sm font-medium`}>
                {claims.length} claim{claims.length !== 1 ? 's' : ''} found
              </span>
            </div>

            <div className="space-y-3">
              {claims.map((claim) => (
                <div
                  key={claim.id}
                  className={`${cardStyles.base} ${cardStyles.padding} hover:shadow-md transition-all`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getConfidenceIcon(claim.confidence)}
                      <span className={`${getClaimTypeColor(claim.claim_type)} px-2 py-1 rounded text-sm font-medium`}>
                        {claim.claim_type}
                      </span>
                      <span className={textStyles.bodySmall}>
                        {(claim.confidence * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <p className={`${textStyles.body} font-medium`}>{claim.text}</p>
                    
                    <div className="grid grid-cols-3 gap-2">
                      <div>
                        <span className={textStyles.bodySmall}>Subject:</span>
                        <p className={`${textStyles.bodySmall} font-medium`}>{claim.subject}</p>
                      </div>
                      <div>
                        <span className={textStyles.bodySmall}>Predicate:</span>
                        <p className={`${textStyles.bodySmall} font-medium`}>{claim.predicate}</p>
                      </div>
                      <div>
                        <span className={textStyles.bodySmall}>Object:</span>
                        <p className={`${textStyles.bodySmall} font-medium`}>{claim.object}</p>
                      </div>
                    </div>

                    {(claim.temporal || claim.location) && (
                      <div className={`flex gap-4 ${textStyles.bodySmall}`}>
                        {claim.temporal && (
                          <div>
                            <span className={textStyles.bodySmall}>When:</span>
                            <span className="ml-1 font-medium">{claim.temporal}</span>
                          </div>
                        )}
                        {claim.location && (
                          <div>
                            <span className={textStyles.bodySmall}>Where:</span>
                            <span className="ml-1 font-medium">{claim.location}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="mt-3 flex gap-2">
                    <button
                      className={compose.button('secondary', 'text-sm px-3 py-1.5')}
                      onClick={() => {
                        // This would trigger evidence search for this claim
                        if (onClaimsExtracted) {
                          onClaimsExtracted([claim]);
                        }
                      }}
                    >
                      <FileText className="h-3 w-3 mr-1" />
                      Find Evidence
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className={`${cardStyles.base} p-3 bg-gray-50 dark:bg-gray-900/20`}>
              <h4 className={`${textStyles.body} font-medium mb-2`}>Summary</h4>
              <div className={`grid grid-cols-4 gap-4 ${textStyles.bodySmall}`}>
                <div>
                  <span className={textStyles.bodySmall}>Factual:</span>
                  <span className="ml-1 font-medium">
                    {claims.filter(c => c.claim_type === 'factual').length}
                  </span>
                </div>
                <div>
                  <span className={textStyles.bodySmall}>Opinion:</span>
                  <span className="ml-1 font-medium">
                    {claims.filter(c => c.claim_type === 'opinion').length}
                  </span>
                </div>
                <div>
                  <span className={textStyles.bodySmall}>Prediction:</span>
                  <span className="ml-1 font-medium">
                    {claims.filter(c => c.claim_type === 'prediction').length}
                  </span>
                </div>
                <div>
                  <span className={textStyles.bodySmall}>Avg Confidence:</span>
                  <span className="ml-1 font-medium">
                    {(claims.reduce((sum, c) => sum + c.confidence, 0) / claims.length * 100).toFixed(0)}%
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
