import React from 'react';
import { Users, FileText, Sparkles, Copy, Download } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import NLPEntityHighlighter from './NLPEntityHighlighter';
import { 
  NLPTab, 
  DomainConfig, 
  NERResponse, 
  SummaryResponse, 
  ENTITY_COLORS 
} from './types';

interface NLPResultsPanelProps {
  activeTab: NLPTab;
  onTabChange: (tab: NLPTab) => void;
  currentDomain: DomainConfig | undefined;
  inputText: string;
  nerResult: NERResponse | null;
  summaryResult: SummaryResponse | null;
  sentimentResult: any | null;
  error: string;
  onCopyResults: () => void;
  onExportResults: () => void;
}

export default function NLPResultsPanel({
  activeTab,
  onTabChange,
  currentDomain,
  inputText,
  nerResult,
  summaryResult,
  sentimentResult,
  error,
  onCopyResults,
  onExportResults
}: NLPResultsPanelProps) {

  return (
    <Panel>
      <Tabs value={activeTab} onValueChange={onTabChange}>
        <div className="mb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h3 className="text-lg font-semibold">Analysis Results</h3>
              {currentDomain && (
                <div className="flex items-center gap-2">
                  <currentDomain.icon size={16} className="text-gray-500" />
                  <span className="text-sm text-gray-500">{currentDomain.name} Domain</span>
                </div>
              )}
              {(nerResult || summaryResult) && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={onCopyResults}
                    className="p-1 text-gray-500 hover:text-gray-700 rounded"
                    title="Copy results to clipboard"
                  >
                    <Copy size={16} />
                  </button>
                  <button
                    onClick={onExportResults}
                    className="p-1 text-gray-500 hover:text-gray-700 rounded"
                    title="Export results as JSON"
                  >
                    <Download size={16} />
                  </button>
                </div>
              )}
            </div>
            
            {/* Tab Navigation */}
            <TabsList>
              <TabsTrigger value="entities" icon={Users}>Entities</TabsTrigger>
              <TabsTrigger value="summary" icon={FileText}>Summary</TabsTrigger>
              <TabsTrigger value="sentiment" icon={Sparkles}>Sentiment</TabsTrigger>
            </TabsList>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300 mb-4">
            {error}
          </div>
        )}

        {/* Entity Results */}
        <TabsContent value="entities">
          <div className="space-y-4">
            {nerResult ? (
              <>
                {/* Highlighted text */}
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-slate-100 mb-2">Highlighted Text</h4>
                  <NLPEntityHighlighter 
                    text={inputText} 
                    entities={nerResult.entities} 
                  />
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
                <p>Click "Extract Entities" to analyze your {currentDomain?.name.toLowerCase()} text</p>
              </div>
            )}
          </div>
        </TabsContent>

        {/* Summary Results */}
        <TabsContent value="summary">
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
                <p>Click "Summarize" to generate a {currentDomain?.name.toLowerCase()} summary</p>
              </div>
            )}
          </div>
        </TabsContent>

        {/* Sentiment Results */}
        <TabsContent value="sentiment">
          <div className="text-center py-8 text-gray-500 dark:text-slate-400">
            <Sparkles size={48} className="mx-auto mb-2 opacity-50" />
            <p>Sentiment analysis for {currentDomain?.name.toLowerCase()} domain coming soon</p>
          </div>
        </TabsContent>
      </Tabs>
    </Panel>
  );
}
