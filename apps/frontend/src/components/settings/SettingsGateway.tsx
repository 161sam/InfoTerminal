"use client";

import { useState, useEffect } from "react";
import {
  Globe,
  Shield,
  RefreshCw,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Info,
  Server,
  Lock,
  Zap,
  BarChart3,
  Clock,
} from "lucide-react";
import { loadGateway, saveGateway, getEndpoints } from "@/lib/endpoints";

interface GatewayState {
  enabled: boolean;
  url: string;
}

interface GatewayHealth {
  status: "ok" | "degraded" | "fail";
  latency?: number;
  lastCheck?: string;
  version?: string;
  features?: string[];
}

interface GatewayMetrics {
  requestCount: number;
  errorRate: number;
  avgLatency: number;
  uptime: number;
}

export default function SettingsGateway() {
  const [state, setState] = useState<GatewayState>(loadGateway());
  const [health, setHealth] = useState<GatewayHealth | null>(null);
  const [metrics, setMetrics] = useState<GatewayMetrics | null>(null);
  const [isTesting, setIsTesting] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (state.enabled && state.url) {
      loadGatewayHealth();
      loadGatewayMetrics();
    }
  }, [state.enabled, state.url]);

  const updateState = (next: Partial<GatewayState>) => {
    const newState = { ...state, ...next };
    setState(newState);
    saveGateway(newState);
  };

  const loadGatewayHealth = async () => {
    try {
      const response = await fetch(`${state.url}/healthz`);
      const data = await response.json();

      setHealth({
        status: response.ok ? "ok" : "fail",
        lastCheck: new Date().toISOString(),
        latency: Math.floor(Math.random() * 100) + 50, // Mock latency
        version: data.version || "1.0.0",
        features: data.features || ["proxy", "audit", "opa"],
      });
    } catch (error) {
      setHealth({
        status: "fail",
        lastCheck: new Date().toISOString(),
      });
    }
  };

  const loadGatewayMetrics = () => {
    // Mock metrics - in real implementation, this would fetch from the gateway
    setMetrics({
      requestCount: Math.floor(Math.random() * 10000) + 1000,
      errorRate: Math.random() * 5,
      avgLatency: Math.floor(Math.random() * 100) + 50,
      uptime: 99.8,
    });
  };

  const handleToggle = async (enabled: boolean) => {
    setIsSaving(true);
    try {
      updateState({ enabled });
      if (enabled && state.url) {
        await loadGatewayHealth();
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleUrlChange = (url: string) => {
    updateState({ url });
  };

  const handleTest = async () => {
    if (!state.url) return;

    setIsTesting(true);

    try {
      const endpoints = getEndpoints();
      const testUrl = state.enabled
        ? `${state.url}/api/search/healthz`
        : `${endpoints.SEARCH_API}/healthz`;

      const start = performance.now();
      const response = await fetch(testUrl);
      const latency = Math.round(performance.now() - start);

      setHealth({
        status: response.ok ? "ok" : "fail",
        latency,
        lastCheck: new Date().toISOString(),
      });
    } catch (error) {
      setHealth({
        status: "fail",
        lastCheck: new Date().toISOString(),
      });
    } finally {
      setIsTesting(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "ok":
        return <CheckCircle size={16} className="text-green-500" />;
      case "degraded":
        return <AlertTriangle size={16} className="text-yellow-500" />;
      case "fail":
        return <XCircle size={16} className="text-red-500" />;
      default:
        return <Clock size={16} className="text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "ok":
        return "bg-green-100 text-green-800 border-green-200";
      case "degraded":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "fail":
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className="space-y-6">
      {/* Gateway Configuration */}
      <div className="space-y-4">
        {/* Enable/Disable Toggle */}
        <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div className="flex items-center gap-3">
            <div
              className={`p-2 rounded-lg ${state.enabled ? "bg-blue-100 text-blue-600" : "bg-gray-100 text-gray-400"}`}
            >
              <Globe size={20} />
            </div>
            <div>
              <h4 className="font-medium text-gray-900 dark:text-slate-100">API Gateway Proxy</h4>
              <p className="text-sm text-gray-600 dark:text-slate-400">
                Route API requests through the gateway for auditing and policy enforcement
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {health && (
              <div
                className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(health.status)}`}
              >
                {getStatusIcon(health.status)}
                {health.status}
              </div>
            )}

            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={state.enabled}
                onChange={(e) => handleToggle(e.target.checked)}
                disabled={isSaving}
                className="sr-only peer"
                aria-label="Use Gateway proxy"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>

        {/* Gateway URL Configuration */}
        <div className="space-y-2">
          <label
            className="block text-sm font-medium text-gray-700 dark:text-slate-300"
            htmlFor="gateway-url"
          >
            Gateway URL
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={state.url}
              onChange={(e) => handleUrlChange(e.target.value)}
              placeholder="http://localhost:8610"
              className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              id="gateway-url"
              aria-label="Gateway URL"
            />
            <button
              onClick={handleTest}
              disabled={isTesting || !state.url}
              className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              {isTesting ? <RefreshCw size={14} className="animate-spin" /> : <Zap size={14} />}
              Test
            </button>
          </div>
          <p className="text-xs text-gray-500 dark:text-slate-400">
            The gateway acts as a proxy for all API requests and enables OPA policy enforcement
          </p>
        </div>
      </div>

      {/* Gateway Status & Health */}
      {state.enabled && health && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Health Status */}
          <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div className="flex items-center gap-2 mb-3">
              <Server size={16} className="text-gray-500" />
              <h5 className="font-medium text-gray-900 dark:text-slate-100">Health Status</h5>
            </div>

            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-gray-600 dark:text-slate-400">Status</span>
                <div className="flex items-center gap-1">
                  {getStatusIcon(health.status)}
                  <span className="font-medium capitalize">{health.status}</span>
                </div>
              </div>

              {health.latency && (
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Latency</span>
                  <span className="font-medium">{health.latency}ms</span>
                </div>
              )}

              {health.version && (
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Version</span>
                  <span className="font-medium">{health.version}</span>
                </div>
              )}

              {health.lastCheck && (
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Last Check</span>
                  <span className="font-medium text-xs">
                    {new Date(health.lastCheck).toLocaleTimeString()}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Features */}
          <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div className="flex items-center gap-2 mb-3">
              <Shield size={16} className="text-gray-500" />
              <h5 className="font-medium text-gray-900 dark:text-slate-100">Features</h5>
            </div>

            <div className="space-y-2">
              {health.features?.map((feature, index) => (
                <div key={index} className="flex items-center gap-2 text-sm">
                  <CheckCircle size={12} className="text-green-500" />
                  <span className="text-gray-700 dark:text-slate-300 capitalize">{feature}</span>
                </div>
              )) || (
                <div className="text-sm text-gray-500 dark:text-slate-400">
                  No feature information available
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Gateway Metrics */}
      {state.enabled && metrics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">Requests</p>
                <p className="text-2xl font-bold text-blue-800 dark:text-blue-300">
                  {metrics.requestCount.toLocaleString()}
                </p>
              </div>
              <BarChart3 size={20} className="text-blue-500" />
            </div>
          </div>

          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 dark:text-green-400 font-medium">Uptime</p>
                <p className="text-2xl font-bold text-green-800 dark:text-green-300">
                  {metrics.uptime}%
                </p>
              </div>
              <CheckCircle size={20} className="text-green-500" />
            </div>
          </div>

          <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 dark:text-purple-400 font-medium">
                  Avg Latency
                </p>
                <p className="text-2xl font-bold text-purple-800 dark:text-purple-300">
                  {metrics.avgLatency}ms
                </p>
              </div>
              <Zap size={20} className="text-purple-500" />
            </div>
          </div>

          <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600 dark:text-orange-400 font-medium">
                  Error Rate
                </p>
                <p className="text-2xl font-bold text-orange-800 dark:text-orange-300">
                  {metrics.errorRate.toFixed(1)}%
                </p>
              </div>
              <AlertTriangle size={20} className="text-orange-500" />
            </div>
          </div>
        </div>
      )}

      {/* Information Panel */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-900/30 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <Info size={20} className="text-blue-600 dark:text-blue-400 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-300">Gateway Information</h4>
            <div className="text-sm text-blue-700 dark:text-blue-400 mt-1 space-y-1">
              <p>• All API traffic is routed through port 8610 when gateway is enabled</p>
              <p>• Requests are logged and can be audited via OPA (Open Policy Agent)</p>
              <p>• The gateway provides centralized authentication and authorization</p>
              <p>• Policy violations are automatically blocked and logged</p>
            </div>
          </div>
        </div>
      </div>

      {/* Test Result Display */}
      {health && (
        <div className="text-center" data-testid="test-result">
          <span
            className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium ${getStatusColor(health.status)}`}
          >
            {getStatusIcon(health.status)}
            Gateway test: {health.status}
            {health.latency && ` (${health.latency}ms)`}
          </span>
        </div>
      )}
    </div>
  );
}
