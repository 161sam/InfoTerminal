import { useState, useEffect, useRef } from 'react';
import { 
  Send, 
  Bot, 
  User, 
  AlertCircle, 
  RefreshCw, 
  Play, 
  Cpu, 
  MessageSquare,
  Settings,
  History,
  Sparkles
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { getApis } from '@/lib/config';

type Message = { 
  role: 'user' | 'assistant' | 'system'; 
  content: string; 
  steps?: any; 
  references?: any;
  timestamp: Date;
  id: string;
};

type PlaybookAction = {
  id: string;
  name: string;
  displayName: string;
  description: string;
  icon: React.ComponentType<{ size?: number }>;
  color: string;
};

const PLAYBOOKS: PlaybookAction[] = [
  {
    id: 'InvestigatePerson',
    name: 'InvestigatePerson',
    displayName: 'Person Investigation',
    description: 'Deep dive into person connections and activities',
    icon: User,
    color: 'blue'
  },
  {
    id: 'FinancialRiskAssistant',
    name: 'FinancialRiskAssistant',
    displayName: 'Financial Risk Analysis',
    description: 'Analyze financial risks and patterns',
    icon: Cpu,
    color: 'amber'
  }
];

export default function AgentPage() {
  const { AGENT_API } = getApis();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [workflowStatus, setWorkflowStatus] = useState<string | null>(null);
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [playbookLoading, setPlaybookLoading] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const n8nConfigured = Boolean(process.env.NEXT_PUBLIC_N8N_URL);

  const checkHealth = async () => {
    try {
      const response = await fetch(`${AGENT_API}/healthz`);
      setIsHealthy(response.ok);
    } catch {
      setIsHealthy(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, [AGENT_API]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    const body = { 
      messages: [...messages.map(({ steps, references, timestamp, id, ...m }) => m), 
      { role: 'user', content: inputText }] 
    };

    try {
      const response = await fetch(`${AGENT_API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      const assistantMessage: Message = {
        id: Date.now().toString() + '_assistant',
        role: 'assistant',
        content: data.reply || 'No response received',
        steps: data.steps,
        references: data.references,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      setIsHealthy(false);
      const errorMessage: Message = {
        id: Date.now().toString() + '_error',
        role: 'system',
        content: error.message || 'Agent service is not reachable',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const runPlaybook = async (playbook: PlaybookAction) => {
    setPlaybookLoading(playbook.id);
    try {
      const response = await fetch(`${AGENT_API}/playbooks/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: playbook.name, params: { q: inputText } }),
      });
      
      const data = await response.json();
      const systemMessage: Message = {
        id: Date.now().toString() + '_playbook',
        role: 'system',
        content: `${playbook.displayName} completed: ${JSON.stringify(data)}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, systemMessage]);
    } catch (error: any) {
      setIsHealthy(false);
      const errorMessage: Message = {
        id: Date.now().toString() + '_playbook_error',
        role: 'system',
        content: `${playbook.displayName} failed: ${error.message || 'Unknown error'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setPlaybookLoading(null);
    }
  };

  const runWorkflow = async () => {
    if (!n8nConfigured) {
      setWorkflowStatus('n8n not configured');
      return;
    }

    setWorkflowStatus('starting...');
    try {
      const response = await fetch(`${AGENT_API}/workflows/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      
      const data = await response.json();
      const status = data.runId ? `Started workflow: ${data.runId}` : 'Workflow completed';
      setWorkflowStatus(status);
      
      const systemMessage: Message = {
        id: Date.now().toString() + '_workflow',
        role: 'system',
        content: `Workflow: ${JSON.stringify(data)}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, systemMessage]);
    } catch (error: any) {
      const errorMsg = error.message || 'Workflow execution failed';
      setWorkflowStatus(errorMsg);
      setIsHealthy(false);
      
      const errorMessage: Message = {
        id: Date.now().toString() + '_workflow_error',
        role: 'system',
        content: errorMsg,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <DashboardLayout title="Investigation Agent" subtitle="Intelligent conversation with your data">
      <div className="flex flex-col h-[calc(100vh-12rem)] max-w-6xl mx-auto">
        
        {/* Health Status Banner */}
        {isHealthy === false && (
          <div className="mb-4 p-4 rounded-lg bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-900/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertCircle size={20} className="text-red-600 dark:text-red-400" />
                <div>
                  <p className="text-sm font-medium text-red-800 dark:text-red-300">Agent Service Unavailable</p>
                  <p className="text-xs text-red-600 dark:text-red-400">Make sure the agent-connector container is running</p>
                </div>
              </div>
              <button 
                onClick={checkHealth}
                className="inline-flex items-center gap-2 px-3 py-1 text-sm font-medium text-red-700 bg-red-100 rounded-lg hover:bg-red-200 dark:bg-red-900/50 dark:text-red-300 dark:hover:bg-red-900/70"
              >
                <RefreshCw size={14} />
                Retry
              </button>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 min-h-0">
          
          {/* Main Chat Panel */}
          <div className="lg:col-span-3 flex flex-col">
            <Panel className="flex-1 flex flex-col min-h-0">
              
              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
                {messages.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-center">
                    <Bot size={48} className="text-gray-400 dark:text-slate-500 mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">
                      Welcome to the Investigation Agent
                    </h3>
                    <p className="text-gray-500 dark:text-slate-400 max-w-md">
                      Start a conversation to investigate your data, run analysis playbooks, or ask questions about entities and connections.
                    </p>
                  </div>
                ) : (
                  <>
                    {messages.map((message) => (
                      <MessageBubble key={message.id} message={message} />
                    ))}
                    {isLoading && (
                      <div className="flex items-center gap-3 text-gray-500">
                        <div className="flex items-center justify-center w-8 h-8 bg-gray-100 rounded-full dark:bg-gray-800">
                          <Bot size={16} />
                        </div>
                        <div className="flex items-center gap-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse animation-delay-200"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse animation-delay-400"></div>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </>
                )}
              </div>

              {/* Input Area */}
              <div className="border-t border-gray-200 dark:border-gray-700 p-4">
                <div className="flex gap-2">
                  <div className="flex-1">
                    <textarea
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Ask me anything about your data..."
                      className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 resize-none"
                      rows={2}
                      disabled={isLoading}
                    />
                  </div>
                  <button
                    onClick={sendMessage}
                    disabled={!inputText.trim() || isLoading}
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    <Send size={16} />
                  </button>
                </div>
              </div>
            </Panel>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Quick Actions */}
            <Panel title="Analysis Playbooks">
              <div className="space-y-3">
                {PLAYBOOKS.map((playbook) => (
                  <button
                    key={playbook.id}
                    onClick={() => runPlaybook(playbook)}
                    disabled={playbookLoading === playbook.id}
                    className="w-full p-3 text-left rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg ${playbook.color === 'blue' ? 'bg-blue-100 text-blue-600' : 'bg-amber-100 text-amber-600'}`}>
                        <playbook.icon size={16} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 dark:text-slate-100 text-sm">
                          {playbook.displayName}
                        </h4>
                        <p className="text-xs text-gray-500 dark:text-slate-400 mt-1">
                          {playbook.description}
                        </p>
                        {playbookLoading === playbook.id && (
                          <div className="flex items-center gap-2 mt-2">
                            <RefreshCw size={12} className="animate-spin" />
                            <span className="text-xs text-blue-600">Running...</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </Panel>

            {/* Workflow Control */}
            {n8nConfigured && (
              <Panel title="Workflow Automation">
                <button
                  onClick={runWorkflow}
                  className="w-full p-3 text-left rounded-lg bg-purple-50 border border-purple-200 hover:bg-purple-100 dark:bg-purple-900/20 dark:border-purple-900/30 dark:hover:bg-purple-900/30 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-purple-100 text-purple-600 rounded-lg dark:bg-purple-900/50 dark:text-purple-400">
                      <Sparkles size={16} />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-slate-100 text-sm">
                        Trigger n8n Workflow
                      </h4>
                      <p className="text-xs text-gray-500 dark:text-slate-400">
                        Run automated data pipeline
                      </p>
                    </div>
                  </div>
                </button>
                {workflowStatus && (
                  <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-800 rounded text-xs text-gray-600 dark:text-slate-300">
                    Status: {workflowStatus}
                  </div>
                )}
              </Panel>
            )}

            {/* Chat History */}
            <Panel title="Session Info">
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Messages</span>
                  <span className="font-medium text-gray-900 dark:text-slate-100">{messages.length}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Agent Status</span>
                  <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                    isHealthy === true ? 'bg-green-100 text-green-800' :
                    isHealthy === false ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {isHealthy === true ? 'Online' : isHealthy === false ? 'Offline' : 'Unknown'}
                  </span>
                </div>
                {messages.length > 0 && (
                  <button
                    onClick={() => setMessages([])}
                    className="w-full mt-3 px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                  >
                    Clear History
                  </button>
                )}
              </div>
            </Panel>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  
  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className={`flex items-center justify-center w-8 h-8 rounded-full flex-shrink-0 ${
          isSystem ? 'bg-orange-100 text-orange-600' : 'bg-blue-100 text-blue-600'
        }`}>
          {isSystem ? <Settings size={16} /> : <Bot size={16} />}
        </div>
      )}
      
      <div className={`max-w-3xl ${isUser ? 'order-first' : ''}`}>
        <div className={`p-3 rounded-lg ${
          isUser 
            ? 'bg-primary-600 text-white'
            : isSystem
            ? 'bg-orange-50 text-orange-900 border border-orange-200 dark:bg-orange-900/20 dark:text-orange-300 dark:border-orange-900/30'
            : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100'
        }`}>
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>
        
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-slate-400">
          <span>{message.timestamp.toLocaleTimeString()}</span>
          {message.role === 'assistant' && (
            <span className="inline-flex items-center gap-1">
              <MessageSquare size={12} />
              Assistant
            </span>
          )}
        </div>

        {/* Steps and References */}
        {(message.steps || message.references) && (
          <div className="mt-2 space-y-2">
            {message.steps && (
              <details className="text-xs">
                <summary className="cursor-pointer text-gray-600 dark:text-slate-400 hover:text-gray-800 dark:hover:text-slate-200">
                  View Steps
                </summary>
                <pre className="mt-1 p-2 bg-gray-50 dark:bg-gray-900 rounded text-xs overflow-auto">
                  {JSON.stringify(message.steps, null, 2)}
                </pre>
              </details>
            )}
            {message.references && (
              <details className="text-xs">
                <summary className="cursor-pointer text-gray-600 dark:text-slate-400 hover:text-gray-800 dark:hover:text-slate-200">
                  View References
                </summary>
                <pre className="mt-1 p-2 bg-gray-50 dark:bg-gray-900 rounded text-xs overflow-auto">
                  {JSON.stringify(message.references, null, 2)}
                </pre>
              </details>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex items-center justify-center w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex-shrink-0">
          <User size={16} />
        </div>
      )}
    </div>
  );
}
