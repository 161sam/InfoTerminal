import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, Zap } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import Button from '@/components/ui/button';
import { LoadingSpinner } from '@/components/ui/loading';
import { getApis } from '@/lib/config';
import { Message, AgentCapability, AgentStatus, CAPABILITY_COLORS } from './types';
import AgentStatusBanner from './AgentStatusBanner';
import AgentSessionPanel from './AgentSessionPanel';
import AgentMessageBubble from './AgentMessageBubble';

interface AgentChatPanelProps {
  agentCapabilities: AgentCapability[];
}

export default function AgentChatPanel({ agentCapabilities }: AgentChatPanelProps) {
  const { AGENT_API } = getApis();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<string>('research_assistant');
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({ healthy: false });
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [showSteps, setShowSteps] = useState<{ [key: string]: boolean }>({});
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

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
    link.download = `agent_conversation_${sessionId || Date.now()}.json`;
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

  const currentCapability = agentCapabilities.find(c => c.id === selectedAgent);

  return (
    <div className="flex flex-col h-[calc(100vh-16rem)] max-w-7xl mx-auto">
      
      {/* Status Banner */}
      <AgentStatusBanner 
        agentStatus={agentStatus} 
        onRetryHealth={checkAgentHealth}
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 min-h-0">
        
        {/* Main Chat Panel */}
        <div className="lg:col-span-3 flex flex-col">
          
          {/* Agent Selection Header */}
          <Panel className="mb-4">
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  {currentCapability && (
                    <div className={`p-2 rounded-lg ${CAPABILITY_COLORS[currentCapability.color as keyof typeof CAPABILITY_COLORS]}`}>
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
                {agentCapabilities.map((capability) => (
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
                    <div className={`p-4 rounded-full mb-4 ${CAPABILITY_COLORS[currentCapability.color as keyof typeof CAPABILITY_COLORS]}`}>
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
                    <AgentMessageBubble
                      key={message.id} 
                      message={message} 
                      showSteps={showSteps}
                      setShowSteps={setShowSteps}
                      copyToClipboard={copyToClipboard}
                      agentCapabilities={agentCapabilities}
                    />
                  ))}
                  {isLoading && (
                    <LoadingSpinner 
                      layout="inline" 
                      variant="primary"
                      text={`Processing with ${currentCapability?.displayName || 'AI Agent'}...`}
                      icon={Zap}
                    />
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
                  <Button
                    onClick={sendMessage}
                    disabled={!inputText.trim() || isLoading}
                    variant="primary"
                    size="md"
                    title="Send message (Enter)"
                  >
                    {isLoading ? (
                      <LoadingSpinner size="sm" />
                    ) : (
                      <Send size={16} />
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </Panel>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          <AgentSessionPanel
            messages={messages}
            sessionId={sessionId}
            selectedAgent={selectedAgent}
            agentStatus={agentStatus}
            agentCapabilities={agentCapabilities}
            onExportConversation={exportConversation}
            onClearConversation={clearConversation}
          />
        </div>
      </div>
    </div>
  );
}
