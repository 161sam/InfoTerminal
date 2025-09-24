// Agent Status Dashboard for InfoTerminal
// Real-time monitoring of agent services and capabilities

import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import {
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Clock,
  Activity,
  Server,
  Zap,
  Settings,
} from "lucide-react";
import {
  AGENT_CAPABILITIES,
  AGENT_ENDPOINTS,
  checkAllAgentHealth,
  checkAgentHealth,
  getCapabilitiesByCategory,
  CAPABILITY_COLORS,
  type AgentCapability,
  type AgentEndpoint,
} from "@/lib/agent-config";

interface ServiceStatus {
  healthy: boolean;
  responseTime?: number;
  error?: string;
  lastCheck?: Date;
}

interface AgentStatusDashboardProps {
  className?: string;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export const AgentStatusDashboard: React.FC<AgentStatusDashboardProps> = ({
  className = "",
  autoRefresh = true,
  refreshInterval = 30000, // 30 seconds
}) => {
  const [serviceStatus, setServiceStatus] = useState<{ [key: string]: ServiceStatus }>({});
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  // Check health of all services
  const checkAllServices = useCallback(async () => {
    setLoading(true);
    try {
      const results = await checkAllAgentHealth();
      const statusWithTimestamp: { [key: string]: ServiceStatus } = {};

      Object.entries(results).forEach(([name, result]) => {
        statusWithTimestamp[name] = {
          ...result,
          lastCheck: new Date(),
        };
      });

      setServiceStatus(statusWithTimestamp);
      setLastUpdate(new Date());
    } catch (error) {
      console.error("Failed to check agent health:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial health check
  useEffect(() => {
    checkAllServices();
  }, [checkAllServices]);

  // Auto-refresh
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(checkAllServices, refreshInterval);
    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval, checkAllServices]);

  const getStatusIcon = (status: ServiceStatus) => {
    if (status.healthy) {
      return <CheckCircle className="h-4 w-4 text-green-600" />;
    } else {
      return <XCircle className="h-4 w-4 text-red-600" />;
    }
  };

  const getStatusBadge = (status: ServiceStatus) => {
    if (status.healthy) {
      return <Badge className="bg-green-100 text-green-800 border-green-200">Online</Badge>;
    } else {
      return <Badge className="bg-red-100 text-red-800 border-red-200">Offline</Badge>;
    }
  };

  const getResponseTimeColor = (responseTime: number | undefined) => {
    if (!responseTime) return "text-gray-500";
    if (responseTime < 100) return "text-green-600";
    if (responseTime < 500) return "text-yellow-600";
    return "text-red-600";
  };

  const healthyServices = Object.values(serviceStatus).filter((s) => s.healthy).length;
  const totalServices = AGENT_ENDPOINTS.length;
  const overallHealthy = healthyServices === totalServices;

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Overview Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className={`p-2 rounded-lg ${
                  overallHealthy ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600"
                }`}
              >
                <Activity className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Agent Services Status</CardTitle>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Real-time monitoring of AI agent infrastructure
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {lastUpdate && (
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Last updated: {lastUpdate.toLocaleTimeString()}
                </div>
              )}
              <Button variant="outline" size="sm" onClick={checkAllServices} disabled={loading}>
                {loading ? (
                  <RefreshCw className="h-4 w-4 animate-spin" />
                ) : (
                  <RefreshCw className="h-4 w-4" />
                )}
                Refresh
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-3">
              <div
                className={`p-3 rounded-lg ${
                  overallHealthy
                    ? "bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400"
                    : "bg-red-100 text-red-600 dark:bg-red-900/20 dark:text-red-400"
                }`}
              >
                <Server className="h-5 w-5" />
              </div>
              <div>
                <div className="font-semibold">
                  {healthyServices}/{totalServices}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Services Online</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400">
                <Zap className="h-5 w-5" />
              </div>
              <div>
                <div className="font-semibold">{AGENT_CAPABILITIES.length}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">AI Capabilities</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400">
                <Settings className="h-5 w-5" />
              </div>
              <div>
                <div className="font-semibold">
                  {autoRefresh ? `${refreshInterval / 1000}s` : "Manual"}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Refresh Mode</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Service Status Details */}
      <Card>
        <CardHeader>
          <CardTitle>Service Health Details</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {AGENT_ENDPOINTS.map((endpoint) => {
              const status = serviceStatus[endpoint.name] || { healthy: false };

              return (
                <div
                  key={endpoint.name}
                  className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
                >
                  <div className="flex items-center gap-4">
                    {getStatusIcon(status)}
                    <div>
                      <div className="font-medium">{endpoint.name}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">{endpoint.url}</div>
                      {status.error && (
                        <div className="text-xs text-red-600 dark:text-red-400 mt-1">
                          Error: {status.error}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    {status.responseTime && (
                      <div className="text-right">
                        <div
                          className={`text-sm font-medium ${getResponseTimeColor(status.responseTime)}`}
                        >
                          {status.responseTime}ms
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          Response Time
                        </div>
                      </div>
                    )}

                    {status.lastCheck && (
                      <div className="text-right">
                        <div className="text-sm text-gray-600 dark:text-gray-300">
                          {status.lastCheck.toLocaleTimeString()}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">Last Check</div>
                      </div>
                    )}

                    {getStatusBadge(status)}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Agent Capabilities by Category */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {(["analysis", "investigation", "security", "intelligence"] as const).map((category) => {
          const capabilities = getCapabilitiesByCategory(category);
          if (capabilities.length === 0) return null;

          return (
            <Card key={category}>
              <CardHeader>
                <CardTitle className="capitalize">{category} Agents</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {capabilities.map((capability) => (
                    <div
                      key={capability.id}
                      className={`flex items-start gap-3 p-3 rounded-lg border ${CAPABILITY_COLORS[capability.color as keyof typeof CAPABILITY_COLORS]}`}
                    >
                      <div className="mt-0.5">
                        <capability.icon className="h-4 w-4" />
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-sm">{capability.displayName}</div>
                        <div className="text-xs opacity-75 mt-1">{capability.description}</div>
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
                  ))}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default AgentStatusDashboard;
