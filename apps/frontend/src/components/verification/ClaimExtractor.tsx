"use client";

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
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
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Search className="h-5 w-5" />
          <CardTitle>Claim Extraction</CardTitle>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Input Section */}
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">Text to Analyze</label>
            <Textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter or paste text to extract verifiable claims from..."
              className="min-h-32"
            />
            <div className="text-xs text-muted-foreground mt-1">
              {inputText.length} characters
            </div>
          </div>

          {/* Settings */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Confidence Threshold</label>
              <select
                value={confidenceThreshold}
                onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                className="w-full p-2 border rounded mt-1"
              >
                <option value={0.5}>0.5 - More claims</option>
                <option value={0.7}>0.7 - Balanced</option>
                <option value={0.8}>0.8 - High confidence</option>
                <option value={0.9}>0.9 - Very high confidence</option>
              </select>
            </div>
            
            <div>
              <label className="text-sm font-medium">Max Claims</label>
              <select
                value={maxClaims}
                onChange={(e) => setMaxClaims(Number(e.target.value))}
                className="w-full p-2 border rounded mt-1"
              >
                <option value={5}>5 claims</option>
                <option value={10}>10 claims</option>
                <option value={20}>20 claims</option>
                <option value={50}>50 claims</option>
              </select>
            </div>
          </div>

          <Button
            onClick={handleExtractClaims}
            disabled={isLoading || !inputText.trim()}
            className="w-full"
          >
            {isLoading ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                Extracting Claims...
              </>
            ) : (
              <>
                <Zap className="h-4 w-4 mr-2" />
                Extract Claims
              </>
            )}
          </Button>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Results */}
        {claims.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium">Extracted Claims</h3>
              <Badge variant="outline">
                {claims.length} claim{claims.length !== 1 ? 's' : ''} found
              </Badge>
            </div>

            <div className="space-y-3">
              {claims.map((claim) => (
                <div
                  key={claim.id}
                  className="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getConfidenceIcon(claim.confidence)}
                      <Badge className={getClaimTypeColor(claim.claim_type)}>
                        {claim.claim_type}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        {(claim.confidence * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <p className="text-sm font-medium">{claim.text}</p>
                    
                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div>
                        <span className="text-muted-foreground">Subject:</span>
                        <p className="font-medium">{claim.subject}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Predicate:</span>
                        <p className="font-medium">{claim.predicate}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Object:</span>
                        <p className="font-medium">{claim.object}</p>
                      </div>
                    </div>

                    {(claim.temporal || claim.location) && (
                      <div className="flex gap-4 text-xs">
                        {claim.temporal && (
                          <div>
                            <span className="text-muted-foreground">When:</span>
                            <span className="ml-1 font-medium">{claim.temporal}</span>
                          </div>
                        )}
                        {claim.location && (
                          <div>
                            <span className="text-muted-foreground">Where:</span>
                            <span className="ml-1 font-medium">{claim.location}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="mt-3 flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        // This would trigger evidence search for this claim
                        if (onClaimsExtracted) {
                          onClaimsExtracted([claim]);
                        }
                      }}
                    >
                      <FileText className="h-3 w-3 mr-1" />
                      Find Evidence
                    </Button>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="p-3 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
              <h4 className="text-sm font-medium mb-2">Summary</h4>
              <div className="grid grid-cols-4 gap-4 text-xs">
                <div>
                  <span className="text-muted-foreground">Factual:</span>
                  <span className="ml-1 font-medium">
                    {claims.filter(c => c.claim_type === 'factual').length}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Opinion:</span>
                  <span className="ml-1 font-medium">
                    {claims.filter(c => c.claim_type === 'opinion').length}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Prediction:</span>
                  <span className="ml-1 font-medium">
                    {claims.filter(c => c.claim_type === 'prediction').length}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Avg Confidence:</span>
                  <span className="ml-1 font-medium">
                    {(claims.reduce((sum, c) => sum + c.confidence, 0) / claims.length * 100).toFixed(0)}%
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
