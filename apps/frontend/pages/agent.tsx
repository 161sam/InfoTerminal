import { useState, useEffect, useRef, useCallback } from 'react';
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
  Sparkles,
  Download,
  Trash2,
  Copy,
  Search,
  Network,
  Shield,
  MapPin,
  Clock,
  CheckCircle,
  Zap,
  ExternalLink,
  ChevronDown,
  ChevronRight
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { getApis } from '@/lib/config';

interface Message { 
  role: 'user' | 'assistant' | 'system'; 
  content: string; 
  steps?: ExecutionStep[]; 
  references?: any;
  timestamp: Date;
  id: string;
  agentType?: string;
  toolsUsed?: string[];
  confidence?: number;
  executionTime?: number;
}

interface ExecutionStep {
  type: string;
  tool: string;
  parameters: any;
  result: any;
  error?: string;
  timestamp: string;
}

interface AgentCapability {
  id: string;
  name: string;
  displayName: string;
  description: string;
  icon: LucideIcon;
  color: string;
  tools: string[];
}

interface AgentStatus {
  healthy: boolean;
  version?: string;
  capabilities?: string[];
  uptime?: number;
  lastCheck?: Date;
}

const AGENT_CAPABILITIES: AgentCapability[] = [
  {
    id: 'research_assistant',
    name: 'research_assistant',
    displayName: 'Research Assistant',
    description: 'Comprehensive research across multiple data sources and databases',
    icon: Search,
    color: 'blue',
    tools: ['web_search', 'database_query', 'document_analysis', 'fact_checking']
  },
  {
    id: 'graph_analyst', 
    name: 'graph_analyst',
    displayName: 'Graph Analyst',
    description: 'Network analysis, relationship mapping, and connection discovery',
    icon: Network,
    color: 'purple',
    tools: ['neo4j_query', 'network_analysis', 'path_finding', 'community_detection']
  },
  {
    id: 'security_analyst',
    name: 'security_analyst', 
    displayName: 'Security Analyst',
    description: 'Threat assessment, risk analysis, and security intelligence',
    icon: Shield,
    color: 'red',
    tools: ['threat_intel', 'vulnerability_scan', 'risk_assessment', 'iot_analysis']
  },
  {
    id: 'geospatial_analyst',
    name: 'geospatial_analyst',
    displayName: 'Geospatial Analyst', 
    description: 'Location intelligence, spatial analysis, and geographic insights',
    icon: MapPin,
    color: 'green',
    tools: ['gis_analysis', 'location_intel', 'spatial_query', 'route_analysis']
  },
  {
    id: 'InvestigatePerson',
    name: 'InvestigatePerson',
    displayName: 'Person Investigation',
    description: 'Deep person profiling, background checks, and social network analysis',
    icon: User,
    color: 'indigo',
    tools: ['social_media', 'public_records', 'network_mapping', 'background_check']
  },
  {
    id: 'FinancialRiskAssistant',
    name: 'FinancialRiskAssistant',
    displayName: 'Financial Risk Analysis',
    description: 'Financial pattern analysis, risk modeling, and compliance assessment',
    icon: Cpu,
    color: 'amber',
    tools: ['transaction_analysis', 'risk_modeling', 'compliance_check', 'fraud_detection']
  }
];

const CAPABILITY_STYLES = {
  blue: 'bg-blue-50 border-blue-200 text-blue-800 hover:bg-blue-100 dark:bg-blue-900/20 dark:border-blue-900/30 dark:text-blue-300',
  purple: 'bg-purple-50 border-purple-200 text-purple-800 hover:bg-purple-100 dark:bg-purple-900/20 dark:border-purple-900/30 dark:text-purple-300',
  red: 'bg-red-50 border-red-200 text-red-800 hover:bg-red-100 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300',
  green: 'bg-green-50 border-green-200 text-green-800 hover:bg-green-100 dark:bg-green-900/20 dark:border-green-900/30 dark:text-green-300',
  indigo: 'bg-indigo-50 border-indigo-200 text-indigo-800 hover:bg-indigo-100 dark:bg-indigo-900/20 dark:border-indigo-900/30 dark:text-indigo-300',
  amber: 'bg-amber-50 border-amber-200 text-amber-800 hover:bg-amber-100 dark:bg-amber-900/20 dark:border-amber-900/30 dark:text-amber-300'
};

