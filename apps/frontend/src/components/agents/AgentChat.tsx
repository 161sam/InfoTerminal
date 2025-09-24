// Enhanced AI Agent Chat Interface for InfoTerminal
// Modular component for intelligent OSINT investigation assistance

import React, { useState, useEffect, useCallback, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Badge } from "../ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { ScrollArea } from "../ui/scroll-area";
import {
  Send,
  Bot,
  User,
  Settings,
  RefreshCw,
  Download,
  Trash2,
  Clock,
  CheckCircle,
  AlertCircle,
  Zap,
  Search,
  Network,
  Shield,
  MapPin,
  Copy,
  ChevronDown,
  ChevronRight,
  Play,
  Cpu,
} from "lucide-react";

interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  agent_type?: string;
  tools_used?: string[];
  steps?: ChatStep[];
  confidence?: number;
  execution_time?: number;
  references?: any;
}

interface ChatStep {
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
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  tools: string[];
}

interface Tool {
  name: string;
  description: string;
  parameters: Record<string, any>;
  category?: string;
}

interface AgentChatProps {
  apiBaseUrl?: string;
  className?: string;
  enableWorkflows?: boolean;
  maxHeight?: string;
}

const AGENT_CAPABILITIES: AgentCapability[] = [
  {
    id: "research_assistant",
    name: "research_assistant",
    displayName: "Research Assistant",
    description: "Comprehensive research across multiple data sources and databases",
    icon: Search,
    color: "blue",
    tools: ["web_search", "database_query", "document_analysis", "fact_checking"],
  },
  {
    id: "graph_analyst",
    name: "graph_analyst",
    displayName: "Graph Analyst",
    description: "Network analysis, relationship mapping, and connection discovery",
    icon: Network,
    color: "purple",
    tools: ["neo4j_query", "network_analysis", "path_finding", "community_detection"],
  },
  {
    id: "security_analyst",
    name: "security_analyst",
    displayName: "Security Analyst",
    description: "Threat assessment, risk analysis, and security intelligence",
    icon: Shield,
    color: "red",
    tools: ["threat_intel", "vulnerability_scan", "risk_assessment", "iot_analysis"],
  },
  {
    id: "geospatial_analyst",
    name: "geospatial_analyst",
    displayName: "Geospatial Analyst",
    description: "Location intelligence, spatial analysis, and geographic insights",
    icon: MapPin,
    color: "green",
    tools: ["gis_analysis", "location_intel", "spatial_query", "route_analysis"],
  },
  {
    id: "person_investigator",
    name: "person_investigator",
    displayName: "Person Investigator",
    description: "Deep person profiling, background checks, and social network analysis",
    icon: User,
    color: "indigo",
    tools: ["social_media", "public_records", "network_mapping", "background_check"],
  },
  {
    id: "financial_analyst",
    name: "financial_analyst",
    displayName: "Financial Analyst",
    description: "Financial pattern analysis, risk modeling, and compliance assessment",
    icon: Cpu,
    color: "amber",
    tools: ["transaction_analysis", "risk_modeling", "compliance_check", "fraud_detection"],
  },
];

const CAPABILITY_COLORS = {
  blue: "bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300",
  purple: "bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-300",
  red: "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300",
  green: "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300",
  indigo: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/20 dark:text-indigo-300",
  amber: "bg-amber-100 text-amber-800 dark:bg-amber-900/20 dark:text-amber-300",
};

