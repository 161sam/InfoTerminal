"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { 
  Scale, 
  CheckCircle, 
  XCircle, 
  Minus,
  HelpCircle,
  Target,
  AlertTriangle,
  Brain,
  Eye
} from 'lucide-react';

interface Evidence {
  id: string;
  source_url: string;
  source_title: string;
  snippet: string;
}

interface StanceResult {
  stance: string;
  confidence: number;
  reasoning: string;
  key_phrases: string[];
  evidence_type: string;
}

interface StanceClassifierProps {
  claim?: string;
  evidence?: Evidence;
  onStanceResult?: (result: StanceResult) => void;
  className?: string;
}

export function StanceClassifier({ 
  claim: initialClaim, 
  evidence: initialEvidence, 
  onStanceResult, 
  className 
}: StanceClassifierProps) {
  const [claim, setClaim] = useState(initialClaim || '');
  const [evidence, setEvidence] = useState(initialEvidence?.snippet || '');
  const [context, setContext] = useState('');
  const [result, setResult] = useState<StanceResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialClaim !== claim) {
      setClaim(initialClaim || '');
    }
  }, [initialClaim]);

  useEffect(() => {
    if (initialEvidence && initialEvidence.snippet !== evidence) {
      setEvidence(initialEvidence.snippet);
      // Auto-classify if both claim and evidence are provided
      if (initialClaim && initialEvidence.snippet) {
        handleClassifyStance();
      }
    }
  }, [initialEvidence]);

  const handleClassifyStance = async () => {
    if (!claim.trim() || !evidence.trim()) {
      setError('Please provide both a claim and evidence to classify');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/verification/classify-stance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claim: claim.trim(),
          evidence: evidence.trim(),
          context: context.trim() || null
        })
      });

      if (!response.ok) {
        throw new Error('Failed to classify stance');
      }

      const stanceResult = await response.json();
      setResult(stanceResult);
      
      if (onStanceResult) {
        onStanceResult(stanceResult);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getStanceIcon = (stance: string) => {
    switch (stance) {
      case 'support': return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'contradict': return <XCircle className="h-5 w-5 text-red-500" />;
      case 'neutral': return <Minus className="h-5 w-5 text-yellow-500" />;
      case 'unrelated': return <HelpCircle className="h-5 w-5 text-gray-500" />;
      default: return <Scale className="h-5 w-5 text-blue-500" />;
    }
  };

  const getStanceColor = (stance: string) => {
    switch (stance) {
      case 'support': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      case 'contradict': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'neutral': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'unrelated': return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
      default: return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
    }
  };

  const getEvidenceTypeIcon = (type: string) => {
    switch (type) {
      case 'direct': return <Target className="h-4 w-4 text-green-600" />;
      case 'indirect': return <Eye className="h-4 w-4 text-yellow-600" />;
      case 'contextual': return <Brain className="h-4 w-4 text-blue-600" />;
      default: return <HelpCircle className="h-4 w-4 text-gray-600" />;
    }
  };

  const getConfidenceLevel = (confidence: number) => {
    if (confidence >= 0.8) return { level: 'High', color: 'text-green-600' };
    if (confidence >= 0.6) return { level: 'Medium', color: 'text-yellow-600' };
    return { level: 'Low', color: 'text-red-600' };
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Scale className="h-5 w-5" />
          <CardTitle>Stance Classification</CardTitle>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Input Section */}
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">Claim to Verify</label>
            <textarea
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              placeholder="Enter the claim to be verified..."
              className="w-full p-3 border rounded mt-1 min-h-20"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Evidence Text</label>
            <textarea
              value={evidence}
              onChange={(e) => setEvidence(e.target.value)}
              placeholder="Enter the evidence text to analyze..."
              className="w-full p-3 border rounded mt-1 min-h-24"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Additional Context (Optional)</label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Enter any additional context that might help with classification..."
              className="w-full p-3 border rounded mt-1 min-h-16"
            />
          </div>

          <Button
            onClick={handleClassifyStance}
            disabled={isLoading || !claim.trim() || !evidence.trim()}
            className="w-full"
          >
            {isLoading ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                Classifying Stance...
              </>
            ) : (
              <>
                <Scale className="h-4 w-4 mr-2" />
                Classify Stance
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
        {result && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium">Stance Analysis Result</h3>
              <div className="flex items-center gap-2">
                {getStanceIcon(result.stance)}
                <Badge className={getStanceColor(result.stance)}>
                  {result.stance.toUpperCase()}
                </Badge>
              </div>
            </div>

            {/* Main Result Card */}
            <div className="p-4 border rounded-lg bg-gray-50 dark:bg-gray-900/20">
              <div className="space-y-4">
                {/* Stance and Confidence */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getStanceIcon(result.stance)}
                    <div>
                      <p className="font-medium">
                        Stance: <span className="capitalize">{result.stance}</span>
                      </p>
                      <p className="text-sm text-muted-foreground">
                        The evidence {result.stance}s the claim
                      </p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <p className={`font-medium ${getConfidenceLevel(result.confidence).color}`}>
                      {getConfidenceLevel(result.confidence).level} Confidence
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {(result.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>

                {/* Confidence Progress Bar */}
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span>Confidence Level</span>
                    <span>{(result.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <Progress 
                    value={result.confidence * 100} 
                    className="h-2"
                  />
                </div>

                {/* Evidence Type */}
                <div className="flex items-center gap-2">
                  {getEvidenceTypeIcon(result.evidence_type)}
                  <span className="text-sm font-medium">Evidence Type:</span>
                  <Badge variant="outline" className="capitalize">
                    {result.evidence_type}
                  </Badge>
                </div>
              </div>
            </div>

            {/* Reasoning */}
            <div className="space-y-2">
              <h4 className="font-medium">Analysis Reasoning</h4>
              <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <p className="text-sm">{result.reasoning}</p>
              </div>
            </div>

            {/* Key Phrases */}
            {result.key_phrases && result.key_phrases.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-medium">Key Indicators</h4>
                <div className="flex flex-wrap gap-2">
                  {result.key_phrases.map((phrase, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {phrase}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Stance Interpretation Guide */}
            <div className="p-3 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
              <h4 className="text-sm font-medium mb-2">Stance Meanings</h4>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="flex items-center gap-1">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  <span><strong>Support:</strong> Evidence confirms the claim</span>
                </div>
                <div className="flex items-center gap-1">
                  <XCircle className="h-3 w-3 text-red-500" />
                  <span><strong>Contradict:</strong> Evidence refutes the claim</span>
                </div>
                <div className="flex items-center gap-1">
                  <Minus className="h-3 w-3 text-yellow-500" />
                  <span><strong>Neutral:</strong> Evidence is neither for nor against</span>
                </div>
                <div className="flex items-center gap-1">
                  <HelpCircle className="h-3 w-3 text-gray-500" />
                  <span><strong>Unrelated:</strong> Evidence doesn't address the claim</span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setClaim('');
                  setEvidence('');
                  setContext('');
                  setResult(null);
                  setError(null);
                }}
              >
                Clear & Start Over
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  // This could export or save the analysis
                  const analysisData = {
                    claim,
                    evidence: evidence.substring(0, 100) + '...',
                    stance: result.stance,
                    confidence: result.confidence,
                    timestamp: new Date().toISOString()
                  };
                  console.log('Analysis result:', analysisData);
                }}
              >
                Export Analysis
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
