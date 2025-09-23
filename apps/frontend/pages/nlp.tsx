import { useState, useEffect } from "react";
import { AlertCircle, RefreshCw } from 'lucide-react';
import DashboardLayout from "@/components/layout/DashboardLayout";
import { getApis } from "@/lib/config";
import { DOMAINS, EXAMPLE_TEXTS } from '@/lib/nlp-domains';
import {
  NLPDomainSelector,
  NLPTextInput,
  NLPResultsPanel,
  NLPSidebar,
  NLPLegalAnalysis,
  Domain,
  NLPTab,
  NERResponse,
  SummaryResponse
} from '@/components/nlp/panels';

export default function ConsolidatedNLPPage() {
  const { DOC_ENTITIES_API } = getApis();
  const [activeDomain, setActiveDomain] = useState<Domain>('general');
  const [activeTab, setActiveTab] = useState<NLPTab>('entities');
  const [inputText, setInputText] = useState("");
  const [nerResult, setNerResult] = useState<NERResponse | null>(null);
  const [summaryResult, setSummaryResult] = useState<SummaryResponse | null>(null);
  const [sentimentResult, setSentimentResult] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  const currentDomain = DOMAINS.find(d => d.id === activeDomain);
  const currentExamples = EXAMPLE_TEXTS[activeDomain] || EXAMPLE_TEXTS.general;

  const checkHealth = async () => {
    try {
      const response = await fetch(`${DOC_ENTITIES_API}/healthz`);
      setIsHealthy(response.ok);
    } catch {
      setIsHealthy(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, [DOC_ENTITIES_API]);

  const callNER = async () => {
    if (!inputText.trim()) return;
    
    setIsLoading(true);
    setError("");
    setNerResult(null);

    try {
      const response = await fetch(`${DOC_ENTITIES_API}/ner`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          text: inputText, 
          domain: activeDomain 
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const result = await response.json();
      setNerResult(result);
      setActiveTab('entities');
    } catch (e: any) {
      setIsHealthy(false);
      setError("NLP service is not available");
    } finally {
      setIsLoading(false);
    }
  };

  const callSummarize = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    setError("");
    setSummaryResult(null);

    try {
      const response = await fetch(`${DOC_ENTITIES_API}/summary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          text: inputText, 
          domain: activeDomain 
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const result = await response.json();
      setSummaryResult(result);
      setActiveTab('summary');
    } catch (e: any) {
      setIsHealthy(false);
      setError("NLP service is not available");
    } finally {
      setIsLoading(false);
    }
  };

  const callSentiment = async () => {
    setActiveTab('sentiment');
  };

  const copyToClipboard = () => {
    const data = JSON.stringify({ entities: nerResult, summary: summaryResult }, null, 2);
    navigator.clipboard.writeText(data);
  };

  const exportResults = () => {
    const data = {
      input_text: inputText,
      domain: activeDomain,
      entities: nerResult,
      summary: summaryResult,
      timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nlp-analysis-${activeDomain}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <DashboardLayout title="Natural Language Processing" subtitle="Domain-specific text analysis and intelligence extraction">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Health Status */}
        {isHealthy === false && (
          <div className="p-4 rounded-lg bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-900/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertCircle size={20} className="text-red-600 dark:text-red-400" />
                <div>
                  <p className="text-sm font-medium text-red-800 dark:text-red-300">NLP Service Unavailable</p>
                  <p className="text-xs text-red-600 dark:text-red-400">Make sure the doc-entities container is running</p>
                </div>
              </div>
              <button 
                onClick={checkHealth}
                className="inline-flex items-center gap-2 px-3 py-1 text-sm font-medium text-red-700 bg-red-100 rounded-lg hover:bg-red-200"
              >
                <RefreshCw size={14} />
                Retry
              </button>
            </div>
          </div>
        )}

        {/* Domain Selection */}
        <NLPDomainSelector
          domains={DOMAINS}
          activeDomain={activeDomain}
          onDomainChange={setActiveDomain}
        />

        {/* Domain-specific content */}
        {activeDomain === 'legal' ? (
          <NLPLegalAnalysis />
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Input and Results */}
            <div className="lg:col-span-2 space-y-6">
              <NLPTextInput
                inputText={inputText}
                onInputTextChange={setInputText}
                currentDomain={currentDomain}
                currentExamples={currentExamples}
                isLoading={isLoading}
                activeTab={activeTab}
                onExtractEntities={callNER}
                onSummarize={callSummarize}
                onSentiment={callSentiment}
              />

              <NLPResultsPanel
                activeTab={activeTab}
                onTabChange={setActiveTab}
                currentDomain={currentDomain}
                inputText={inputText}
                nerResult={nerResult}
                summaryResult={summaryResult}
                sentimentResult={sentimentResult}
                error={error}
                onCopyResults={copyToClipboard}
                onExportResults={exportResults}
              />
            </div>

            {/* Sidebar */}
            <NLPSidebar
              isHealthy={isHealthy}
              currentDomain={currentDomain}
              nerResult={nerResult}
              summaryResult={summaryResult}
              inputText={inputText}
            />
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
