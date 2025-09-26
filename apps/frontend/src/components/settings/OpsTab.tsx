import { useEffect, useState, useCallback } from "react";
import {
  Play,
  Square,
  RotateCcw,
  Activity,
  Settings,
  Server,
  AlertTriangle,
  CheckCircle,
  Clock,
  Monitor,
  RefreshCw,
  ChevronDown,
  ChevronRight,
  Terminal,
  BarChart3,
  HardDrive,
  Cpu,
  Network,
  Eye,
  EyeOff,
  Lock,
} from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import { toast } from "@/components/ui/toast";
import {
  listStacks,
  stackStatus,
  stackUp,
  stackDown,
  stackRestart,
  stackScale,
  streamLogs,
} from "@/lib/ops";
import { useAuth } from "@/components/auth/AuthProvider";
import { canAccessFeature } from "@/lib/auth/rbac";

interface StackInfo {
  title: string;
  files: string[];
}

interface ServiceInfo {
  Service: string;
  Replicas: string;
  Image: string;
  Ports: string;
  Status?: string;
  Created?: string;
  Updated?: string;
}

interface StackDetails {
  stack: string;
  services: ServiceInfo[];
  totalReplicas?: number;
  runningReplicas?: number;
  uptime?: string;
}

type ActionType = "up" | "down" | "restart" | "status";

