import { useState, useEffect } from "react";
import { 
  Brain, 
  FileText, 
  Users, 
  RefreshCw, 
  AlertCircle, 
  CheckCircle,
  Sparkles,
  Eye,
  Copy,
  Download
} from 'lucide-react';
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import { getApis } from "@/lib/config";

type NLPTab = 'entities' | 'summary' | 'sentiment';

interface EntityResult {
  text: string;
  label: string;
  start: number;
  end: number;
  confidence: number;
}

interface NERResponse {
  entities: EntityResult[];
  processing_time?: number;
}

interface SummaryResponse {
  summary: string;
  processing_time?: number;
}

const EXAMPLE_TEXTS = [
  {
    title: "Financial Report Sample",
    text: "ACME Corporation reported Q3 revenues of $2.4M, with CEO John Smith stating that the London office expansion contributed significantly to growth. The company's partnership with TechFlow Solutions has opened new markets in Europe."
  },
  {
    title: "News Article Sample", 
    text: "Berlin, Germany - The European Central Bank announced yesterday that inflation rates have stabilized at 2.1%. ECB President Christine Lagarde emphasized the importance of maintaining monetary policy stability across the eurozone."
  },
  {
    title: "Investigation Report",
    text: "Subject: Maria Rodriguez, DOB: 1985-03-15, last known address: 123 Main Street, New York. Email: m.rodriguez@example.com. Associated with Global Imports LLC and frequent transactions to Swiss bank account CH93 0076 2011 6238 5295 7."
  }
];

const ENTITY_COLORS: Record<string, string> = {
  'PERSON': 'bg-blue-100 text-blue-800 border-blue-200',
  'ORG': 'bg-green-100 text-green-800 border-green-200',
  'ORGANIZATION': 'bg-green-100 text-green-800 border-green-200',
  'GPE': 'bg-purple-100 text-purple-800 border-purple-200',
  'LOCATION': 'bg-purple-100 text-purple-800 border-purple-200',
  'MONEY': 'bg-yellow-100 text-yellow-800 border-yellow-200',
  'DATE': 'bg-orange-100 text-orange-800 border-orange-200',
  'EMAIL': 'bg-pink-100 text-pink-800 border-pink-200',
  'DEFAULT': 'bg-gray-100 text-gray-800 border-gray-200'
};

