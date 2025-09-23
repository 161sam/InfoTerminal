import { useState } from 'react';
import { MessageSquare, Monitor, Bot, Settings } from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { isAgentEnabled } from '@/lib/config';
import { AGENT_CAPABILITIES } from '@/lib/agent-capabilities';
import { inputStyles, buttonStyles, textStyles, cardStyles, statusStyles, compose } from '@/styles/design-tokens';
import {
  AgentChatPanel,
  AgentManagementPanel
} from '@/components/agents/panels';

export default function ConsolidatedAgentPage() {
  const [activeTab, setActiveTab] = useState<string>('interaction');
  const agentEnabled = isAgentEnabled();

  if (!agentEnabled) {
    return (
      <DashboardLayout 
        title="Agent Platform" 
        subtitle="AI agent services are currently disabled"
      >
        <div className={`${cardStyles.base} ${cardStyles.padding}`}>
          <div className="flex flex-col items-center justify-center py-12">
            <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-full mb-4">
              <Bot className="h-12 w-12 text-gray-400 dark:text-gray-500" />
            </div>
            <h3 className={`${textStyles.h3} mb-2`}>Agent Services Not Available</h3>
            <p className={`${textStyles.body} text-center max-w-md mb-4`}>
              Agent services are currently disabled. Enable them by setting NEXT_PUBLIC_FEATURE_AGENT=1 
              in your environment configuration.
            </p>
            <button className={compose.button('secondary')}>
              <Settings className="h-4 w-4 mr-2" />
              Configure Services
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const tabs = [
    { id: 'interaction', label: 'Agent Interaction', icon: MessageSquare },
    { id: 'management', label: 'Agent Management', icon: Monitor }
  ];

  return (
    <DashboardLayout
      title="Agent Platform"
      subtitle="AI-powered investigation and analysis platform"
    >
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="rounded-lg border border-primary-200 bg-primary-50 p-4 text-sm text-gray-800 shadow-sm">
          <p className="font-semibold">New: single-turn MVP chat</p>
          <p className="mt-1">
            Need the lightweight mocked agent demo from Wave 4?{' '}
            <a href="/agent/mvp" className="text-primary-700 underline">
              Open the MVP chat interface
            </a>{' '}
            to trigger the mocked tool governance flow.
          </p>
        </div>

        {/* Main Tab Navigation */}
        <div className="space-y-6">
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-2 border-b border-gray-200 dark:border-gray-800">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-t-lg border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'text-primary-600 border-primary-600 bg-primary-50 dark:bg-primary-900/20 dark:text-primary-300 dark:border-primary-400'
                      : 'text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:border-gray-600'
                  }`}
                >
                  <Icon size={16} />
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Agent Interaction Tab Content */}
          {activeTab === 'interaction' && (
            <div className="mt-6">
              <AgentChatPanel agentCapabilities={AGENT_CAPABILITIES} />
            </div>
          )}

          {/* Agent Management Tab Content */}
          {activeTab === 'management' && (
            <div className="mt-6">
              <AgentManagementPanel agentCapabilities={AGENT_CAPABILITIES} />
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
