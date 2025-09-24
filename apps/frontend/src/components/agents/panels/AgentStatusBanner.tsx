import React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";
import { AgentStatus } from "./types";

interface AgentStatusBannerProps {
  agentStatus: AgentStatus;
  onRetryHealth: () => void;
}

export default function AgentStatusBanner({ agentStatus, onRetryHealth }: AgentStatusBannerProps) {
  if (agentStatus.healthy !== false) {
    return null;
  }

  return (
    <div className="mb-4 p-4 rounded-lg bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-900/30">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <AlertCircle size={20} className="text-red-600 dark:text-red-400" />
          <div>
            <p className="text-sm font-medium text-red-800 dark:text-red-300">
              Agent Service Unavailable
            </p>
            <p className="text-xs text-red-600 dark:text-red-400">
              {agentStatus.lastCheck && `Last check: ${agentStatus.lastCheck.toLocaleTimeString()}`}
            </p>
          </div>
        </div>
        <button
          onClick={onRetryHealth}
          className="inline-flex items-center gap-2 px-3 py-1 text-sm font-medium text-red-700 bg-red-100 rounded-lg hover:bg-red-200 dark:bg-red-900/50 dark:text-red-300 dark:hover:bg-red-900/70"
        >
          <RefreshCw size={14} />
          Retry
        </button>
      </div>
    </div>
  );
}
