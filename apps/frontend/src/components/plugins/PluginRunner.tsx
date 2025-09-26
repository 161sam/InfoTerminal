// Plugin System Components for InfoTerminal
// Provides interface for running security and investigation tools

import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Badge } from "../ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "../ui/dialog";
import { Textarea } from "../ui/textarea";
import { Switch } from "../ui/switch";
import {
  Play,
  Square,
  Download,
  RefreshCw,
  Settings,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Terminal,
  Shield,
  Network,
  Globe,
  Search,
  Lock,
} from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { canAccessFeature } from "@/lib/auth/rbac";
import { ProgressModal } from "../feedback/ProgressModal";
import { useTaskProgress } from "@/hooks/useTaskProgress";
import { useNotifications } from "@/lib/notifications";

interface Plugin {
  name: string;
  version: string;
  description: string;
  category: string;
  author: string;
  risk_level: "low" | "medium" | "high";
  requires_network: boolean;
  requires_root: boolean;
  parameters: PluginParameter[];
  output_formats: string[];
  security: {
    timeout: number;
    memory_limit: string;
    sandbox: string;
  };
}

interface PluginParameter {
  name: string;
  type: string;
  description: string;
  required: boolean;
  default?: any;
  choices?: string[];
  validation?: string;
  example?: string;
  min?: number;
  max?: number;
}

interface Job {
  job_id: string;
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
  plugin_name: string;
  started_at?: string;
  completed_at?: string;
  execution_time?: number;
  results?: any;
  error?: string;
  graph_entities?: any[];
  search_documents?: any[];
}

interface PluginCategory {
  name: string;
  plugins: Array<{
    name: string;
    description: string;
    risk_level: string;
  }>;
  risk_levels: string[];
}

interface PluginRunnerProps {
  apiBaseUrl?: string;
  className?: string;
}

const riskLevelColors = {
  low: "bg-green-100 text-green-800",
  medium: "bg-yellow-100 text-yellow-800",
  high: "bg-red-100 text-red-800",
};

const categoryIcons = {
  network_reconnaissance: Network,
  domain_intelligence: Globe,
  vulnerability_scanning: Shield,
  default: Terminal,
};

const statusIcons = {
  queued: Clock,
  running: RefreshCw,
  completed: CheckCircle,
  failed: XCircle,
  cancelled: Square,
};

const statusColors = {
  queued: "text-blue-600",
  running: "text-yellow-600",
  completed: "text-green-600",
  failed: "text-red-600",
  cancelled: "text-gray-600",
};

