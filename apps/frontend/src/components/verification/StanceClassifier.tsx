"use client";

import React, { useState, useEffect } from 'react';
import Panel from '@/components/layout/Panel';
import { LoadingSpinner } from '@/components/ui/loading';
import { inputStyles, buttonStyles, textStyles, cardStyles, statusStyles, compose } from '@/styles/design-tokens';
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
    <Panel title="Stance Classification" className={className}>
      <div className="space-y-6">
        {/* Input Section */}
        <div className="space-y-4">
          <div>
            <label className={`${textStyles.body} font-medium`}>Claim to Verify</label>
            <textarea
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              placeholder="Enter the claim to be verified..."
              className={`${inputStyles.base} mt-1 min-h-20`}
            />
          </div>

          <div>
            <label className={`${textStyles.body} font-medium`}>Evidence Text</label>
            <textarea
              value={evidence}
              onChange={(e) => setEvidence(e.target.value)}
              placeholder="Enter the evidence text to analyze..."
              className={`${inputStyles.base} mt-1 min-h-24`}
            />
          </div>

          <div>
            <label className={`${textStyles.body} font-medium`}>Additional Context (Optional)</label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Enter any additional context that might help with classification..."
              className={`${inputStyles.base} mt-1 min-h-16`}
            />
          </div>

          <button
            onClick={handleClassifyStance}
            disabled={isLoading || !claim.trim() || !evidence.trim()}
            className={`w-full ${compose.button('primary', (isLoading || !claim.trim() || !evidence.trim()) ? 'opacity-50 cursor-not-allowed' : '')}`}
          >
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" variant="primary" layout="inline" />
                Classifying Stance...
              </>
            ) : (
              <>
                <Scale className="h-4 w-4 mr-2" />
                Classify Stance
              </>
            )}
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className={`${cardStyles.base} ${cardStyles.padding} ${statusStyles.error} border-red-200 dark:border-red-800`}>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              <span className={textStyles.body}>{error}</span>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className={textStyles.h3}>Stance Analysis Result</h3>
              <div className="flex items-center gap-2">
                {getStanceIcon(result.stance)}
                <span className={`${getStanceColor(result.stance)} px-3 py-1 rounded-full text-sm font-medium uppercase`}>
                  {result.stance}
                </span>
              </div>
            </div>

            {/* Main Result Card */}
            <div className={`${cardStyles.base} ${cardStyles.padding} bg-gray-50 dark:bg-gray-900/20`}>
              <div className="space-y-4">
                {/* Stance and Confidence */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getStanceIcon(result.stance)}
                    <div>
                      <p className={`${textStyles.body} font-medium`}>
                        Stance: <span className="capitalize">{result.stance}</span>
                      </p>
                      <p className={textStyles.bodySmall}>
                        The evidence {result.stance}s the claim
                      </p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <p className={`font-medium ${getConfidenceLevel(result.confidence).color}`}>
                      {getConfidenceLevel(result.confidence).level} Confidence
                    </p>
                    <p className={textStyles.bodySmall}>
                      {(result.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>

                {/* Confidence Progress Bar */}
                <div>
                  <div className={`flex justify-between ${textStyles.bodySmall} mb-1`}>
                    <span>Confidence Level</span>
                    <span>{(result.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                </div>

                {/* Evidence Type */}
                <div className="flex items-center gap-2">
                  {getEvidenceTypeIcon(result.evidence_type)}
                  <span className={`${textStyles.body} font-medium`}>Evidence Type:</span>
                  <span className={`${statusStyles.info} px-2 py-1 rounded text-sm font-medium capitalize`}>
                    {result.evidence_type}
                  </span>
                </div>
              </div>
            </div>

            {/* Reasoning */}
            <div className="space-y-2">
              <h4 className={`${textStyles.body} font-medium`}>Analysis Reasoning</h4>
              <div className={`${cardStyles.base} p-3 bg-blue-50 dark:bg-blue-900/20`}>
                <p className={textStyles.body}>{result.reasoning}</p>
              </div>
            </div>

            {/* Key Phrases */}
            {result.key_phrases && result.key_phrases.length > 0 && (
              <div className="space-y-2">
                <h4 className={`${textStyles.body} font-medium`}>Key Indicators</h4>
                <div className="flex flex-wrap gap-2">
                  {result.key_phrases.map((phrase, index) => (
                    <span key={index} className={`${statusStyles.neutral} px-2 py-1 rounded text-sm`}>
                      {phrase}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Stance Interpretation Guide */}
            <div className={`${cardStyles.base} p-3 bg-gray-50 dark:bg-gray-900/20`}>
              <h4 className={`${textStyles.body} font-medium mb-2`}>Stance Meanings</h4>
              <div className="grid grid-cols-2 gap-2">
                <div className="flex items-center gap-1">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  <span className={textStyles.bodySmall}><strong>Support:</strong> Evidence confirms the claim</span>
                </div>
                <div className="flex items-center gap-1">
                  <XCircle className="h-3 w-3 text-red-500" />
                  <span className={textStyles.bodySmall}><strong>Contradict:</strong> Evidence refutes the claim</span>
                </div>
                <div className="flex items-center gap-1">
                  <Minus className="h-3 w-3 text-yellow-500" />
                  <span className={textStyles.bodySmall}><strong>Neutral:</strong> Evidence is neither for nor against</span>
                </div>
                <div className="flex items-center gap-1">
                  <HelpCircle className="h-3 w-3 text-gray-500" />
                  <span className={textStyles.bodySmall}><strong>Unrelated:</strong> Evidence doesn't address the claim</span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              <button
                className={compose.button('secondary', 'text-sm px-3 py-2')}
                onClick={() => {
                  setClaim('');
                  setEvidence('');
                  setContext('');
                  setResult(null);
                  setError(null);
                }}
              >
                Clear & Start Over
              </button>
              
              <button
                className={compose.button('secondary', 'text-sm px-3 py-2')}
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
              </button>
            </div>
          </div>
        )}
      </div>
    </Panel>
  );
}