export default function OpsTab() {
  const { user } = useAuth();
  const canOperateStacks = canAccessFeature(user?.roles, "opsActions");
  const [stacks, setStacks] = useState<Record<string, StackInfo>>({});
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState<Record<string, ActionType | null>>({});
  const [status, setStatus] = useState<StackDetails | null>(null);
  const [expandedStacks, setExpandedStacks] = useState<Record<string, boolean>>({});
  const [logText, setLogText] = useState("");
  const [logStack, setLogStack] = useState<string | null>(null);
  const [scaleService, setScaleService] = useState("");
  const [scaleReplicas, setScaleReplicas] = useState(1);
  const [logController, setLogController] = useState<AbortController | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState<NodeJS.Timeout | null>(null);

  const loadStacks = useCallback(async () => {
    if (!canOperateStacks) return;
    setLoading(true);
    try {
      const data = await listStacks();
      setStacks(data.stacks || {});
    } catch (error) {
      toast("Failed to load stacks", { variant: "error" });
    } finally {
      setLoading(false);
    }
  }, [canOperateStacks]);

  useEffect(() => {
    if (!canOperateStacks) return;
    loadStacks();
  }, [canOperateStacks, loadStacks]);

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        if (status) {
          handleAction("status", status.stack);
        }
      }, 10000); // Refresh every 10 seconds

      setRefreshInterval(interval);
      return () => clearInterval(interval);
    } else if (refreshInterval) {
      clearInterval(refreshInterval);
      setRefreshInterval(null);
    }
  }, [autoRefresh, status, refreshInterval]);

  

  if (!canOperateStacks) {
    return (
      <Panel>
        <div className="flex items-start gap-3 text-gray-600 dark:text-gray-300">
          <Lock size={18} className="mt-1 text-gray-500 dark:text-gray-400" />
          <div>
            <p className="font-semibold text-gray-800 dark:text-gray-100">
              Sie haben keine Berechtigung
            </p>
            <p className="text-sm">Operations-Aktionen erfordern die Rollen Admin oder Ops.</p>
          </div>
        </div>
      </Panel>
    );
  }

  const handleAction = async (action: ActionType, stackName: string) => {
    setActionLoading((prev) => ({ ...prev, [stackName]: action }));

    try {
      switch (action) {
        case "status":
          const statusData = await stackStatus(stackName);
          setStatus({
            stack: stackName,
            services: statusData.services || [],
            totalReplicas: statusData.services?.reduce((sum: number, s: ServiceInfo) => {
              const replicas = s.Replicas.split("/");
              return sum + parseInt(replicas[1] || "0");
            }, 0),
            runningReplicas: statusData.services?.reduce((sum: number, s: ServiceInfo) => {
              const replicas = s.Replicas.split("/");
              return sum + parseInt(replicas[0] || "0");
            }, 0),
          });
          break;
        case "up":
          await stackUp(stackName);
          toast(`Stack ${stackName} started successfully`, { variant: "success" });
          break;
        case "down":
          await stackDown(stackName);
          toast(`Stack ${stackName} stopped successfully`, { variant: "success" });
          break;
        case "restart":
          await stackRestart(stackName);
          toast(`Stack ${stackName} restarted successfully`, { variant: "success" });
          break;
      }
    } catch (error) {
      toast(`${action} action failed for ${stackName}`, { variant: "error" });
    } finally {
      setActionLoading((prev) => ({ ...prev, [stackName]: null }));
    }
  };

  const handleScale = async (stackName: string) => {
    if (!scaleService) {
      toast("Please select a service to scale", { variant: "error" });
      return;
    }

    if (scaleReplicas < 0 || scaleReplicas > 10) {
      toast("Replicas must be between 0 and 10", { variant: "error" });
      return;
    }

    setActionLoading((prev) => ({ ...prev, [stackName]: "status" }));

    try {
      await stackScale(stackName, scaleService, scaleReplicas);
      toast(`Service ${scaleService} scaled to ${scaleReplicas} replicas`, { variant: "success" });

      // Refresh status after scaling
      setTimeout(() => handleAction("status", stackName), 2000);
    } catch (error) {
      toast("Scale operation failed", { variant: "error" });
    } finally {
      setActionLoading((prev) => ({ ...prev, [stackName]: null }));
    }
  };

  const handleLogs = async (stackName: string) => {
    // Stop existing log stream
    logController?.abort();

    const controller = new AbortController();
    setLogController(controller);
    setLogText("");
    setLogStack(stackName);

    try {
      const response = await streamLogs(stackName, { signal: controller.signal });
      const reader = response.body?.getReader();

      if (!reader) {
        toast("Failed to start log stream", { variant: "error" });
        return;
      }

      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        setLogText((prev) => prev + chunk);
      }
    } catch (error: unknown) {
      const isAbortError = (err: unknown): boolean =>
        typeof err === "object" &&
        err !== null &&
        "name" in err &&
        (err as any).name === "AbortError";
      if (!isAbortError(error)) {
        toast("Log streaming failed", { variant: "error" });
      }
    }
  };

  const stopLogs = () => {
    logController?.abort();
    setLogController(null);
    setLogStack(null);
  };

  const toggleStackExpansion = (stackName: string) => {
    setExpandedStacks((prev) => ({
      ...prev,
      [stackName]: !prev[stackName],
    }));
  };

  const getServiceStatusIcon = (service: ServiceInfo) => {
    const [running, total] = service.Replicas.split("/").map(Number);

    if (running === total && running > 0) {
      return <CheckCircle size={16} className="text-green-500" />;
    } else if (running > 0 && running < total) {
      return <AlertTriangle size={16} className="text-yellow-500" />;
    } else {
      return <Clock size={16} className="text-gray-400" />;
    }
  };

  const getStackHealthStatus = (services?: ServiceInfo[]) => {
    if (!services || services.length === 0) return "unknown";

    const totalServices = services.length;
    const healthyServices = services.filter((s) => {
      const [running, total] = s.Replicas.split("/").map(Number);
      return running === total && running > 0;
    }).length;

    if (healthyServices === totalServices) return "healthy";
    if (healthyServices > 0) return "degraded";
    return "down";
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <RefreshCw size={32} className="animate-spin mx-auto mb-4 text-primary-600" />
          <p className="text-gray-600 dark:text-slate-400">Loading Docker stacks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Operations Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            Docker Stack Operations
          </h3>
          <p className="text-sm text-gray-600 dark:text-slate-400">
            All operations are audited and logged for compliance
          </p>
        </div>

        <div className="flex items-center gap-2">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded"
            />
            Auto-refresh
          </label>

          <Button variant="outline" size="sm" onClick={loadStacks} disabled={loading}>
            {loading ? <RefreshCw size={14} className="animate-spin" /> : <RefreshCw size={14} />}
          </Button>
        </div>
      </div>

      {/* Stacks Overview */}
      {Object.keys(stacks).length === 0 ? (
        <Panel>
          <div className="text-center py-8 text-gray-500 dark:text-slate-400">
            <Server size={32} className="mx-auto mb-2" />
            <p>No Docker stacks found</p>
            <p className="text-sm">Make sure Docker is running and stacks are deployed</p>
          </div>
        </Panel>
      ) : (
        Object.entries(stacks).map(([stackName, stackInfo]) => {
          const isExpanded = expandedStacks[stackName];
          const isLoading = actionLoading[stackName];
          const stackStatus = status?.stack === stackName ? status : null;
          const healthStatus = getStackHealthStatus(stackStatus?.services);

          return (
            <Panel key={stackName} className="overflow-hidden">
              {/* Stack Header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => toggleStackExpansion(stackName)}
                    className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
                  >
                    {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                  </button>

                  <div className="flex items-center gap-2">
                    <Server size={20} className="text-gray-600 dark:text-slate-400" />
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-slate-100">
                        {stackInfo.title}
                      </h4>
                      <p className="text-sm text-gray-500 dark:text-slate-400">
                        {stackName} • {stackInfo.files.length} file(s)
                      </p>
                    </div>
                  </div>

                  {stackStatus && (
                    <div
                      className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                        healthStatus === "healthy"
                          ? "bg-green-100 text-green-800"
                          : healthStatus === "degraded"
                            ? "bg-yellow-100 text-yellow-800"
                            : healthStatus === "down"
                              ? "bg-red-100 text-red-800"
                              : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {healthStatus === "healthy" && <CheckCircle size={12} />}
                      {healthStatus === "degraded" && <AlertTriangle size={12} />}
                      {healthStatus === "down" && <Clock size={12} />}
                      {healthStatus}
                    </div>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleAction("status", stackName)}
                    disabled={isLoading === "status"}
                  >
                    {isLoading === "status" ? (
                      <RefreshCw size={14} className="animate-spin" />
                    ) : (
                      <Monitor size={14} />
                    )}
                    Status
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleAction("up", stackName)}
                    disabled={isLoading === "up"}
                  >
                    {isLoading === "up" ? (
                      <RefreshCw size={14} className="animate-spin" />
                    ) : (
                      <Play size={14} />
                    )}
                    Start
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleAction("down", stackName)}
                    disabled={isLoading === "down"}
                  >
                    {isLoading === "down" ? (
                      <RefreshCw size={14} className="animate-spin" />
                    ) : (
                      <Square size={14} />
                    )}
                    Stop
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleAction("restart", stackName)}
                    disabled={isLoading === "restart"}
                  >
                    {isLoading === "restart" ? (
                      <RefreshCw size={14} className="animate-spin" />
                    ) : (
                      <RotateCcw size={14} />
                    )}
                    Restart
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => (logStack === stackName ? stopLogs() : handleLogs(stackName))}
                  >
                    {logStack === stackName ? (
                      <>
                        <EyeOff size={14} />
                        Stop Logs
                      </>
                    ) : (
                      <>
                        <Terminal size={14} />
                        Logs
                      </>
                    )}
                  </Button>
                </div>
              </div>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="p-4 space-y-4">
                  {/* Stack Files */}
                  <div>
                    <h5 className="text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                      Configuration Files
                    </h5>
                    <div className="flex flex-wrap gap-2">
                      {stackInfo.files.map((file, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded dark:bg-gray-800 dark:text-slate-400"
                        >
                          {file}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Services Status */}
                  {stackStatus && (
                    <>
                      <div>
                        <h5 className="text-sm font-medium text-gray-700 dark:text-slate-300 mb-3">
                          Services ({stackStatus.services.length})
                        </h5>

                        <div className="grid grid-cols-1 gap-3">
                          {stackStatus.services.map((service, index) => {
                            const [running, total] = service.Replicas.split("/").map(Number);

                            return (
                              <div
                                key={index}
                                className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
                              >
                                <div className="flex items-center gap-3">
                                  {getServiceStatusIcon(service)}
                                  <div>
                                    <div className="font-medium text-sm text-gray-900 dark:text-slate-100">
                                      {service.Service}
                                    </div>
                                    <div className="text-xs text-gray-500 dark:text-slate-400">
                                      {service.Image}
                                    </div>
                                  </div>
                                </div>

                                <div className="flex items-center gap-4 text-sm">
                                  <div className="text-right">
                                    <div className="font-medium text-gray-900 dark:text-slate-100">
                                      {running}/{total}
                                    </div>
                                    <div className="text-xs text-gray-500 dark:text-slate-400">
                                      replicas
                                    </div>
                                  </div>

                                  {service.Ports && (
                                    <div className="text-right">
                                      <div className="font-medium text-gray-900 dark:text-slate-100">
                                        {service.Ports}
                                      </div>
                                      <div className="text-xs text-gray-500 dark:text-slate-400">
                                        ports
                                      </div>
                                    </div>
                                  )}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* Scaling Controls */}
                      <div className="flex items-center gap-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                        <select
                          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                          value={scaleService}
                          onChange={(e) => setScaleService(e.target.value)}
                        >
                          <option value="">Select service to scale...</option>
                          {stackStatus.services.map((service) => (
                            <option key={service.Service} value={service.Service}>
                              {service.Service}
                            </option>
                          ))}
                        </select>

                        <input
                          type="number"
                          min={0}
                          max={10}
                          className="w-20 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                          value={scaleReplicas}
                          onChange={(e) => setScaleReplicas(Number(e.target.value))}
                          placeholder="Replicas"
                        />

                        <Button
                          size="sm"
                          onClick={() => handleScale(stackName)}
                          disabled={!scaleService || !!isLoading}
                        >
                          <BarChart3 size={14} className="mr-1" />
                          Scale
                        </Button>
                      </div>
                    </>
                  )}

                  {/* Live Logs */}
                  {logStack === stackName && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <h5 className="text-sm font-medium text-gray-700 dark:text-slate-300">
                          Live Logs
                        </h5>
                        <Button size="sm" variant="outline" onClick={stopLogs}>
                          <Square size={12} className="mr-1" />
                          Stop Stream
                        </Button>
                      </div>

                      <div className="bg-black text-green-400 p-3 rounded-lg max-h-64 overflow-auto font-mono text-xs">
                        {logText ? (
                          <pre className="whitespace-pre-wrap">{logText}</pre>
                        ) : (
                          <div className="flex items-center gap-2">
                            <RefreshCw size={12} className="animate-spin" />
                            Connecting to log stream...
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </Panel>
          );
        })
      )}

      {/* Operations Notice */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-900/30 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <AlertTriangle size={20} className="text-yellow-600 dark:text-yellow-400 mt-0.5" />
          <div>
            <h4 className="font-medium text-yellow-800 dark:text-yellow-300">Operations Notice</h4>
            <p className="text-sm text-yellow-700 dark:text-yellow-400 mt-1">
              All Docker operations are logged and audited for security compliance. Only authorized
              personnel should perform production operations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