export const PluginRunner: React.FC<PluginRunnerProps> = ({
  apiBaseUrl = "http://localhost:8621",
  className = "",
}) => {
  const { user } = useAuth();
  const canRunPlugins = canAccessFeature(user?.roles, "pluginRunner");
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [categories, setCategories] = useState<PluginCategory[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedPlugin, setSelectedPlugin] = useState<Plugin | null>(null);
  const [parameters, setParameters] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("plugins");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [executionDialogOpen, setExecutionDialogOpen] = useState(false);
  const [resultsDialogOpen, setResultsDialogOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [showProgressModal, setShowProgressModal] = useState(false);
  const notifications = useNotifications();

  const fetchPlugins = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/plugins`);
      if (!response.ok) throw new Error("Failed to fetch plugins");
      const data = await response.json();
      setPlugins(data.plugins || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch plugins");
    }
  }, [apiBaseUrl]);

  const fetchCategories = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/categories`);
      if (!response.ok) throw new Error("Failed to fetch categories");
      const data = await response.json();
      setCategories(data.categories || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch categories");
    }
  }, [apiBaseUrl]);

  const fetchJobs = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/jobs?limit=50`);
      if (!response.ok) throw new Error("Failed to fetch jobs");
      const data = await response.json();
      setJobs(data.jobs || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch jobs");
    }
  }, [apiBaseUrl]);

  const fetchJobDetails = useCallback(
    async (jobId: string) => {
      try {
        const response = await fetch(`${apiBaseUrl}/jobs/${jobId}`);
        if (!response.ok) throw new Error("Failed to fetch job details");
        const job = await response.json();
        setSelectedJob(job);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch job details");
      }
    },
    [apiBaseUrl],
  );

  useEffect(() => {
    if (!canRunPlugins) return;
    fetchPlugins();
    fetchCategories();
    fetchJobs();
  }, [canRunPlugins, fetchPlugins, fetchCategories, fetchJobs]);

  // Auto-refresh jobs
  useEffect(() => {
    if (!canRunPlugins) return;
    const interval = setInterval(() => {
      if (activeTab === "jobs") {
        fetchJobs();
      }
    }, 5000);
    return () => clearInterval(interval);
  }, [activeTab, canRunPlugins, fetchJobs]);

  const pollPluginJob = useCallback(async () => {
    if (!activeJobId) return null;
    try {
      const response = await fetch(`${apiBaseUrl}/jobs/${activeJobId}`);
      if (!response.ok) return null;
      const job = await response.json();
      const status = job.status as string;
      let progress = 30;
      if (status === "queued") {
        progress = 10;
      } else if (status === "running") {
        progress = 60;
        if (job.progress) {
          const numeric = parseInt(job.progress, 10);
          if (!Number.isNaN(numeric)) {
            progress = Math.min(95, Math.max(60, numeric));
          }
        }
      } else if (status === "completed") {
        progress = 100;
      } else if (status === "failed" || status === "cancelled") {
        progress = 100;
      }
      return {
        type: "plugin_job",
        job_id: job.job_id,
        status,
        message: job.progress || `Job status: ${status}`,
        progress,
      };
    } catch {
      return null;
    }
  }, [activeJobId, apiBaseUrl]);

  const jobProgress = useTaskProgress({
    active: showProgressModal,
    taskId: activeJobId,
    eventType: "plugin_job",
    poller: pollPluginJob,
    pollInterval: 3000,
    fallbackDurationMs: 12000,
    matchEvent: (event, id) => {
      const jobId = (event.job_id ?? event.jobId) as string | undefined;
      return jobId === id;
    },
  });

  const executePlugin = async () => {
    if (!selectedPlugin) return;

    setLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/execute`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          plugin_name: selectedPlugin.name,
          parameters: parameters,
          output_format: "json",
        }),
      });

      if (!response.ok) throw new Error("Failed to execute plugin");

      const result = await response.json();
      setExecutionDialogOpen(false);
      setParameters({});
      setSelectedPlugin(null);
      if (result?.job_id) {
        setActiveJobId(result.job_id);
        setShowProgressModal(true);
        jobProgress.setManualProgress(12, "running", "Pluginlauf gestartet");
      }
      fetchJobs(); // Refresh jobs list
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to execute plugin");
    } finally {
      setLoading(false);
    }
  };

  const cancelJob = React.useCallback(async (jobId: string) => {
    try {
      const response = await fetch(`${apiBaseUrl}/jobs/${jobId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to cancel job");
      fetchJobs(); // Refresh jobs list
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to cancel job");
    }
  }, [apiBaseUrl, fetchJobs]);

  const handleCancelActiveJob = useCallback(async () => {
    if (!activeJobId) return;
    await cancelJob(activeJobId);
    jobProgress.setManualProgress(100, "failed", "Pluginlauf abgebrochen");
    notifications.info("Pluginlauf abgebrochen");
    setActiveJobId(null);
    setShowProgressModal(false);
  }, [activeJobId, cancelJob, jobProgress, notifications]);

  useEffect(() => {
    if (!activeJobId) return;
    const status = jobProgress.state.status;
    if (status === "completed") {
      notifications.success("Plugin fertig", "Der Pluginlauf wurde abgeschlossen.");
      fetchJobs();
      setTimeout(() => {
        setShowProgressModal(false);
        setActiveJobId(null);
      }, 1500);
    } else if (status === "failed") {
      notifications.error("Plugin fehlgeschlagen", jobProgress.state.error || "Job fehlgeschlagen");
      fetchJobs();
    }
  }, [activeJobId, jobProgress.state.status, jobProgress.state.error, fetchJobs, notifications]);

  if (!canRunPlugins) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-gray-100">
            <Lock size={18} />
            Sie haben keine Berechtigung
          </CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-gray-600 dark:text-gray-300">
          Plugin-Ausführungen sind nur für Admin- oder Ops-Rollen verfügbar.
        </CardContent>
      </Card>
    );
  }

  const downloadResults = (job: Job) => {
    const blob = new Blob([JSON.stringify(job.results, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${job.plugin_name}_${job.job_id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const renderParameterInput = (param: PluginParameter) => {
    const value = parameters[param.name] || param.default || "";

    if (param.type === "boolean") {
      return (
        <div className="flex items-center space-x-2">
          <Switch
            id={param.name}
            checked={value}
            onCheckedChange={(checked) =>
              setParameters((prev) => ({ ...prev, [param.name]: checked }))
            }
          />
          <label htmlFor={param.name} className="text-sm">
            {param.description}
          </label>
        </div>
      );
    }

    if (param.choices) {
      return (
        <Select
          value={value}
          onValueChange={(val) => setParameters((prev) => ({ ...prev, [param.name]: val }))}
        >
          <SelectTrigger>
            <SelectValue placeholder={`Select ${param.name}`} />
          </SelectTrigger>
          <SelectContent>
            {param.choices.map((choice) => (
              <SelectItem key={choice} value={choice}>
                {choice}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      );
    }

    if (param.type === "integer") {
      return (
        <Input
          type="number"
          min={param.min}
          max={param.max}
          value={value}
          onChange={(e) =>
            setParameters((prev) => ({ ...prev, [param.name]: Number(e.target.value) }))
          }
          placeholder={param.example}
        />
      );
    }

    return (
      <Input
        type="text"
        value={value}
        onChange={(e) => setParameters((prev) => ({ ...prev, [param.name]: e.target.value }))}
        placeholder={param.example}
      />
    );
  };

  const filteredPlugins = plugins.filter(
    (plugin) => selectedCategory === "all" || plugin.category === selectedCategory,
  );

  const renderPluginsTab = () => (
    <div className="space-y-6">
      {/* Category Filter */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium">Category:</label>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-64">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category.name} value={category.name}>
                    {category.name.replace(/_/g, " ")} ({category.plugins.length})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Plugin Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredPlugins.map((plugin) => {
          const IconComponent =
            categoryIcons[plugin.category as keyof typeof categoryIcons] || categoryIcons.default;

          return (
            <Card key={plugin.name} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <IconComponent className="h-5 w-5" />
                    <CardTitle className="text-lg">{plugin.name}</CardTitle>
                  </div>
                  <Badge className={riskLevelColors[plugin.risk_level]}>{plugin.risk_level}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-gray-600">{plugin.description}</p>

                <div className="flex flex-wrap gap-2">
                  <Badge variant="outline">{plugin.category.replace(/_/g, " ")}</Badge>
                  <Badge variant="outline">v{plugin.version}</Badge>
                  {plugin.requires_network && <Badge variant="outline">Network</Badge>}
                  {plugin.requires_root && <Badge variant="outline">Root</Badge>}
                </div>

                <div className="text-xs text-gray-500">
                  <div>Timeout: {plugin.security.timeout}s</div>
                  <div>Memory: {plugin.security.memory_limit}</div>
                  <div>Sandbox: {plugin.security.sandbox}</div>
                </div>

                <Button
                  onClick={() => {
                    setSelectedPlugin(plugin);
                    setParameters({});
                    setExecutionDialogOpen(true);
                  }}
                  className="w-full"
                  variant={plugin.risk_level === "high" ? "destructive" : "default"}
                >
                  <Play className="h-4 w-4 mr-2" />
                  Run Plugin
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );

  const renderJobsTab = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Execution Jobs</CardTitle>
            <Button onClick={fetchJobs} variant="outline" size="sm">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {jobs.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                No jobs found. Run a plugin to see execution results here.
              </div>
            ) : (
              jobs.map((job) => {
                const StatusIcon = statusIcons[job.status];
                const statusColor = statusColors[job.status];

                return (
                  <Card key={job.job_id} className="border-l-4 border-l-blue-500">
                    <CardContent className="pt-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <StatusIcon
                            className={`h-5 w-5 ${statusColor} ${job.status === "running" ? "animate-spin" : ""}`}
                          />
                          <div>
                            <div className="font-medium">{job.plugin_name}</div>
                            <div className="text-sm text-gray-500">Job ID: {job.job_id}</div>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className={statusColor}>
                            {job.status}
                          </Badge>

                          {job.status === "completed" && (
                            <>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={async () => {
                                  await fetchJobDetails(job.job_id);
                                  setResultsDialogOpen(true);
                                }}
                              >
                                <Search className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => downloadResults(job)}
                              >
                                <Download className="h-4 w-4" />
                              </Button>
                            </>
                          )}

                          {(job.status === "queued" || job.status === "running") && (
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => cancelJob(job.job_id)}
                            >
                              <Square className="h-4 w-4" />
                            </Button>
                          )}
                        </div>
                      </div>

                      {job.execution_time && (
                        <div className="mt-2 text-sm text-gray-600">
                          Execution time: {job.execution_time.toFixed(2)}s
                        </div>
                      )}

                      {job.error && (
                        <div className="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded">
                          {job.error}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                );
              })
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className={`w-full ${className}`}>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="plugins">Available Plugins</TabsTrigger>
          <TabsTrigger value="jobs">Execution Jobs</TabsTrigger>
        </TabsList>

        <TabsContent value="plugins" className="mt-6">
          {renderPluginsTab()}
        </TabsContent>

        <TabsContent value="jobs" className="mt-6">
          {renderJobsTab()}
        </TabsContent>
      </Tabs>

      {/* Execution Dialog */}
      <Dialog open={executionDialogOpen} onOpenChange={setExecutionDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Terminal className="h-5 w-5" />
              Execute {selectedPlugin?.name}
              <Badge className={riskLevelColors[selectedPlugin?.risk_level || "low"]}>
                {selectedPlugin?.risk_level}
              </Badge>
            </DialogTitle>
          </DialogHeader>

          {selectedPlugin && (
            <div className="space-y-6">
              <div className="text-sm text-gray-600">{selectedPlugin.description}</div>

              {selectedPlugin.risk_level === "high" && (
                <div className="bg-red-50 border border-red-200 rounded p-3 flex items-start gap-2">
                  <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5" />
                  <div className="text-sm text-red-700">
                    <strong>High Risk Plugin:</strong> This plugin may perform potentially harmful
                    operations. Use with caution and ensure you understand the implications.
                  </div>
                </div>
              )}

              <div className="space-y-4">
                <h4 className="font-medium">Parameters:</h4>
                {selectedPlugin.parameters.map((param) => (
                  <div key={param.name} className="space-y-2">
                    <label className="text-sm font-medium">
                      {param.name}
                      {param.required && <span className="text-red-500">*</span>}
                    </label>
                    {renderParameterInput(param)}
                    <p className="text-xs text-gray-500">{param.description}</p>
                  </div>
                ))}
              </div>

              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setExecutionDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={executePlugin} disabled={loading}>
                  {loading ? (
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  ) : (
                    <Play className="h-4 w-4 mr-2" />
                  )}
                  Execute Plugin
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Results Dialog */}
      <Dialog open={resultsDialogOpen} onOpenChange={setResultsDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Job Results: {selectedJob?.plugin_name}</DialogTitle>
          </DialogHeader>

          {selectedJob && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <strong>Status:</strong> {selectedJob.status}
                </div>
                <div>
                  <strong>Execution Time:</strong> {selectedJob.execution_time?.toFixed(2)}s
                </div>
                <div>
                  <strong>Started:</strong>{" "}
                  {selectedJob.started_at
                    ? new Date(selectedJob.started_at).toLocaleString()
                    : "N/A"}
                </div>
                <div>
                  <strong>Completed:</strong>{" "}
                  {selectedJob.completed_at
                    ? new Date(selectedJob.completed_at).toLocaleString()
                    : "N/A"}
                </div>
              </div>

              {selectedJob.graph_entities && selectedJob.graph_entities.length > 0 && (
                <div>
                  <h4 className="font-medium mb-2">
                    Graph Entities ({selectedJob.graph_entities.length})
                  </h4>
                  <div className="bg-gray-50 p-3 rounded text-sm max-h-40 overflow-y-auto">
                    {selectedJob.graph_entities.map((entity, idx) => (
                      <div key={idx} className="flex items-center gap-2 mb-1">
                        <Badge variant="secondary">{entity.type}</Badge>
                        <span>{entity.id}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {selectedJob.results && (
                <div>
                  <h4 className="font-medium mb-2">Raw Results</h4>
                  <Textarea
                    value={JSON.stringify(selectedJob.results, null, 2)}
                    readOnly
                    className="min-h-96 font-mono text-xs"
                  />
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>

      <ProgressModal
        isOpen={showProgressModal}
        title="Plugin-Ausführung"
        description={activeJobId ? `Job-ID: ${activeJobId}` : undefined}
        state={jobProgress.state}
        onClose={() => {
          setShowProgressModal(false);
          setActiveJobId(null);
        }}
        onCancel={handleCancelActiveJob}
        cancelLabel="Job abbrechen"
        successLabel="Schließen"
      />

      {error && (
        <div className="fixed bottom-4 right-4 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded shadow-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default PluginRunner;
