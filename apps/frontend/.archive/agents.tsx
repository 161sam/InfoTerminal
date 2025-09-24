import { useState, useEffect } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import AgentStatusDashboard from "@/components/agents/AgentStatusDashboard";
import { EnhancedAgentChat } from "@/components/agents/AgentChat";
import {
  Bot,
  Settings,
  Activity,
  Database,
  Users,
  BarChart3,
  MessageSquare,
  Zap,
  Server,
  Brain,
  Network,
  Shield,
} from "lucide-react";
import {
  AGENT_CAPABILITIES,
  AGENT_CONFIG,
  getCapabilitiesByCategory,
  checkAllAgentHealth,
  CAPABILITY_COLORS,
} from "@/lib/agent-config";
import { getApis, isAgentEnabled, isMultiAgentEnabled, isWorkflowsEnabled } from "@/lib/config";

interface AgentManagementProps {}

export default function AgentManagement({}: AgentManagementProps) {
  const [activeTab, setActiveTab] = useState("overview");
  const [agentHealth, setAgentHealth] = useState<{ [key: string]: any }>({});
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  const apis = getApis();
  const agentEnabled = isAgentEnabled();
  const multiAgentEnabled = isMultiAgentEnabled();
  const workflowsEnabled = isWorkflowsEnabled();

  // Load agent health on mount
  useEffect(() => {
    const loadHealth = async () => {
      try {
        const health = await checkAllAgentHealth();
        setAgentHealth(health);
      } catch (error) {
        console.error("Failed to load agent health:", error);
      }
    };

    if (agentEnabled) {
      loadHealth();
    }
  }, [agentEnabled]);

  if (!agentEnabled) {
    return (
      <DashboardLayout title="Agent Management" subtitle="AI agent services are currently disabled">
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <div className="p-4 bg-gray-100 rounded-full mb-4">
              <Bot className="h-12 w-12 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium mb-2">Agent Services Not Available</h3>
            <p className="text-gray-600 text-center max-w-md mb-4">
              Agent services are currently disabled. Enable them by setting
              NEXT_PUBLIC_FEATURE_AGENT=1 in your environment configuration.
            </p>
            <Button variant="outline">
              <Settings className="h-4 w-4 mr-2" />
              Configure Services
            </Button>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  const categories = [
    { id: "all", name: "All Capabilities", icon: Brain },
    { id: "analysis", name: "Analysis", icon: BarChart3 },
    { id: "investigation", name: "Investigation", icon: Users },
    { id: "security", name: "Security", icon: Shield },
    { id: "intelligence", name: "Intelligence", icon: Network },
  ];

  const filteredCapabilities =
    selectedCategory === "all"
      ? AGENT_CAPABILITIES
      : getCapabilitiesByCategory(selectedCategory as any);

  const healthyServices = Object.values(agentHealth).filter((h) => h.healthy).length;
  const totalServices = Object.keys(agentHealth).length;

  return (
    <DashboardLayout
      title="Agent Management"
      subtitle="AI-powered investigation and analysis platform"
    >
      <div className="space-y-6">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Services</p>
                <p className="text-2xl font-bold">
                  {healthyServices}/{totalServices}
                </p>
              </div>
              <div className="p-3 bg-green-100 rounded-full">
                <Server className="h-5 w-5 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Capabilities</p>
                <p className="text-2xl font-bold">{AGENT_CAPABILITIES.length}</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-full">
                <Brain className="h-5 w-5 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Multi-Agent</p>
                <p className="text-2xl font-bold">{multiAgentEnabled ? "ON" : "OFF"}</p>
              </div>
              <div
                className={`p-3 rounded-full ${multiAgentEnabled ? "bg-green-100" : "bg-gray-100"}`}
              >
                <Users
                  className={`h-5 w-5 ${multiAgentEnabled ? "text-green-600" : "text-gray-400"}`}
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Workflows</p>
                <p className="text-2xl font-bold">{workflowsEnabled ? "ON" : "OFF"}</p>
              </div>
              <div
                className={`p-3 rounded-full ${workflowsEnabled ? "bg-purple-100" : "bg-gray-100"}`}
              >
                <Zap
                  className={`h-5 w-5 ${workflowsEnabled ? "text-purple-600" : "text-gray-400"}`}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="capabilities">Capabilities</TabsTrigger>
            <TabsTrigger value="chat">Test Chat</TabsTrigger>
            <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Service Status Overview */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5" />
                    Service Health
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(agentHealth).map(([service, status]) => (
                      <div key={service} className="flex items-center justify-between">
                        <span className="font-medium">{service}</span>
                        <Badge variant={status.healthy ? "default" : "destructive"}>
                          {status.healthy ? "Online" : "Offline"}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Configuration Overview */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5" />
                    Configuration
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span>Default Agent:</span>
                      <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                        {AGENT_CONFIG.defaults.defaultCapability}
                      </code>
                    </div>
                    <div className="flex justify-between">
                      <span>Max Iterations:</span>
                      <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                        {AGENT_CONFIG.defaults.maxIterations}
                      </code>
                    </div>
                    <div className="flex justify-between">
                      <span>Include Steps:</span>
                      <Badge variant={AGENT_CONFIG.defaults.includeSteps ? "default" : "secondary"}>
                        {AGENT_CONFIG.defaults.includeSteps ? "Yes" : "No"}
                      </Badge>
                    </div>
                    <div className="flex justify-between">
                      <span>Timeout:</span>
                      <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                        {AGENT_CONFIG.defaults.timeout / 1000}s
                      </code>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="capabilities" className="mt-6">
            <div className="space-y-6">
              {/* Category Filter */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex flex-wrap gap-2">
                    {categories.map((category) => (
                      <Button
                        key={category.id}
                        variant={selectedCategory === category.id ? "default" : "outline"}
                        size="sm"
                        onClick={() => setSelectedCategory(category.id)}
                      >
                        <category.icon className="h-4 w-4 mr-2" />
                        {category.name}
                      </Button>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Capabilities Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredCapabilities.map((capability) => (
                  <Card key={capability.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex items-start gap-4">
                        <div
                          className={`p-3 rounded-lg ${CAPABILITY_COLORS[capability.color as keyof typeof CAPABILITY_COLORS]}`}
                        >
                          <capability.icon className="h-5 w-5" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold mb-2">{capability.displayName}</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                            {capability.description}
                          </p>

                          {/* Tools */}
                          <div className="mb-3">
                            <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                              Available Tools:
                            </div>
                            <div className="flex flex-wrap gap-1">
                              {capability.tools.slice(0, 3).map((tool) => (
                                <Badge key={tool} variant="outline" className="text-xs">
                                  {tool}
                                </Badge>
                              ))}
                              {capability.tools.length > 3 && (
                                <Badge variant="outline" className="text-xs">
                                  +{capability.tools.length - 3}
                                </Badge>
                              )}
                            </div>
                          </div>

                          {/* Expertise */}
                          <div>
                            <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                              Expertise:
                            </div>
                            <div className="text-xs text-gray-600 dark:text-gray-400">
                              {capability.expertise.slice(0, 2).join(", ")}
                              {capability.expertise.length > 2 && "..."}
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="chat" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5" />
                  Agent Test Interface
                </CardTitle>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Test agent capabilities and debug responses
                </p>
              </CardHeader>
              <CardContent>
                <EnhancedAgentChat
                  apiBaseUrl={apis.AGENT_API}
                  enableWorkflows={workflowsEnabled}
                  maxHeight="600px"
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="monitoring" className="mt-6">
            <AgentStatusDashboard autoRefresh={true} refreshInterval={30000} />
          </TabsContent>

          <TabsContent value="settings" className="mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* API Endpoints */}
              <Card>
                <CardHeader>
                  <CardTitle>API Endpoints</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <label className="text-sm font-medium">Agent API:</label>
                      <code className="block text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded mt-1">
                        {apis.AGENT_API}
                      </code>
                    </div>
                    <div>
                      <label className="text-sm font-medium">Doc Entities API:</label>
                      <code className="block text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded mt-1">
                        {apis.DOC_ENTITIES_API}
                      </code>
                    </div>
                    {workflowsEnabled && (
                      <div>
                        <label className="text-sm font-medium">N8N API:</label>
                        <code className="block text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded mt-1">
                          {apis.N8N_API}
                        </code>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Feature Flags */}
              <Card>
                <CardHeader>
                  <CardTitle>Feature Configuration</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span>Agent Services:</span>
                      <Badge variant={agentEnabled ? "default" : "secondary"}>
                        {agentEnabled ? "Enabled" : "Disabled"}
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Multi-Agent:</span>
                      <Badge variant={multiAgentEnabled ? "default" : "secondary"}>
                        {multiAgentEnabled ? "Enabled" : "Disabled"}
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Workflows:</span>
                      <Badge variant={workflowsEnabled ? "default" : "secondary"}>
                        {workflowsEnabled ? "Enabled" : "Disabled"}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
