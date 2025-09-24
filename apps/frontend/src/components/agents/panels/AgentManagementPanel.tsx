import React, { useState, useEffect } from "react";
import {
  Settings,
  Activity,
  Server,
  Brain,
  Users,
  Shield,
  Network,
  Zap,
  BarChart3,
} from "lucide-react";
import Panel from "@/components/layout/Panel";
import { getApis, isAgentEnabled, isMultiAgentEnabled, isWorkflowsEnabled } from "@/lib/config";
import { AgentCapability, CAPABILITY_COLORS } from "./types";
import { cardStyles, textStyles, statusStyles, compose } from "@/styles/design-tokens";

interface AgentManagementPanelProps {
  agentCapabilities: AgentCapability[];
}

export default function AgentManagementPanel({ agentCapabilities }: AgentManagementPanelProps) {
  const [agentHealth, setAgentHealth] = useState<{ [key: string]: any }>({});
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  const apis = getApis();
  const agentEnabled = isAgentEnabled();
  const multiAgentEnabled = isMultiAgentEnabled();
  const workflowsEnabled = isWorkflowsEnabled();

  // Mock health check for demo
  useEffect(() => {
    const mockHealth = {
      "agent-api": { healthy: true, version: "1.2.0", uptime: 86400 },
      "doc-entities": { healthy: true, version: "1.1.0", uptime: 82800 },
      "graph-api": { healthy: false, version: "unknown", uptime: 0 },
    };
    setAgentHealth(mockHealth);
  }, []);

  const categories = [
    { id: "all", name: "All Capabilities", icon: Brain },
    { id: "analysis", name: "Analysis", icon: BarChart3 },
    { id: "investigation", name: "Investigation", icon: Users },
    { id: "security", name: "Security", icon: Shield },
    { id: "intelligence", name: "Intelligence", icon: Network },
  ];

  const filteredCapabilities = agentCapabilities; // For simplicity, showing all

  const healthyServices = Object.values(agentHealth).filter((h) => h.healthy).length;
  const totalServices = Object.keys(agentHealth).length;

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`${cardStyles.base} ${cardStyles.padding}`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={textStyles.body}>Services</p>
              <p className={`text-2xl font-bold ${textStyles.h2}`}>
                {healthyServices}/{totalServices}
              </p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-full">
              <Server className="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>

        <div className={`${cardStyles.base} ${cardStyles.padding}`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={textStyles.body}>Capabilities</p>
              <p className={`text-2xl font-bold ${textStyles.h2}`}>{agentCapabilities.length}</p>
            </div>
            <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full">
              <Brain className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>

        <div className={`${cardStyles.base} ${cardStyles.padding}`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={textStyles.body}>Multi-Agent</p>
              <p className={`text-2xl font-bold ${textStyles.h2}`}>
                {multiAgentEnabled ? "ON" : "OFF"}
              </p>
            </div>
            <div
              className={`p-3 rounded-full ${
                multiAgentEnabled
                  ? "bg-green-100 dark:bg-green-900/30"
                  : "bg-gray-100 dark:bg-gray-800"
              }`}
            >
              <Users
                className={`h-5 w-5 ${
                  multiAgentEnabled
                    ? "text-green-600 dark:text-green-400"
                    : "text-gray-400 dark:text-gray-500"
                }`}
              />
            </div>
          </div>
        </div>

        <div className={`${cardStyles.base} ${cardStyles.padding}`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={textStyles.body}>Workflows</p>
              <p className={`text-2xl font-bold ${textStyles.h2}`}>
                {workflowsEnabled ? "Active" : "Inactive"}
              </p>
            </div>
            <div
              className={`p-3 rounded-full ${
                workflowsEnabled
                  ? "bg-purple-100 dark:bg-purple-900/30"
                  : "bg-gray-100 dark:bg-gray-800"
              }`}
            >
              <Zap
                className={`h-5 w-5 ${
                  workflowsEnabled
                    ? "text-purple-600 dark:text-purple-400"
                    : "text-gray-400 dark:text-gray-500"
                }`}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Service Health Status */}
      <Panel title="Service Health">
        <div className="space-y-3">
          {Object.entries(agentHealth).map(([service, health]) => (
            <div
              key={service}
              className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <div
                  className={`h-3 w-3 rounded-full ${
                    health.healthy ? "bg-green-500 dark:bg-green-400" : "bg-red-500 dark:bg-red-400"
                  }`}
                />
                <div>
                  <p className={textStyles.h4}>{service}</p>
                  <p className={textStyles.bodySmall}>Version: {health.version}</p>
                </div>
              </div>
              <span className={compose.status(health.healthy ? "success" : "error")}>
                {health.healthy ? "Healthy" : "Offline"}
              </span>
            </div>
          ))}
        </div>
      </Panel>

      {/* Category Filters */}
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              selectedCategory === category.id
                ? "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            }`}
          >
            <category.icon size={16} />
            {category.name}
          </button>
        ))}
      </div>

      {/* Agent Capabilities */}
      <Panel title="Agent Capabilities">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredCapabilities.map((capability) => (
            <div
              key={capability.id}
              className={`${cardStyles.base} p-4 hover:shadow-lg transition-shadow`}
            >
              <div className="flex items-start justify-between mb-3">
                <div
                  className={`p-2 rounded-lg ${capability.color.replace("text-", "bg-").replace("600", "100")} dark:bg-opacity-20`}
                >
                  <capability.icon size={20} className={capability.color} />
                </div>
                <span className={compose.status("info")}>{capability.expertise.length} skills</span>
              </div>
              <h3 className={`${textStyles.h4} mb-2`}>{capability.name}</h3>
              <p className={`${textStyles.body} mb-3`}>{capability.description}</p>

              <div className="space-y-2">
                <div>
                  <h4 className={`${textStyles.bodySmall} font-medium mb-1`}>Tools:</h4>
                  <div className="flex flex-wrap gap-1">
                    {capability.tools.slice(0, 3).map((tool, idx) => (
                      <span
                        key={idx}
                        className={`${textStyles.bodySmall} px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded`}
                      >
                        {tool}
                      </span>
                    ))}
                    {capability.tools.length > 3 && (
                      <span
                        className={`${textStyles.bodySmall} px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded`}
                      >
                        +{capability.tools.length - 3} more
                      </span>
                    )}
                  </div>
                </div>

                <div>
                  <h4 className={`${textStyles.bodySmall} font-medium mb-1`}>Expertise:</h4>
                  <div className="flex flex-wrap gap-1">
                    {capability.expertise.slice(0, 2).map((skill, idx) => (
                      <span
                        key={idx}
                        className={`${textStyles.bodySmall} px-2 py-1 bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 rounded`}
                      >
                        {skill}
                      </span>
                    ))}
                    {capability.expertise.length > 2 && (
                      <span
                        className={`${textStyles.bodySmall} px-2 py-1 bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 rounded`}
                      >
                        +{capability.expertise.length - 2} more
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Panel>

      {/* Configuration Overview */}
      <Panel title="Configuration Overview">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <h4 className={textStyles.h4}>Feature Flags</h4>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className={textStyles.body}>Agent System</span>
                <span className={compose.status(agentEnabled ? "success" : "error")}>
                  {agentEnabled ? "Enabled" : "Disabled"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className={textStyles.body}>Multi-Agent</span>
                <span className={compose.status(multiAgentEnabled ? "success" : "error")}>
                  {multiAgentEnabled ? "Enabled" : "Disabled"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className={textStyles.body}>Workflows</span>
                <span className={compose.status(workflowsEnabled ? "success" : "error")}>
                  {workflowsEnabled ? "Enabled" : "Disabled"}
                </span>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h4 className={textStyles.h4}>API Endpoints</h4>
            <div className="space-y-2">
              {Object.entries(apis).map(([name, url]) => (
                <div key={name} className="flex items-center justify-between">
                  <span className={textStyles.body}>{name}</span>
                  <span className={`${textStyles.bodySmall} font-mono truncate max-w-40`}>
                    {url}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Panel>
    </div>
  );
}
