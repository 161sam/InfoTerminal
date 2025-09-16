import React, { useState } from 'react';
import { 
  Shield, 
  Search, 
  Scale, 
  Target,
  Activity,
  CheckCircle
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { ClaimExtractor } from '@/components/verification/ClaimExtractor';
import { EvidenceViewer } from '@/components/verification/EvidenceViewer';
import { StanceClassifier } from '@/components/verification/StanceClassifier';
import { CredibilityDashboard } from '@/components/verification/CredibilityDashboard';

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

export default function VerificationPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'extract' | 'evidence' | 'stance' | 'credibility'>('overview');
  const [selectedClaim, setSelectedClaim] = useState<string>('');
  const [selectedEvidence, setSelectedEvidence] = useState<Evidence | undefined>(undefined);
  const [verificationStats, setVerificationStats] = useState({
    totalClaims: 0,
    evidenceSources: 0,
    stanceAnalyses: 0,
    credibilityChecks: 0
  });

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'extract', label: 'Extract Claims', icon: Search },
    { id: 'evidence', label: 'Find Evidence', icon: Target },
    { id: 'stance', label: 'Classify Stance', icon: Scale },
    { id: 'credibility', label: 'Check Credibility', icon: Shield }
  ];

  const handleClaimsExtracted = (claims: Claim[]) => {
    setVerificationStats(prev => ({ ...prev, totalClaims: claims.length }));
    if (claims.length > 0) {
      setSelectedClaim(claims[0].text);
      // Auto-switch to evidence tab
      setActiveTab('evidence');
    }
  };

  const handleEvidenceSelected = (evidence: Evidence) => {
    setSelectedEvidence(evidence);
    setVerificationStats(prev => ({ ...prev, evidenceSources: prev.evidenceSources + 1 }));
    // Auto-switch to stance tab
    setActiveTab('stance');
  };

  const handleStanceResult = (result: StanceResult) => {
    setVerificationStats(prev => ({ ...prev, stanceAnalyses: prev.stanceAnalyses + 1 }));
  };

  return (
    <DashboardLayout title="Verification Center" subtitle="Fact-checking and claim verification tools">
      <div className="p-6">
        <div className="max-w-7xl space-y-6">
          
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-2 border-b border-gray-200 dark:border-gray-800">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-t-lg border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'text-blue-600 border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                      : 'text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Stats Overview */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500">Claims Extracted</div>
                    <Search className="h-4 w-4 text-blue-500" />
                  </div>
                  <div className="text-2xl font-bold text-blue-600">{verificationStats.totalClaims}</div>
                  <div className="text-sm text-gray-500">From analyzed text</div>
                </Panel>

                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500">Evidence Sources</div>
                    <Target className="h-4 w-4 text-green-500" />
                  </div>
                  <div className="text-2xl font-bold text-green-600">{verificationStats.evidenceSources}</div>
                  <div className="text-sm text-gray-500">Retrieved for verification</div>
                </Panel>

                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500">Stance Analyses</div>
                    <Scale className="h-4 w-4 text-purple-500" />
                  </div>
                  <div className="text-2xl font-bold text-purple-600">{verificationStats.stanceAnalyses}</div>
                  <div className="text-sm text-gray-500">Completed classifications</div>
                </Panel>

                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500">Credibility Checks</div>
                    <Shield className="h-4 w-4 text-orange-500" />
                  </div>
                  <div className="text-2xl font-bold text-orange-600">{verificationStats.credibilityChecks}</div>
                  <div className="text-sm text-gray-500">Source assessments</div>
                </Panel>
              </div>

              {/* Feature Overview */}
              <Panel>
                <div className="flex items-center gap-3 mb-6">
                  <Shield className="h-6 w-6 text-blue-500" />
                  <h3 className="text-xl font-semibold">InfoTerminal v0.2.0 Verification Features</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Search className="h-5 w-5 text-blue-500" />
                      <h4 className="font-medium">Claim Extraction</h4>
                    </div>
                    <p className="text-sm text-gray-600">Automatically extract verifiable claims from text using advanced NLP models</p>
                  </div>
                  
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Target className="h-5 w-5 text-green-500" />
                      <h4 className="font-medium">Evidence Retrieval</h4>
                    </div>
                    <p className="text-sm text-gray-600">Find supporting evidence from multiple sources including web, news, and academic papers</p>
                  </div>
                  
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Scale className="h-5 w-5 text-purple-500" />
                      <h4 className="font-medium">Stance Classification</h4>
                    </div>
                    <p className="text-sm text-gray-600">Classify whether evidence supports, contradicts, or is neutral toward claims</p>
                  </div>
                  
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Shield className="h-5 w-5 text-orange-500" />
                      <h4 className="font-medium">Source Credibility</h4>
                    </div>
                    <p className="text-sm text-gray-600">Assess the credibility and bias of information sources automatically</p>
                  </div>
                </div>
              </Panel>

              {/* Workflow Guide */}
              <Panel>
                <h3 className="text-lg font-semibold mb-4">Verification Workflow</h3>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-600 rounded-full text-sm font-medium">
                      1
                    </div>
                    <div>
                      <h4 className="font-medium">Extract Claims</h4>
                      <p className="text-sm text-gray-600">Paste or type text to automatically identify verifiable claims</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-green-100 text-green-600 rounded-full text-sm font-medium">
                      2
                    </div>
                    <div>
                      <h4 className="font-medium">Find Evidence</h4>
                      <p className="text-sm text-gray-600">Search for supporting or contradicting evidence from reliable sources</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-purple-100 text-purple-600 rounded-full text-sm font-medium">
                      3
                    </div>
                    <div>
                      <h4 className="font-medium">Classify Stance</h4>
                      <p className="text-sm text-gray-600">Analyze whether evidence supports or contradicts the claim</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-orange-100 text-orange-600 rounded-full text-sm font-medium">
                      4
                    </div>
                    <div>
                      <h4 className="font-medium">Check Credibility</h4>
                      <p className="text-sm text-gray-600">Evaluate the reliability and bias of information sources</p>
                    </div>
                  </div>
                </div>
              </Panel>
            </div>
          )}

          {/* Extract Claims Tab */}
          {activeTab === 'extract' && (
            <ClaimExtractor onClaimsExtracted={handleClaimsExtracted} />
          )}

          {/* Find Evidence Tab */}
          {activeTab === 'evidence' && (
            <EvidenceViewer 
              claim={selectedClaim}
              onStanceClassification={handleEvidenceSelected}
            />
          )}

          {/* Classify Stance Tab */}
          {activeTab === 'stance' && (
            <StanceClassifier 
              claim={selectedClaim}
              evidence={selectedEvidence}
              onStanceResult={handleStanceResult}
            />
          )}

          {/* Check Credibility Tab */}
          {activeTab === 'credibility' && (
            <CredibilityDashboard 
              sourceUrl={selectedEvidence?.source_url}
            />
          )}

        </div>
      </div>
    </DashboardLayout>
  );
}