export default function EnhancedAgentPage() {
  const { AGENT_API, DOC_ENTITIES_API } = getApis();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<string>('research_assistant');
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({ healthy: false });
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [showSteps, setShowSteps] = useState<{ [key: string]: boolean }>({});
  const [workflowStatus, setWorkflowStatus] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const n8nConfigured = Boolean(process.env.NEXT_PUBLIC_N8N_URL);

  // Enhanced health check with detailed status
  const checkAgentHealth = useCallback(async () => {
    try {
      const response = await fetch(`${AGENT_API}/healthz`);
      const data = response.ok ? await response.json() : {};
      
      setAgentStatus({
        healthy: response.ok,
        version: data.version || 'unknown',
        capabilities: data.capabilities || [],
        uptime: data.uptime,
        lastCheck: new Date()
      });
    } catch {
      setAgentStatus({ 
        healthy: false, 
        lastCheck: new Date() 
      });
    }
  }, [AGENT_API]);

  useEffect(() => {
    checkAgentHealth();
    const interval = setInterval(checkAgentHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, [checkAgentHealth]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Generate unique session ID
  const generateSessionId = useCallback(() => {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }, []);

  // Enhanced message sending with better error handling and agent type support
  const sendMessage = useCallback(async () => {
    if (!inputText.trim() || isLoading) return;

    const currentSessionId = sessionId || generateSessionId();
    if (!sessionId) setSessionId(currentSessionId);

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: inputText,
      timestamp: new Date(),
      agentType: selectedAgent
    };

    setMessages(prev => [...prev, userMessage]);
    const messageContent = inputText;
    setInputText('');
    setIsLoading(true);

    try {
      const requestBody = {
        messages: [...messages.map(({ steps, references, timestamp, id, toolsUsed, confidence, executionTime, ...m }) => m), 
                   { role: 'user', content: messageContent }],
        agent_type: selectedAgent,
        session_id: currentSessionId,
        max_iterations: 10,
        include_steps: true,
        include_references: true
      };

      const startTime = Date.now();
      const response = await fetch(`${AGENT_API}/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Agent service error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      const executionTime = (Date.now() - startTime) / 1000;

      const assistantMessage: Message = {
        id: `assistant_${Date.now()}`,
        role: 'assistant',
        content: data.reply || data.response || 'No response received',
        steps: data.steps || [],
        references: data.references,
        timestamp: new Date(),
        agentType: selectedAgent,
        toolsUsed: data.tools_used || [],
        confidence: data.confidence,
        executionTime
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update agent status on successful response
      if (!agentStatus.healthy) {
        setAgentStatus(prev => ({ ...prev, healthy: true, lastCheck: new Date() }));
      }

    } catch (error: any) {
      console.error('Agent communication error:', error);
      
      setAgentStatus(prev => ({ ...prev, healthy: false, lastCheck: new Date() }));
      
      const errorMessage: Message = {
        id: `error_${Date.now()}`,
        role: 'system',
        content: `Communication error: ${error.message || 'Agent service unavailable'}. Please check service status and try again.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }, [inputText, isLoading, sessionId, selectedAgent, messages, AGENT_API, agentStatus.healthy, generateSessionId]);

  // Run specific capability with enhanced parameters
  const runCapability = useCallback(async (capability: AgentCapability) => {
    if (isLoading) return;
    
    setIsLoading(true);
    const currentSessionId = sessionId || generateSessionId();
    if (!sessionId) setSessionId(currentSessionId);

    try {
      const response = await fetch(`${AGENT_API}/capabilities/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          capability: capability.id,
          agent_type: capability.name,
          context: inputText || 'General analysis',
          session_id: currentSessionId,
          tools: capability.tools
        }),
      });
      
      const data = await response.json();
      const systemMessage: Message = {
        id: `capability_${Date.now()}`,
        role: 'system',
        content: `${capability.displayName} analysis completed. Results: ${data.result || JSON.stringify(data)}`,
        steps: data.steps,
        timestamp: new Date(),
        agentType: capability.name,
        toolsUsed: data.tools_used || capability.tools
      };
      setMessages(prev => [...prev, systemMessage]);
    } catch (error: any) {
      const errorMessage: Message = {
        id: `capability_error_${Date.now()}`,
        role: 'system',
        content: `${capability.displayName} failed: ${error.message || 'Unknown error'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputText, isLoading, sessionId, AGENT_API, generateSessionId]);

  // Enhanced workflow execution
  const runWorkflow = async () => {
    if (!n8nConfigured) {
      setWorkflowStatus('n8n not configured');
      return;
    }

    setWorkflowStatus('initializing...');
    try {
      const response = await fetch(`${AGENT_API}/workflows/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          context: inputText || 'Manual trigger',
          session_id: sessionId,
          agent_type: selectedAgent
        }),
      });
      
      const data = await response.json();
      const status = data.runId ? `Running: ${data.runId}` : 'Completed';
      setWorkflowStatus(status);
      
      const systemMessage: Message = {
        id: `workflow_${Date.now()}`,
        role: 'system',
        content: `Workflow execution: ${data.status || 'initiated'}. ${data.message || ''}`,
        timestamp: new Date(),
        references: data.details
      };
      setMessages(prev => [...prev, systemMessage]);
    } catch (error: any) {
      const errorMsg = error.message || 'Workflow execution failed';
      setWorkflowStatus(`Error: ${errorMsg}`);
      
      const errorMessage: Message = {
        id: `workflow_error_${Date.now()}`,
        role: 'system',
        content: `Workflow error: ${errorMsg}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  // Export conversation with enhanced metadata
  const exportConversation = () => {
    const conversationData = {
      conversation_id: sessionId,
      agent_type: selectedAgent,
      messages: messages.map(msg => ({
        ...msg,
        timestamp: msg.timestamp.toISOString()
      })),
      session_info: {
        started_at: messages.length > 0 ? messages[0].timestamp.toISOString() : new Date().toISOString(),
        agent_status: agentStatus,
        total_messages: messages.length
      },
      export_timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(conversationData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `infoterminal_agent_conversation_${sessionId || Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Clear conversation with confirmation
  const clearConversation = () => {
    if (messages.length === 0) return;
    
    if (confirm('Are you sure you want to clear this conversation? This action cannot be undone.')) {
      setMessages([]);
      setSessionId(null);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const currentCapability = AGENT_CAPABILITIES.find(c => c.id === selectedAgent);

  return (
    <DashboardLayout 
      title="Investigation Agent" 
      subtitle="AI-powered intelligence analysis and investigation platform"
    >
      <div className="flex flex-col h-[calc(100vh-12rem)] max-w-7xl mx-auto">
        
        {/* Enhanced Status Banner */}
        {agentStatus.healthy === false && (
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
                onClick={checkAgentHealth}
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
            
            {/* Agent Selection Header */}
            <Panel className="mb-4">
              <div className="p-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    {currentCapability && (
                      <div className={`p-2 rounded-lg ${CAPABILITY_STYLES[currentCapability.color as keyof typeof CAPABILITY_STYLES]}`}>
                        <currentCapability.icon size={20} />
                      </div>
                    )}
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-slate-100">
                        {currentCapability?.displayName || 'Select Agent'}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-slate-400">
                        {currentCapability?.description || 'Choose an AI agent for your investigation'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                      agentStatus.healthy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {agentStatus.healthy ? 'Online' : 'Offline'}
                    </span>
                    {sessionId && (
                      <span className="text-xs text-gray-500 dark:text-slate-400">
                        Session: {sessionId.slice(-8)}
                      </span>
                    )}
                  </div>
                </div>
                
                {/* Agent Selector */}
                <select
                  value={selectedAgent}
                  onChange={(e) => setSelectedAgent(e.target.value)}
                  className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  disabled={isLoading}
                >
                  {AGENT_CAPABILITIES.map((capability) => (
                    <option key={capability.id} value={capability.id}>
                      {capability.displayName}
                    </option>
                  ))}
                </select>
              </div>
            </Panel>

            {/* Messages Panel */}
            <Panel className="flex-1 flex flex-col min-h-0">
              
              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
                {messages.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-center">
                    {currentCapability && (
                      <div className={`p-4 rounded-full mb-4 ${CAPABILITY_STYLES[currentCapability.color as keyof typeof CAPABILITY_STYLES]}`}>
                        <currentCapability.icon size={48} />
                      </div>
                    )}
                    <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">
                      {currentCapability?.displayName || 'Investigation Agent'}
                    </h3>
                    <p className="text-gray-500 dark:text-slate-400 max-w-md mb-4">
                      {currentCapability?.description || 'Start a conversation to begin your investigation.'}
                    </p>
                    {currentCapability && (
                      <div className="text-xs text-gray-400 dark:text-slate-500">
                        <strong>Available tools:</strong> {currentCapability.tools.join(', ')}
                      </div>
                    )}
                  </div>
                ) : (
                  <>
                    {messages.map((message) => (
                      <EnhancedMessageBubble 
                        key={message.id} 
                        message={message} 
                        showSteps={showSteps}
                        setShowSteps={setShowSteps}
                        copyToClipboard={copyToClipboard}
                      />
                    ))}
                    {isLoading && (
                      <div className="flex items-center gap-3 text-gray-500">
                        <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                          currentCapability ? CAPABILITY_STYLES[currentCapability.color as keyof typeof CAPABILITY_STYLES] : 'bg-gray-100'
                        }`}>
                          <RefreshCw size={16} className="animate-spin" />
                        </div>
                        <div className="flex items-center gap-2">
                          <Zap size={14} />
                          <span className="text-sm">Processing with {currentCapability?.displayName}...</span>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </>
                )}
              </div>

              {/* Enhanced Input Area */}
              <div className="border-t border-gray-200 dark:border-gray-700 p-4">
                <div className="flex gap-2">
                  <div className="flex-1">
                    <textarea
                      ref={inputRef}
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={`Ask ${currentCapability?.displayName || 'the agent'} anything about your investigation...`}
                      className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 resize-none"
                      rows={2}
                      disabled={isLoading}
                    />
                  </div>
                  <div className="flex flex-col gap-1">
                    <button
                      onClick={sendMessage}
                      disabled={!inputText.trim() || isLoading}
                      className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                      title="Send message (Enter)"
                    >
                      <Send size={16} />
                    </button>
                    {currentCapability && (
                      <button
                        onClick={() => runCapability(currentCapability)}
                        disabled={isLoading}
                        className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        title={`Run ${currentCapability.displayName} analysis`}
                      >
                        <Play size={16} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </Panel>
          </div>

          {/* Enhanced Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Agent Capabilities */}
            <Panel title="Available Agents">
              <div className="space-y-2">
                {AGENT_CAPABILITIES.map((capability) => (
                  <button
                    key={capability.id}
                    onClick={() => setSelectedAgent(capability.id)}
                    className={`w-full p-3 text-left rounded-lg border transition-colors ${
                      selectedAgent === capability.id 
                        ? CAPABILITY_STYLES[capability.color as keyof typeof CAPABILITY_STYLES] 
                        : 'border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg ${
                        selectedAgent === capability.id 
                          ? 'bg-white/20' 
                          : CAPABILITY_STYLES[capability.color as keyof typeof CAPABILITY_STYLES]
                      }`}>
                        <capability.icon size={16} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-sm">
                          {capability.displayName}
                        </h4>
                        <p className="text-xs opacity-75 mt-1">
                          {capability.description}
                        </p>
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
                  disabled={isLoading}
                  className="w-full p-3 text-left rounded-lg bg-purple-50 border border-purple-200 hover:bg-purple-100 dark:bg-purple-900/20 dark:border-purple-900/30 dark:hover:bg-purple-900/30 transition-colors disabled:opacity-50"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-purple-100 text-purple-600 rounded-lg dark:bg-purple-900/50 dark:text-purple-400">
                      <Sparkles size={16} />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-slate-100 text-sm">
                        Trigger Workflow
                      </h4>
                      <p className="text-xs text-gray-500 dark:text-slate-400">
                        Run automated pipeline
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

            {/* Session Management */}
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
                </div>
                
                <div className="flex gap-2">
                  <button
                    onClick={exportConversation}
                    disabled={messages.length === 0}
                    className="flex-1 px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700 disabled:opacity-50 flex items-center gap-2 justify-center"
                  >
                    <Download size={14} />
                    Export
                  </button>
                  <button
                    onClick={clearConversation}
                    disabled={messages.length === 0}
                    className="flex-1 px-3 py-2 text-sm text-red-600 bg-red-50 rounded-lg hover:bg-red-100 dark:bg-red-900/20 dark:text-red-300 dark:hover:bg-red-900/30 disabled:opacity-50 flex items-center gap-2 justify-center"
                  >
                    <Trash2 size={14} />
                    Clear
                  </button>
                </div>
              </div>
            </Panel>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

interface MessageBubbleProps {
  message: Message;
  showSteps: { [key: string]: boolean };
  setShowSteps: React.Dispatch<React.SetStateAction<{ [key: string]: boolean }>>;
  copyToClipboard: (text: string) => void;
}

function EnhancedMessageBubble({ message, showSteps, setShowSteps, copyToClipboard }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  const capability = AGENT_CAPABILITIES.find(c => c.id === message.agentType);
  
  const toggleSteps = () => {
    setShowSteps(prev => ({
      ...prev,
      [message.id]: !prev[message.id]
    }));
  };

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className={`flex items-center justify-center w-8 h-8 rounded-full flex-shrink-0 ${
          isSystem 
            ? 'bg-orange-100 text-orange-600 dark:bg-orange-900/20 dark:text-orange-400' 
            : capability
            ? CAPABILITY_STYLES[capability.color as keyof typeof CAPABILITY_STYLES]
            : 'bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
        }`}>
          {isSystem ? (
            <Settings size={16} />
          ) : capability ? (
            <capability.icon size={16} />
          ) : (
            <Bot size={16} />
          )}
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
          <div className="prose prose-sm max-w-none">
            <p className="whitespace-pre-wrap m-0">{message.content}</p>
          </div>
        </div>
        
        {/* Message Metadata */}
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-slate-400 flex-wrap">
          <span>{message.timestamp.toLocaleTimeString()}</span>
          
          {message.role === 'assistant' && capability && (
            <>
              <span>•</span>
              <span className="inline-flex items-center gap-1">
                <capability.icon size={12} />
                {capability.displayName}
              </span>
            </>
          )}

          {message.toolsUsed && message.toolsUsed.length > 0 && (
            <>
              <span>•</span>
              <div className="flex flex-wrap gap-1">
                {message.toolsUsed.map(tool => (
                  <span key={tool} className="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">
                    {tool}
                  </span>
                ))}
              </div>
            </>
          )}
          
          {message.executionTime && (
            <>
              <span>•</span>
              <span className="inline-flex items-center gap-1">
                <Clock size={12} />
                {message.executionTime.toFixed(2)}s
              </span>
            </>
          )}
          
          {message.confidence !== undefined && (
            <>
              <span>•</span>
              <span className="inline-flex items-center gap-1">
                <CheckCircle size={12} />
                {(message.confidence * 100).toFixed(0)}%
              </span>
            </>
          )}

          <button
            onClick={() => copyToClipboard(message.content)}
            className="ml-auto p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
            title="Copy message"
          >
            <Copy size={12} />
          </button>
        </div>

        {/* Enhanced Steps and References */}
        {(message.steps?.length || message.references) && (
          <div className="mt-2 space-y-2">
            {message.steps && message.steps.length > 0 && (
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg">
                <button
                  onClick={toggleSteps}
                  className="w-full flex items-center justify-between p-2 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
                >
                  <span>Execution Steps ({message.steps.length})</span>
                  {showSteps[message.id] ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                </button>
                
                {showSteps[message.id] && (
                  <div className="p-2 space-y-2 border-t border-gray-200 dark:border-gray-700">
                    {message.steps.map((step, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        {step.error ? (
                          <AlertCircle className="h-3 w-3 text-red-500 mt-0.5" />
                        ) : (
                          <CheckCircle className="h-3 w-3 text-green-500 mt-0.5" />
                        )}
                        <div className="flex-1 text-xs">
                          <div className="font-medium">{step.tool}</div>
                          {step.error ? (
                            <div className="text-red-600 dark:text-red-400">{step.error}</div>
                          ) : (
                            <div className="text-gray-600 dark:text-gray-400">
                              {step.result ? 'Completed successfully' : 'Processing...'}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
            
            {message.references && (
              <details className="bg-gray-50 dark:bg-gray-900 rounded-lg">
                <summary className="cursor-pointer p-2 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg">
                  References & Citations
                </summary>
                <pre className="mt-1 p-2 text-xs overflow-auto border-t border-gray-200 dark:border-gray-700">
                  {JSON.stringify(message.references, null, 2)}
                </pre>
              </details>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex items-center justify-center w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex-shrink-0 dark:bg-primary-900/20 dark:text-primary-400">
          <User size={16} />
        </div>
      )}
    </div>
  );
}
