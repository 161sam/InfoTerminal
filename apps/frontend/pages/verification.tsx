import React, { useState } from "react";
import { Shield, Search, Scale, Target, Activity, CheckCircle } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import { ClaimExtractor } from "@/components/verification/ClaimExtractor";
import { EvidenceViewer } from "@/components/verification/EvidenceViewer";
import { StanceClassifier } from "@/components/verification/StanceClassifier";
import { CredibilityDashboard } from "@/components/verification/CredibilityDashboard";
import {
  inputStyles,
  buttonStyles,
  textStyles,
  cardStyles,
  statusStyles,
  compose,
} from "@/styles/design-tokens";

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
  const [activeTab, setActiveTab] = useState<
    "overview" | "extract" | "evidence" | "stance" | "credibility"
  >("overview");
  const [selectedClaim, setSelectedClaim] = useState<string>("");
  const [selectedEvidence, setSelectedEvidence] = useState<Evidence | undefined>(undefined);
  const [verificationStats, setVerificationStats] = useState({
    totalClaims: 0,
    evidenceSources: 0,
    stanceAnalyses: 0,
    credibilityChecks: 0,
  });

  const tabs = [
    { id: "overview", label: "Overview", icon: Activity },
    { id: "extract", label: "Extract Claims", icon: Search },
    { id: "evidence", label: "Find Evidence", icon: Target },
    { id: "stance", label: "Classify Stance", icon: Scale },
    { id: "credibility", label: "Check Credibility", icon: Shield },
  ];

  const handleClaimsExtracted = (claims: Claim[]) => {
    setVerificationStats((prev) => ({ ...prev, totalClaims: claims.length }));
    if (claims.length > 0) {
      setSelectedClaim(claims[0].text);
      // Auto-switch to evidence tab
      setActiveTab("evidence");
    }
  };

  const handleEvidenceSelected = (evidence: Evidence) => {
    setSelectedEvidence(evidence);
    setVerificationStats((prev) => ({ ...prev, evidenceSources: prev.evidenceSources + 1 }));
    // Auto-switch to stance tab
    setActiveTab("stance");
  };

  const handleStanceResult = (result: StanceResult) => {
    setVerificationStats((prev) => ({ ...prev, stanceAnalyses: prev.stanceAnalyses + 1 }));
  };

  return (
    <DashboardLayout
      title="Verification Center"
      subtitle="Fact-checking and claim verification tools"
    >
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
                      ? "text-primary-600 border-primary-600 bg-primary-50 dark:bg-primary-900/20 dark:text-primary-300 dark:border-primary-400"
                      : "text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:border-gray-600"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Overview Tab */}
          {activeTab === "overview" && (
            <div className="space-y-6">
              {/* Stats Overview */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500 dark:text-slate-400">
                      Claims Extracted
                    </div>
                    <Search className="h-4 w-4 text-blue-500" />
                  </div>
                  <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                    {verificationStats.totalClaims}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-slate-400">
                    From analyzed text
                  </div>
                </Panel>

                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500 dark:text-slate-400">
                      Evidence Sources
                    </div>
                    <Target className="h-4 w-4 text-green-500" />
                  </div>
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {verificationStats.evidenceSources}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-slate-400">
                    Retrieved for verification
                  </div>
                </Panel>

                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500 dark:text-slate-400">Stance Analyses</div>
                    <Scale className="h-4 w-4 text-purple-500" />
                  </div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {verificationStats.stanceAnalyses}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-slate-400">
                    Completed classifications
                  </div>
                </Panel>

                <Panel>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm text-gray-500 dark:text-slate-400">
                      Credibility Checks
                    </div>
                    <Shield className="h-4 w-4 text-orange-500" />
                  </div>
                  <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                    {verificationStats.credibilityChecks}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-slate-400">
                    Source assessments
                  </div>
                </Panel>
              </div>

              {/* Feature Overview */}
              <Panel>
                <div className="flex items-center gap-3 mb-6">
                  <Shield className="h-6 w-6 text-blue-500" />
                  <h3 className={`${textStyles.h3} text-primary-600 dark:text-primary-400`}>
                    InfoTerminal v0.2.0 Verification Features
                  </h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className={`${cardStyles.base} p-4`}>
                    <div className="flex items-center gap-2 mb-2">
                      <Search className="h-5 w-5 text-blue-500" />
                      <h4 className={`${textStyles.body} font-medium`}>Claim Extraction</h4>
                    </div>
                    <p className={textStyles.body}>
                      Automatically extract verifiable claims from text using advanced NLP models
                    </p>
                  </div>

                  <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                    <div className="flex items-center gap-2 mb-2">
                      <Target className="h-5 w-5 text-green-500" />
                      <h4 className={`${textStyles.body} font-medium`}>Evidence Retrieval</h4>
                    </div>
                    <p className={textStyles.body}>
                      Find supporting evidence from multiple sources including web, news, and
                      academic papers
                    </p>
                  </div>

                  <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                    <div className="flex items-center gap-2 mb-2">
                      <Scale className="h-5 w-5 text-purple-500" />
                      <h4 className={`${textStyles.body} font-medium`}>Stance Classification</h4>
                    </div>
                    <p className={textStyles.body}>
                      Classify whether evidence supports, contradicts, or is neutral toward claims
                    </p>
                  </div>

                  <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                    <div className="flex items-center gap-2 mb-2">
                      <Shield className="h-5 w-5 text-orange-500" />
                      <h4 className={`${textStyles.body} font-medium`}>Source Credibility</h4>
                    </div>
                    <p className={textStyles.body}>
                      Assess the credibility and bias of information sources automatically
                    </p>
                  </div>
                </div>
              </Panel>

              {/* Workflow Guide */}
              <Panel>
                <h3 className={`${textStyles.h3} mb-4`}>Verification Workflow</h3>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-600 rounded-full text-sm font-medium">
                      1
                    </div>
                    <div>
                      <h4 className={`${textStyles.body} font-medium`}>Extract Claims</h4>
                      <p className={textStyles.bodySmall}>
                        Paste or type text to automatically identify verifiable claims
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-green-100 text-green-600 rounded-full text-sm font-medium">
                      2
                    </div>
                    <div>
                      <h4 className={`${textStyles.body} font-medium`}>Find Evidence</h4>
                      <p className={textStyles.bodySmall}>
                        Search for supporting or contradicting evidence from reliable sources
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-purple-100 text-purple-600 rounded-full text-sm font-medium">
                      3
                    </div>
                    <div>
                      <h4 className={`${textStyles.body} font-medium`}>Classify Stance</h4>
                      <p className={textStyles.bodySmall}>
                        Analyze whether evidence supports or contradicts the claim
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-orange-100 text-orange-600 rounded-full text-sm font-medium">
                      4
                    </div>
                    <div>
                      <h4 className={`${textStyles.body} font-medium`}>Check Credibility</h4>
                      <p className={textStyles.bodySmall}>
                        Evaluate the reliability and bias of information sources
                      </p>
                    </div>
                  </div>
                </div>
              </Panel>
            </div>
          )}

          {/* Extract Claims Tab */}
          {activeTab === "extract" && <ClaimExtractor onClaimsExtracted={handleClaimsExtracted} />}

          {/* Find Evidence Tab */}
          {activeTab === "evidence" && (
            <EvidenceViewer claim={selectedClaim} onStanceClassification={handleEvidenceSelected} />
          )}

          {/* Classify Stance Tab */}
          {activeTab === "stance" && (
            <StanceClassifier
              claim={selectedClaim}
              evidence={selectedEvidence}
              onStanceResult={handleStanceResult}
            />
          )}

          {/* Check Credibility Tab */}
          {activeTab === "credibility" && (
            <CredibilityDashboard sourceUrl={selectedEvidence?.source_url} />
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