export default function NLPPage() {
  const { DOC_ENTITIES_API } = getApis();
  const [activeTab, setActiveTab] = useState<NLPTab>('entities');
  const [inputText, setInputText] = useState("");
  const [nerResult, setNerResult] = useState<NERResponse | null>(null);
  const [summaryResult, setSummaryResult] = useState<SummaryResponse | null>(null);
  const [sentimentResult, setSentimentResult] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

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
        body: JSON.stringify({ text: inputText })
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
        body: JSON.stringify({ text: inputText })
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
    // Placeholder for sentiment analysis
    setActiveTab('sentiment');
  };

  const highlightEntities = (text: string, entities: EntityResult[]) => {
    if (!entities?.length) return text;

    const sortedEntities = [...entities].sort((a, b) => a.start - b.start);
    let result = [];
    let lastEnd = 0;

    sortedEntities.forEach((entity, index) => {
      // Add text before entity
      if (entity.start > lastEnd) {
        result.push(text.slice(lastEnd, entity.start));
      }

      // Add highlighted entity
      const colorClass = ENTITY_COLORS[entity.label] || ENTITY_COLORS.DEFAULT;
      result.push(
        <span
          key={index}
          className={`px-2 py-1 rounded-md border ${colorClass} font-medium`}
          title={`${entity.label} (${Math.round(entity.confidence * 100)}%)`}
        >
          {entity.text}
        </span>
      );

      lastEnd = entity.end;
    });

    // Add remaining text
    if (lastEnd < text.length) {
      result.push(text.slice(lastEnd));
    }

    return result;
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const exportResults = () => {
    const data = {
      input_text: inputText,
      entities: nerResult,
      summary: summaryResult,
      timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'nlp-analysis.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <DashboardLayout title="Natural Language Processing" subtitle="Extract insights from text with AI">
      <div className="max-w-6xl mx-auto space-y-6">
        
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Input Panel */}
          <div className="lg:col-span-2 space-y-6">
            <Panel title="Text Input">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                    Enter text to analyze
                  </label>
                  <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    rows={8}
                    className="w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    placeholder="Paste your text here for analysis..."
                  />
                  <div className="mt-2 flex items-center justify-between text-sm text-gray-500">
                    <span>{inputText.length} characters</span>
                    <span>{inputText.trim().split(/\s+/).filter(w => w).length} words</span>
                  </div>
                </div>

                {/* Example texts */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                    Or try these examples:
                  </label>
                  <div className="grid grid-cols-1 gap-2">
                    {EXAMPLE_TEXTS.map((example, index) => (
                      <button
                        key={index}
                        onClick={() => setInputText(example.text)}
                        className="p-3 text-left rounded-lg border border-gray-200 hover:border-gray-300 hover:bg-gray-50 dark:border-gray-700 dark:hover:border-gray-600 dark:hover:bg-gray-800 transition-colors"
                      >
                        <div className="font-medium text-sm text-gray-900 dark:text-slate-100">{example.title}</div>
                        <div className="text-xs text-gray-500 dark:text-slate-400 mt-1 truncate">
                          {example.text.slice(0, 100)}...
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Action buttons */}
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={callNER}
                    disabled={!inputText.trim() || isLoading}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading && activeTab === 'entities' ? (
                      <RefreshCw size={16} className="animate-spin" />
                    ) : (
                      <Users size={16} />
                    )}
                    Extract Entities
                  </button>
                  
                  <button
                    onClick={callSummarize}
                    disabled={!inputText.trim() || isLoading}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading && activeTab === 'summary' ? (
                      <RefreshCw size={16} className="animate-spin" />
                    ) : (
                      <FileText size={16} />
                    )}
                    Summarize
                  </button>

                  <button
                    onClick={callSentiment}
                    disabled={!inputText.trim() || isLoading}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Sparkles size={16} />
                    Sentiment
                  </button>
                </div>
              </div>
            </Panel>

            {/* Results Panel */}
            <Panel>
              <div className="mb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <h3 className="text-lg font-semibold">Analysis Results</h3>
                    {(nerResult || summaryResult) && (
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => copyToClipboard(JSON.stringify({ entities: nerResult, summary: summaryResult }, null, 2))}
                          className="p-1 text-gray-500 hover:text-gray-700 rounded"
                        >
                          <Copy size={16} />
                        </button>
                        <button
                          onClick={exportResults}
                          className="p-1 text-gray-500 hover:text-gray-700 rounded"
                        >
                          <Download size={16} />
                        </button>
                      </div>
                    )}
                  </div>
                  
                  {/* Tab navigation */}
                  <div className="flex bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
                    {[
                      { id: 'entities' as NLPTab, label: 'Entities', icon: Users },
                      { id: 'summary' as NLPTab, label: 'Summary', icon: FileText },
                      { id: 'sentiment' as NLPTab, label: 'Sentiment', icon: Sparkles }
                    ].map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`inline-flex items-center gap-2 px-3 py-1 text-sm rounded-md transition-colors ${
                          activeTab === tab.id
                            ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-slate-100 shadow-sm'
                            : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
                        }`}
                      >
                        <tab.icon size={14} />
                        {tab.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {error && (
                <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300">
                  {error}
                </div>
              )}

              {/* Entity Results */}
              {activeTab === 'entities' && (
                <div className="space-y-4">
                  {nerResult ? (
                    <>
                      {/* Highlighted text */}
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-slate-100 mb-2">Highlighted Text</h4>
                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border text-sm leading-relaxed">
                          {highlightEntities(inputText, nerResult.entities)}
                        </div>
                      </div>

                      {/* Entity list */}
                      {nerResult.entities?.length > 0 && (
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-slate-100 mb-2">
                            Detected Entities ({nerResult.entities.length})
                          </h4>
                          <div className="space-y-2">
                            {nerResult.entities.map((entity, index) => (
                              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                <div className="flex items-center gap-3">
                                  <span className={`px-2 py-1 rounded text-xs font-medium border ${ENTITY_COLORS[entity.label] || ENTITY_COLORS.DEFAULT}`}>
                                    {entity.label}
                                  </span>
                                  <span className="font-medium text-gray-900 dark:text-slate-100">{entity.text}</span>
                                </div>
                                <div className="flex items-center gap-2 text-sm text-gray-500">
                                  <span>{Math.round(entity.confidence * 100)}%</span>
                                  <span className="text-xs">({entity.start}-{entity.end})</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {nerResult.processing_time && (
                        <div className="text-xs text-gray-500">
                          Processing time: {nerResult.processing_time}ms
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="text-center py-8 text-gray-500 dark:text-slate-400">
                      <Users size={48} className="mx-auto mb-2 opacity-50" />
                      <p>Click "Extract Entities" to analyze your text</p>
                    </div>
                  )}
                </div>
              )}

              {/* Summary Results */}
              {activeTab === 'summary' && (
                <div className="space-y-4">
                  {summaryResult ? (
                    <>
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-slate-100 mb-2">Generated Summary</h4>
                        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
                          <p className="text-gray-900 dark:text-slate-100 leading-relaxed">{summaryResult.summary}</p>
                        </div>
                      </div>

                      {summaryResult.processing_time && (
                        <div className="text-xs text-gray-500">
                          Processing time: {summaryResult.processing_time}ms
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="text-center py-8 text-gray-500 dark:text-slate-400">
                      <FileText size={48} className="mx-auto mb-2 opacity-50" />
                      <p>Click "Summarize" to generate a summary</p>
                    </div>
                  )}
                </div>
              )}

              {/* Sentiment Results */}
              {activeTab === 'sentiment' && (
                <div className="text-center py-8 text-gray-500 dark:text-slate-400">
                  <Sparkles size={48} className="mx-auto mb-2 opacity-50" />
                  <p>Sentiment analysis coming soon</p>
                </div>
              )}
            </Panel>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Service Status */}
            <Panel title="Service Status">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-slate-400">NLP Service</span>
                  <div className="flex items-center gap-2">
                    {isHealthy === true ? (
                      <CheckCircle size={16} className="text-green-500" />
                    ) : isHealthy === false ? (
                      <AlertCircle size={16} className="text-red-500" />
                    ) : (
                      <RefreshCw size={16} className="text-gray-400 animate-spin" />
                    )}
                    <span className={`text-sm font-medium ${
                      isHealthy === true ? 'text-green-600' :
                      isHealthy === false ? 'text-red-600' :
                      'text-gray-600'
                    }`}>
                      {isHealthy === true ? 'Online' : isHealthy === false ? 'Offline' : 'Checking...'}
                    </span>
                  </div>
                </div>
              </div>
            </Panel>

            {/* Entity Legend */}
            <Panel title="Entity Types">
              <div className="space-y-2">
                {Object.entries(ENTITY_COLORS).filter(([key]) => key !== 'DEFAULT').map(([type, colorClass]) => (
                  <div key={type} className="flex items-center gap-2">
                    <span className={`px-2 py-1 rounded text-xs font-medium border ${colorClass}`}>
                      {type}
                    </span>
                  </div>
                ))}
              </div>
            </Panel>

            {/* Quick Stats */}
            {(nerResult || summaryResult) && (
              <Panel title="Analysis Stats">
                <div className="space-y-2 text-sm">
                  {nerResult && (
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 dark:text-slate-400">Entities Found</span>
                      <span className="font-medium text-gray-900 dark:text-slate-100">{nerResult.entities?.length || 0}</span>
                    </div>
                  )}
                  {summaryResult && (
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 dark:text-slate-400">Summary Length</span>
                      <span className="font-medium text-gray-900 dark:text-slate-100">{summaryResult.summary?.length || 0} chars</span>
                    </div>
                  )}
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-slate-400">Input Length</span>
                    <span className="font-medium text-gray-900 dark:text-slate-100">{inputText.length} chars</span>
                  </div>
                </div>
              </Panel>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
