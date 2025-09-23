import React from 'react';
import { Download, Trash2 } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import { Message, AgentCapability, AgentStatus } from './types';

interface AgentSessionPanelProps {
  messages: Message[];
  sessionId: string | null;
  selectedAgent: string;
  agentStatus: AgentStatus;
  agentCapabilities: AgentCapability[];
  onExportConversation: () => void;
  onClearConversation: () => void;
}

export default function AgentSessionPanel({ 
  messages, 
  sessionId, 
  selectedAgent, 
  agentStatus,
  agentCapabilities,
  onExportConversation,
  onClearConversation
}: AgentSessionPanelProps) {
  const currentCapability = agentCapabilities.find(c => c.id === selectedAgent);

  return (
    <Panel title="Session Management">
      <div className="space-y-3">
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-gray-600 dark:text-slate-400">Messages</span>
            <span className="font-medium text-gray-900 dark:text-slate-100">{messages.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600 dark:text-slate-400">Agent</span>
            <span className="font-medium text-gray-900 dark:text-slate-100">
              {currentCapability?.displayName || 'None'}
            </span>
          </div>
          {agentStatus.version && (
            <div className="flex items-center justify-between">
              <span className="text-gray-600 dark:text-slate-400">Version</span>
              <span className="font-mono text-xs text-gray-900 dark:text-slate-100">
                {agentStatus.version}
              </span>
            </div>
          )}
          {sessionId && (
            <div className="flex items-center justify-between">
              <span className="text-gray-600 dark:text-slate-400">Session ID</span>
              <span className="font-mono text-xs text-gray-900 dark:text-slate-100">
                {sessionId.slice(-8)}
              </span>
            </div>
          )}
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={onExportConversation}
            disabled={messages.length === 0}
            className="flex-1 px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700 disabled:opacity-50 flex items-center gap-2 justify-center"
          >
            <Download size={14} />
            Export
          </button>
          <button
            onClick={onClearConversation}
            disabled={messages.length === 0}
            className="flex-1 px-3 py-2 text-sm text-red-600 bg-red-50 rounded-lg hover:bg-red-100 dark:bg-red-900/20 dark:text-red-300 dark:hover:bg-red-900/30 disabled:opacity-50 flex items-center gap-2 justify-center"
          >
            <Trash2 size={14} />
            Clear
          </button>
        </div>
      </div>
    </Panel>
  );
}
