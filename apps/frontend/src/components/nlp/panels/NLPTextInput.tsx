import React from "react";
import { Users, FileText, Sparkles } from "lucide-react";
import Panel from "@/components/layout/Panel";
import { LoadingSpinner } from "@/components/ui/loading";
import { Domain, DomainConfig, ExampleText, NLPTab } from "./types";

interface NLPTextInputProps {
  inputText: string;
  onInputTextChange: (text: string) => void;
  currentDomain: DomainConfig | undefined;
  currentExamples: ExampleText[];
  isLoading: boolean;
  activeTab: NLPTab;
  onExtractEntities: () => void;
  onSummarize: () => void;
  onSentiment: () => void;
}

export default function NLPTextInput({
  inputText,
  onInputTextChange,
  currentDomain,
  currentExamples,
  isLoading,
  activeTab,
  onExtractEntities,
  onSummarize,
  onSentiment,
}: NLPTextInputProps) {
  return (
    <Panel title="Text Input">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
            Enter text to analyze ({currentDomain?.name.toLowerCase()} domain)
          </label>
          <textarea
            value={inputText}
            onChange={(e) => onInputTextChange(e.target.value)}
            rows={8}
            className="w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            placeholder={`Paste your ${currentDomain?.name.toLowerCase()} text here for analysis...`}
          />
          <div className="mt-2 flex items-center justify-between text-sm text-gray-500">
            <span>{inputText.length} characters</span>
            <span>
              {
                inputText
                  .trim()
                  .split(/\s+/)
                  .filter((w) => w).length
              }{" "}
              words
            </span>
          </div>
        </div>

        {/* Domain-specific examples */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
            Or try these {currentDomain?.name.toLowerCase()} examples:
          </label>
          <div className="grid grid-cols-1 gap-2">
            {currentExamples.map((example, index) => (
              <button
                key={index}
                onClick={() => onInputTextChange(example.text)}
                className="p-3 text-left rounded-lg border border-gray-200 hover:border-gray-300 hover:bg-gray-50 dark:border-gray-700 dark:hover:border-gray-600 dark:hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-center gap-2 mb-1">
                  {currentDomain && <currentDomain.icon size={14} className="text-gray-500" />}
                  <div className="font-medium text-sm text-gray-900 dark:text-slate-100">
                    {example.title}
                  </div>
                </div>
                <div className="text-xs text-gray-500 dark:text-slate-400 truncate">
                  {example.text.slice(0, 120)}...
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex flex-wrap gap-3">
          <button
            onClick={onExtractEntities}
            disabled={!inputText.trim() || isLoading}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading && activeTab === "entities" ? (
              <LoadingSpinner size="sm" />
            ) : (
              <Users size={16} />
            )}
            Extract Entities
          </button>

          <button
            onClick={onSummarize}
            disabled={!inputText.trim() || isLoading}
            className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading && activeTab === "summary" ? (
              <LoadingSpinner size="sm" />
            ) : (
              <FileText size={16} />
            )}
            Summarize
          </button>

          <button
            onClick={onSentiment}
            disabled={!inputText.trim() || isLoading}
            className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Sparkles size={16} />
            Sentiment
          </button>
        </div>
      </div>
    </Panel>
  );
}
