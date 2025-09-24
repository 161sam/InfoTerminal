import React from "react";
import { CheckCircle, AlertCircle } from "lucide-react";
import Panel from "@/components/layout/Panel";
import { LoadingSpinner } from "@/components/ui/loading";
import { DomainConfig, NERResponse, SummaryResponse, ENTITY_COLORS } from "./types";

interface NLPSidebarProps {
  isHealthy: boolean | null;
  currentDomain: DomainConfig | undefined;
  nerResult: NERResponse | null;
  summaryResult: SummaryResponse | null;
  inputText: string;
}

export default function NLPSidebar({
  isHealthy,
  currentDomain,
  nerResult,
  summaryResult,
  inputText,
}: NLPSidebarProps) {
  return (
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
                <LoadingSpinner size="sm" variant="default" />
              )}
              <span
                className={`text-sm font-medium ${
                  isHealthy === true
                    ? "text-green-600"
                    : isHealthy === false
                      ? "text-red-600"
                      : "text-gray-600"
                }`}
              >
                {isHealthy === true ? "Online" : isHealthy === false ? "Offline" : "Checking..."}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600 dark:text-slate-400">Active Domain</span>
            <span className="text-sm font-medium text-gray-900 dark:text-slate-100">
              {currentDomain?.name || "General"}
            </span>
          </div>
        </div>
      </Panel>

      {/* Entity Types */}
      <Panel title="Entity Types">
        <div className="space-y-2">
          {Object.entries(ENTITY_COLORS)
            .filter(([key]) => key !== "DEFAULT")
            .map(([type, colorClass]) => (
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
                <span className="font-medium text-gray-900 dark:text-slate-100">
                  {nerResult.entities?.length || 0}
                </span>
              </div>
            )}
            {summaryResult && (
              <div className="flex items-center justify-between">
                <span className="text-gray-600 dark:text-slate-400">Summary Length</span>
                <span className="font-medium text-gray-900 dark:text-slate-100">
                  {summaryResult.summary?.length || 0} chars
                </span>
              </div>
            )}
            <div className="flex items-center justify-between">
              <span className="text-gray-600 dark:text-slate-400">Input Length</span>
              <span className="font-medium text-gray-900 dark:text-slate-100">
                {inputText.length} chars
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600 dark:text-slate-400">Domain</span>
              <span className="font-medium text-gray-900 dark:text-slate-100">
                {currentDomain?.name}
              </span>
            </div>
          </div>
        </Panel>
      )}
    </div>
  );
}