export const EnhancedAgentChat: React.FC<AgentChatProps> = ({
  apiBaseUrl = "http://localhost:8610", // Default to agent-connector
  className = "",
  enableWorkflows = false,
  maxHeight = "600px",
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState("research_assistant");
  const [availableTools, setAvailableTools] = useState<Tool[]>([]);
  const [allowedTools, setAllowedTools] = useState<string[]>([]);
  const [showSettings, setShowSettings] = useState(false);
  const [showSteps, setShowSteps] = useState<{ [key: string]: boolean }>({});
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("chat");
  const [agentStatus, setAgentStatus] = useState({ healthy: false, lastCheck: null });

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Check agent health
  const checkHealth = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/healthz`);
      setAgentStatus({
        healthy: response.ok,
        lastCheck: new Date(),
      });
    } catch {
      setAgentStatus({
        healthy: false,
        lastCheck: new Date(),
      });
    }
  }, [apiBaseUrl]);

  // Fetch available tools
  const fetchTools = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/tools`);
      if (!response.ok) throw new Error("Failed to fetch tools");
      const data = await response.json();
      setAvailableTools(data.tools || []);
    } catch (err) {
      console.warn("Could not fetch tools:", err);
      // Set default tools if API is not available
      setAvailableTools([
        { name: "web_search", description: "Search the web for information", parameters: {} },
        { name: "database_query", description: "Query internal databases", parameters: {} },
        { name: "document_analysis", description: "Analyze documents", parameters: {} },
      ]);
    }
  }, [apiBaseUrl]);

  useEffect(() => {
    checkHealth();
    fetchTools();
    const interval = setInterval(checkHealth, 60000); // Check every minute
    return () => clearInterval(interval);
  }, [checkHealth, fetchTools]);

  // Generate session ID
  const generateSessionId = useCallback(() => {
    return `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }, []);

  // Send message with enhanced error handling
  const sendMessage = async () => {
    if (!inputValue.trim() || loading) return;

    const currentSessionId = conversationId || generateSessionId();
    if (!conversationId) setConversationId(currentSessionId);

    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      role: "user",
      content: inputValue.trim(),
      timestamp: new Date(),
      agent_type: selectedAgent,
    };

    setMessages((prev) => [...prev, userMessage]);
    const messageContent = inputValue;
    setInputValue("");
    setLoading(true);
    setError(null);

    try {
      const requestBody = {
        messages: [
          ...messages.map(
            ({ steps, references, timestamp, id, tools_used, confidence, execution_time, ...m }) =>
              m,
          ),
          { role: "user", content: messageContent },
        ],
        agent_type: selectedAgent,
        session_id: currentSessionId,
        tools_allowed: allowedTools.length > 0 ? allowedTools : undefined,
        max_iterations: 10,
        include_steps: true,
      };

      const startTime = Date.now();
      const response = await fetch(`${apiBaseUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Agent error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const executionTime = (Date.now() - startTime) / 1000;

      const assistantMessage: ChatMessage = {
        id: `assistant_${Date.now()}`,
        role: "assistant",
        content: data.reply || data.response || "No response received",
        timestamp: new Date(),
        agent_type: selectedAgent,
        tools_used: data.tools_used || [],
        steps: data.steps || [],
        confidence: data.confidence,
        execution_time: executionTime,
        references: data.references,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setAgentStatus((prev) => ({ ...prev, healthy: true }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      setAgentStatus((prev) => ({ ...prev, healthy: false }));

      const errorMessage: ChatMessage = {
        id: `error_${Date.now()}`,
        role: "system",
        content: `Error: ${err instanceof Error ? err.message : "Unknown error occurred"}`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  // Run specific capability
  const runCapability = useCallback(
    async (capability: AgentCapability) => {
      if (loading || !inputValue.trim()) return;

      const currentSessionId = conversationId || generateSessionId();
      if (!conversationId) setConversationId(currentSessionId);

      setLoading(true);
      try {
        const response = await fetch(`${apiBaseUrl}/capabilities/run`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            capability: capability.id,
            agent_type: capability.name,
            context: inputValue,
            session_id: currentSessionId,
            tools: capability.tools,
          }),
        });

        if (!response.ok) throw new Error(`Capability error: ${response.statusText}`);

        const data = await response.json();
        const systemMessage: ChatMessage = {
          id: `capability_${Date.now()}`,
          role: "system",
          content: `${capability.displayName} analysis: ${data.result || JSON.stringify(data)}`,
          steps: data.steps,
          timestamp: new Date(),
          agent_type: capability.name,
          tools_used: data.tools_used || capability.tools,
        };

        setMessages((prev) => [...prev, systemMessage]);
        setInputValue(""); // Clear input after successful capability run
      } catch (err) {
        const errorMessage: ChatMessage = {
          id: `capability_error_${Date.now()}`,
          role: "system",
          content: `${capability.displayName} failed: ${err instanceof Error ? err.message : "Unknown error"}`,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    },
    [inputValue, loading, conversationId, apiBaseUrl, generateSessionId],
  );

  // Clear conversation
  const clearConversation = async () => {
    if (messages.length === 0) return;

    if (window.confirm("Clear this conversation? This action cannot be undone.")) {
      try {
        if (conversationId) {
          await fetch(`${apiBaseUrl}/conversations/${conversationId}`, {
            method: "DELETE",
          });
        }
      } catch {
        // Ignore deletion errors
      }
      setMessages([]);
      setConversationId(null);
    }
  };

  // Export conversation
  const exportConversation = () => {
    const conversationData = {
      conversation_id: conversationId,
      agent_type: selectedAgent,
      messages: messages.map((msg) => ({
        ...msg,
        timestamp: msg.timestamp.toISOString(),
      })),
      created_at: new Date().toISOString(),
      session_info: {
        agent_status: agentStatus,
        total_messages: messages.length,
      },
    };

    const blob = new Blob([JSON.stringify(conversationData, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `agent_chat_${conversationId || Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const toggleSteps = (messageId: string) => {
    setShowSteps((prev) => ({
      ...prev,
      [messageId]: !prev[messageId],
    }));
  };

  const currentCapability = AGENT_CAPABILITIES.find((c) => c.id === selectedAgent);

  const renderMessage = (message: ChatMessage) => {
    const isUser = message.role === "user";
    const isSystem = message.role === "system";
    const capability = AGENT_CAPABILITIES.find((c) => c.id === message.agent_type);

    return (
      <div key={message.id} className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
        {!isUser && (
          <div className="flex-shrink-0">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center ${
                isSystem
                  ? "bg-orange-100 text-orange-600 dark:bg-orange-900/20 dark:text-orange-300"
                  : capability
                    ? CAPABILITY_COLORS[capability.color as keyof typeof CAPABILITY_COLORS]
                    : "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300"
              }`}
            >
              {isSystem ? (
                <Settings className="h-4 w-4" />
              ) : capability ? (
                <capability.icon className="h-4 w-4" />
              ) : (
                <Bot className="h-4 w-4" />
              )}
            </div>
          </div>
        )}

        <div className={`max-w-[70%] ${isUser ? "order-first" : ""}`}>
          <div
            className={`rounded-lg p-3 ${
              isUser
                ? "bg-blue-600 text-white"
                : isSystem
                  ? "bg-orange-50 text-orange-900 border border-orange-200 dark:bg-orange-900/20 dark:text-orange-300 dark:border-orange-900/30"
                  : "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100"
            }`}
          >
            <div className="text-sm whitespace-pre-wrap">{message.content}</div>
          </div>

          {/* Message metadata */}
          <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-gray-400 flex-wrap">
            <span>{message.timestamp.toLocaleTimeString()}</span>

            {capability && message.role === "assistant" && (
              <>
                <span>•</span>
                <span className="inline-flex items-center gap-1">
                  <capability.icon className="h-3 w-3" />
                  {capability.displayName}
                </span>
              </>
            )}

            {message.tools_used && message.tools_used.length > 0 && (
              <>
                <span>•</span>
                <div className="flex flex-wrap gap-1">
                  {message.tools_used.map((tool) => (
                    <Badge key={tool} variant="outline" className="text-xs">
                      {tool}
                    </Badge>
                  ))}
                </div>
              </>
            )}

            {message.execution_time && (
              <>
                <span>•</span>
                <span className="inline-flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {message.execution_time.toFixed(2)}s
                </span>
              </>
            )}

            {message.confidence !== undefined && (
              <>
                <span>•</span>
                <span className="inline-flex items-center gap-1">
                  <CheckCircle className="h-3 w-3" />
                  {(message.confidence * 100).toFixed(0)}%
                </span>
              </>
            )}

            <Button
              variant="ghost"
              size="sm"
              className="h-auto p-1 ml-auto"
              onClick={() => copyToClipboard(message.content)}
            >
              <Copy className="h-3 w-3" />
            </Button>
          </div>

          {/* Steps and references */}
          {(message.steps?.length || message.references) && (
            <div className="mt-2 space-y-2">
              {message.steps && message.steps.length > 0 && (
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <button
                    onClick={() => toggleSteps(message.id)}
                    className="w-full flex items-center justify-between p-2 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
                  >
                    <span>Execution Steps ({message.steps.length})</span>
                    {showSteps[message.id] ? (
                      <ChevronDown className="h-3 w-3" />
                    ) : (
                      <ChevronRight className="h-3 w-3" />
                    )}
                  </button>

                  {showSteps[message.id] && (
                    <div className="p-2 space-y-1 border-t border-gray-200 dark:border-gray-700">
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
                              <div className="text-gray-600 dark:text-gray-400">Completed</div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {isUser && (
          <div className="flex-shrink-0">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
              <User className="h-4 w-4 text-white" />
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={`w-full ${className}`} style={{ height: maxHeight }}>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full h-full flex flex-col">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="chat">Chat</TabsTrigger>
          <TabsTrigger value="capabilities">Capabilities</TabsTrigger>
          <TabsTrigger value="tools">Tools</TabsTrigger>
        </TabsList>

        <TabsContent value="chat" className="flex-1 mt-4">
          <div className="flex flex-col h-full">
            {/* Agent Selection Header */}
            <Card className="mb-4">
              <CardContent className="pt-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {currentCapability && (
                      <div
                        className={`p-2 rounded-lg ${CAPABILITY_COLORS[currentCapability.color as keyof typeof CAPABILITY_COLORS]}`}
                      >
                        <currentCapability.icon className="h-4 w-4" />
                      </div>
                    )}
                    <div className="flex-1">
                      <Select value={selectedAgent} onValueChange={setSelectedAgent}>
                        <SelectTrigger className="w-[200px]">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {AGENT_CAPABILITIES.map((capability) => (
                            <SelectItem key={capability.id} value={capability.id}>
                              <div className="flex items-center gap-2">
                                <capability.icon className="h-4 w-4" />
                                {capability.displayName}
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Badge variant={agentStatus.healthy ? "default" : "destructive"}>
                      {agentStatus.healthy ? "Online" : "Offline"}
                    </Badge>
                    <Button variant="outline" size="sm" onClick={() => setShowSettings(true)}>
                      <Settings className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={clearConversation}
                      disabled={messages.length === 0}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={exportConversation}
                      disabled={messages.length === 0}
                    >
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Messages Area */}
            <Card className="flex-1 flex flex-col">
              <CardContent className="flex-1 flex flex-col p-4">
                <ScrollArea className="flex-1 pr-4">
                  <div className="space-y-4">
                    {messages.length === 0 ? (
                      <div className="text-center text-gray-500 py-8">
                        {currentCapability && (
                          <div
                            className={`w-12 h-12 rounded-full mx-auto mb-4 flex items-center justify-center ${CAPABILITY_COLORS[currentCapability.color as keyof typeof CAPABILITY_COLORS]}`}
                          >
                            <currentCapability.icon className="h-6 w-6" />
                          </div>
                        )}
                        <div className="text-lg font-medium">
                          {currentCapability?.displayName} Ready
                        </div>
                        <div className="text-sm mt-1">{currentCapability?.description}</div>
                      </div>
                    ) : (
                      messages.map(renderMessage)
                    )}

                    {loading && (
                      <div className="flex gap-3">
                        <div className="flex-shrink-0">
                          <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center ${
                              currentCapability
                                ? CAPABILITY_COLORS[
                                    currentCapability.color as keyof typeof CAPABILITY_COLORS
                                  ]
                                : "bg-gray-100"
                            }`}
                          >
                            <RefreshCw className="h-4 w-4 animate-spin" />
                          </div>
                        </div>
                        <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-3">
                          <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                            <Zap className="h-4 w-4" />
                            Processing...
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  <div ref={messagesEndRef} />
                </ScrollArea>

                {/* Input Area */}
                <div className="mt-4 flex gap-2">
                  <Input
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
                    placeholder={`Ask ${currentCapability?.displayName || "the agent"}...`}
                    disabled={loading}
                    className="flex-1"
                  />
                  <Button onClick={sendMessage} disabled={!inputValue.trim() || loading}>
                    {loading ? (
                      <RefreshCw className="h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                  </Button>
                  {currentCapability && (
                    <Button
                      onClick={() => runCapability(currentCapability)}
                      disabled={!inputValue.trim() || loading}
                      variant="secondary"
                    >
                      <Play className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="capabilities" className="flex-1 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Available AI Capabilities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {AGENT_CAPABILITIES.map((capability) => (
                  <Card
                    key={capability.id}
                    className={`cursor-pointer transition-colors ${
                      selectedAgent === capability.id ? "ring-2 ring-primary" : ""
                    }`}
                    onClick={() => setSelectedAgent(capability.id)}
                  >
                    <CardContent className="pt-4">
                      <div className="flex items-start gap-3">
                        <div
                          className={`p-2 rounded-lg ${CAPABILITY_COLORS[capability.color as keyof typeof CAPABILITY_COLORS]}`}
                        >
                          <capability.icon className="h-4 w-4" />
                        </div>
                        <div className="flex-1">
                          <div className="font-medium">{capability.displayName}</div>
                          <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                            {capability.description}
                          </div>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {capability.tools.slice(0, 3).map((tool) => (
                              <Badge key={tool} variant="outline" className="text-xs">
                                {tool}
                              </Badge>
                            ))}
                            {capability.tools.length > 3 && (
                              <Badge variant="outline" className="text-xs">
                                +{capability.tools.length - 3} more
                              </Badge>
                            )}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tools" className="flex-1 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Available Tools</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {availableTools.map((tool) => (
                  <Card key={tool.name}>
                    <CardContent className="pt-4">
                      <div className="font-medium">{tool.name}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {tool.description}
                      </div>
                      {Object.keys(tool.parameters).length > 0 && (
                        <div className="mt-2">
                          <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Parameters:
                          </div>
                          <div className="text-xs text-gray-600 dark:text-gray-400">
                            {Object.keys(tool.parameters).join(", ")}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Settings Dialog */}
      <Dialog open={showSettings} onOpenChange={setShowSettings}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Agent Settings</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">Tool Restrictions</label>
              <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                Leave empty to allow all tools, or select specific tools to restrict usage.
              </p>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {availableTools.map((tool) => (
                  <div key={tool.name} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id={tool.name}
                      checked={allowedTools.includes(tool.name)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setAllowedTools((prev) => [...prev, tool.name]);
                        } else {
                          setAllowedTools((prev) => prev.filter((t) => t !== tool.name));
                        }
                      }}
                    />
                    <label htmlFor={tool.name} className="text-sm">
                      {tool.name}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {error && (
        <div className="fixed bottom-4 right-4 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded shadow-lg z-50 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4" />
            {error}
          </div>
        </div>
      )}
    </div>
  );
};

export { EnhancedAgentChat as AgentChat };
export default EnhancedAgentChat;
