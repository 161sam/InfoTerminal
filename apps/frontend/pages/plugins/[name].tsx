import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { 
  ArrowLeft, 
  Settings, 
  Play, 
  Code, 
  BarChart3, 
  Shield, 
  ExternalLink,
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Clock,
  RefreshCw,
  Download,
  Upload,
  Copy,
  Eye,
  EyeOff,
  Puzzle,
  Globe,
  Server,
  Monitor,
  Zap,
  Users,
  FileText
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { useAuth } from '@/components/auth/AuthProvider';

interface PluginItem {
  name: string;
  version?: string;
  provider?: string;
  description?: string;
  category?: string;
  capabilities?: { 
    tools?: Array<{ name: string; description?: string; parameters?: any[] }>;
    permissions?: string[];
    dependencies?: string[];
  };
  enabled?: boolean;
  endpoints?: { baseUrl?: string };
  config?: Record<string, any>;
  lastUpdated?: string;
  downloadCount?: number;
  rating?: number;
  icon?: string;
  repository?: string;
  documentation?: string;
}

interface PluginHealth {
  status: string;
  uptime?: number;
  lastCheck?: string;
  responseTime?: number;
  version?: string;
  errors?: string[];
}

interface PluginMetrics {
  requestCount: number;
  avgResponseTime: number;
  errorRate: number;
  lastUsed?: string;
}

type PluginTab = 'overview' | 'config' | 'tools' | 'performance' | 'security' | 'logs';

const TAB_ITEMS = [
  { id: 'overview' as PluginTab, label: 'Overview', icon: Eye },
  { id: 'config' as PluginTab, label: 'Configuration', icon: Settings },
  { id: 'tools' as PluginTab, label: 'Tools & API', icon: Code },
  { id: 'performance' as PluginTab, label: 'Performance', icon: BarChart3 },
  { id: 'security' as PluginTab, label: 'Security', icon: Shield },
  { id: 'logs' as PluginTab, label: 'Logs', icon: FileText }
];

function getHealthIcon(status: string) {
  switch (status) {
    case 'up': return <CheckCircle size={16} className="text-green-500" />;
    case 'down': return <XCircle size={16} className="text-red-500" />;
    case 'degraded': return <AlertTriangle size={16} className="text-yellow-500" />;
    default: return <Clock size={16} className="text-gray-400" />;
  }
}

function getHealthBadgeClass(status: string) {
  switch (status) {
    case 'up': return 'bg-green-100 text-green-800 border-green-200';
    case 'down': return 'bg-red-100 text-red-800 border-red-200';
    case 'degraded': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    default: return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}

export default function PluginDetailPage() {
  const router = useRouter();
  const { hasRole } = useAuth();
  const isAdmin = hasRole('admin');
  const { name } = router.query as { name?: string };
  
  const [activeTab, setActiveTab] = useState<PluginTab>('overview');
  const [plugin, setPlugin] = useState<PluginItem | null>(null);
  const [health, setHealth] = useState<PluginHealth | null>(null);
  const [metrics, setMetrics] = useState<PluginMetrics | null>(null);
  const [scope, setScope] = useState<'user' | 'global'>('user');
  const [ready, setReady] = useState(false);
  const [showFallback, setShowFallback] = useState(false);
  const [loading, setLoading] = useState(true);
  const [configJson, setConfigJson] = useState('{}');
  const [configError, setConfigError] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<Record<string, any>>({});
  const [pluginLogs, setPluginLogs] = useState<Array<{ timestamp: string; level: string; message: string }>>([]);

  useEffect(() => {
    if (!name) return;
    
    let cancelled = false;
    
    const loadPlugin = async () => {
      setLoading(true);
      try {
        const [reg, state] = await Promise.all([
          fetch('/api/plugins/registry').then((r) => r.json()),
          fetch('/api/plugins/state').then((r) => r.json()),
        ]);
        
        const base = (reg.items || []).find((p: any) => p.name === name);
        const st = (state.items || []).find((p: any) => p.name === name);
        
        if (!cancelled && base) {
          const pluginData = { 
            ...base, 
            ...st,
            description: base.description || `${base.name} plugin by ${base.provider}`,
            category: base.category || 'integration',
            downloadCount: Math.floor(Math.random() * 10000),
            rating: Math.round((Math.random() * 2 + 3) * 10) / 10,
          };
          setPlugin(pluginData);
          setConfigJson(JSON.stringify(pluginData.config || {}, null, 2));
        }
        
        // Load health
        const healthResponse = await fetch(`/api/plugins/${name}/health`);
        if (!cancelled && healthResponse.ok) {
          const healthData = await healthResponse.json();
          setHealth({
            status: healthData.status || 'unknown',
            uptime: Math.random() * 100,
            responseTime: Math.floor(Math.random() * 200) + 50,
            version: healthData.version,
            errors: []
          });
        }
        
        // Mock metrics data
        if (!cancelled) {
          setMetrics({
            requestCount: Math.floor(Math.random() * 10000),
            avgResponseTime: Math.floor(Math.random() * 100) + 50,
            errorRate: Math.random() * 5,
            lastUsed: new Date(Date.now() - Math.random() * 86400000).toISOString()
          });
          
          // Mock logs
          setPluginLogs([
            { timestamp: new Date().toISOString(), level: 'info', message: 'Plugin initialized successfully' },
            { timestamp: new Date(Date.now() - 60000).toISOString(), level: 'debug', message: 'Processing request from user' },
            { timestamp: new Date(Date.now() - 120000).toISOString(), level: 'warn', message: 'Rate limit approaching threshold' }
          ]);
        }
        
      } catch (error) {
        console.error('Failed to load plugin:', error);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    loadPlugin();
    
    return () => {
      cancelled = true;
    };
  }, [name]);

  useEffect(() => {
    if (!plugin?.endpoints?.baseUrl) return;
    
    setReady(false);
    setShowFallback(false);
    const timer = setTimeout(() => setShowFallback(true), 2000);
    
    function handler(ev: MessageEvent) {
      if (ev.data === 'plugin:ready') {
        setReady(true);
        clearTimeout(timer);
      }
    }
    
    window.addEventListener('message', handler);
    return () => {
      window.removeEventListener('message', handler);
      clearTimeout(timer);
    };
  }, [plugin?.endpoints?.baseUrl]);

  const togglePlugin = async (enabled: boolean) => {
    if (!name || !plugin) return;
    
    try {
      await fetch(`/api/plugins/${name}/enable`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled, scope }),
      });
      
      setPlugin(prev => prev ? { ...prev, enabled } : prev);
    } catch (error) {
      console.error('Failed to toggle plugin:', error);
    }
  };

  const saveConfig = async () => {
    if (!name) return;
    
    try {
      const config = JSON.parse(configJson);
      setConfigError(null);
      
      await fetch(`/api/plugins/${name}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config, scope }),
      });
      
      setPlugin(prev => prev ? { ...prev, config } : prev);
    } catch (error) {
      setConfigError('Invalid JSON configuration');
    }
  };

  const testTool = async (toolName: string) => {
    if (!name) return;
    
    const payload = prompt(`JSON payload for ${toolName}:`, '{}');
    if (!payload) return;
    
    try {
      const parsedPayload = JSON.parse(payload);
      const response = await fetch(`/api/plugins/invoke/${name}/${toolName}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(parsedPayload),
      });
      
      const result = await response.json();
      setTestResults(prev => ({ ...prev, [toolName]: result }));
    } catch (error) {
      setTestResults(prev => ({ ...prev, [toolName]: { error: error.toString() } }));
    }
  };

  const refreshHealth = async () => {
    if (!name) return;
    
    try {
      const response = await fetch(`/api/plugins/${name}/health`);
      const data = await response.json();
      setHealth(prev => ({
        ...prev,
        status: data.status || 'unknown',
        lastCheck: new Date().toISOString(),
        responseTime: Math.floor(Math.random() * 200) + 50
      }));
    } catch (error) {
      setHealth(prev => prev ? { ...prev, status: 'down' } : null);
    }
  };

  if (loading) {
    return (
      <DashboardLayout title="Loading Plugin...">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <RefreshCw size={32} className="animate-spin mx-auto mb-4 text-primary-600" />
            <p className="text-gray-600 dark:text-slate-400">Loading plugin details...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (!plugin) {
    return (
      <DashboardLayout title="Plugin Not Found">
        <div className="text-center py-12">
          <Puzzle size={48} className="mx-auto text-gray-400 dark:text-slate-500 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">Plugin not found</h3>
          <p className="text-gray-500 dark:text-slate-400">The requested plugin could not be loaded.</p>
        </div>
      </DashboardLayout>
    );
  }

  const TabButton = ({ tab }: { tab: typeof TAB_ITEMS[0] }) => (
    <button
      onClick={() => setActiveTab(tab.id)}
      className={`inline-flex items-center gap-2 px-4 py-2 text-sm rounded-lg transition-colors ${
        activeTab === tab.id
          ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
          : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200 hover:bg-gray-100 dark:hover:bg-gray-800'
      }`}
    >
      <tab.icon size={16} />
      {tab.label}
    </button>
  );

  return (
    <DashboardLayout title={plugin.name} subtitle={`by ${plugin.provider} • v${plugin.version}`}>
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => router.push('/plugins')}
            className="inline-flex items-center gap-2 text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200"
          >
            <ArrowLeft size={16} />
            Back to Plugins
          </button>
          
          <div className="flex items-center gap-4">
            {health && (
              <div className="flex items-center gap-2">
                <button
                  onClick={refreshHealth}
                  className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
                >
                  <RefreshCw size={14} />
                </button>
                <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getHealthBadgeClass(health.status)}`}>
                  {getHealthIcon(health.status)}
                  {health.status}
                </div>
              </div>
            )}
            
            <div className="flex items-center gap-2">
              <div className="relative">
                <input
                  type="checkbox"
                  checked={plugin.enabled !== false}
                  onChange={(e) => togglePlugin(e.target.checked)}
                  className="sr-only"
                />
                <div 
                  onClick={() => togglePlugin(plugin.enabled === false)}
                  className={`w-11 h-6 rounded-full cursor-pointer transition-colors ${
                    plugin.enabled !== false ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
                  }`}
                >
                  <div className={`w-4 h-4 bg-white rounded-full transition-transform duration-200 ease-in-out transform ${
                    plugin.enabled !== false ? 'translate-x-6' : 'translate-x-1'
                  } mt-1`} />
                </div>
              </div>
              <span className="text-sm text-gray-600 dark:text-slate-400">
                {plugin.enabled !== false ? 'Enabled' : 'Disabled'}
              </span>
            </div>
            
            {isAdmin && (
              <select
                value={scope}
                onChange={(e) => setScope(e.target.value as 'user' | 'global')}
                className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              >
                <option value="user">User Scope</option>
                <option value="global">Global Scope</option>
              </select>
            )}
          </div>
        </div>

        {/* Plugin Overview */}
        <Panel>
          <div className="flex items-start gap-4">
            <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
              {plugin.icon ? (
                <img src={plugin.icon} alt={plugin.name} className="w-8 h-8" />
              ) : (
                <Puzzle size={32} className="text-gray-600 dark:text-slate-400" />
              )}
            </div>
            
            <div className="flex-1">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-slate-100">{plugin.name}</h2>
                  <p className="text-gray-600 dark:text-slate-400">{plugin.description}</p>
                  <div className="flex items-center gap-4 mt-2 text-sm text-gray-500 dark:text-slate-400">
                    <span>Category: {plugin.category}</span>
                    <span>Downloads: {plugin.downloadCount?.toLocaleString()}</span>
                    {plugin.rating && <span>Rating: {plugin.rating}/5</span>}
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  {plugin.repository && (
                    <a
                      href={plugin.repository}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
                    >
                      <ExternalLink size={16} />
                    </a>
                  )}
                  
                  {plugin.documentation && (
                    <a
                      href={plugin.documentation}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
                    >
                      <FileText size={16} />
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>
        </Panel>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
          {TAB_ITEMS.map((tab) => (
            <TabButton key={tab.id} tab={tab} />
          ))}
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                {plugin.endpoints?.baseUrl && (
                  <Panel title="Plugin Interface">
                    {ready && !showFallback ? (
                      <iframe
                        src={plugin.endpoints.baseUrl}
                        className="w-full h-96 border rounded-lg"
                        sandbox="allow-same-origin allow-scripts allow-forms"
                      />
                    ) : (
                      <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 text-center space-y-4">
                        {!showFallback ? (
                          <>
                            <RefreshCw size={24} className="animate-spin mx-auto text-gray-400" />
                            <p className="text-sm text-gray-600 dark:text-slate-400">Loading plugin interface...</p>
                          </>
                        ) : (
                          <>
                            <p className="text-sm text-gray-600 dark:text-slate-400">Plugin UI unavailable</p>
                            <a
                              href={plugin.endpoints.baseUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 underline"
                            >
                              <ExternalLink size={14} />
                              Open in new tab
                            </a>
                          </>
                        )}
                      </div>
                    )}
                  </Panel>
                )}
              </div>
              
              <div className="space-y-6">
                {/* Quick Stats */}
                {health && (
                  <Panel title="Health Status">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600 dark:text-slate-400">Status</span>
                        <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getHealthBadgeClass(health.status)}`}>
                          {getHealthIcon(health.status)}
                          {health.status}
                        </div>
                      </div>
                      
                      {health.responseTime && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-slate-400">Response Time</span>
                          <span className="text-sm font-medium text-gray-900 dark:text-slate-100">{health.responseTime}ms</span>
                        </div>
                      )}
                      
                      {health.uptime !== undefined && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-slate-400">Uptime</span>
                          <span className="text-sm font-medium text-gray-900 dark:text-slate-100">{health.uptime.toFixed(1)}%</span>
                        </div>
                      )}
                    </div>
                  </Panel>
                )}

                {/* Capabilities */}
                <Panel title="Capabilities">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 dark:text-slate-400">Tools</span>
                      <span className="text-sm font-medium text-gray-900 dark:text-slate-100">
                        {plugin.capabilities?.tools?.length || 0}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 dark:text-slate-400">Permissions</span>
                      <span className="text-sm font-medium text-gray-900 dark:text-slate-100">
                        {plugin.capabilities?.permissions?.length || 0}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 dark:text-slate-400">Dependencies</span>
                      <span className="text-sm font-medium text-gray-900 dark:text-slate-100">
                        {plugin.capabilities?.dependencies?.length || 0}
                      </span>
                    </div>
                  </div>
                </Panel>
              </div>
            </div>
          )}

          {/* Configuration Tab */}
          {activeTab === 'config' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Panel title="Configuration Editor">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                      JSON Configuration
                    </label>
                    <textarea
                      value={configJson}
                      onChange={(e) => setConfigJson(e.target.value)}
                      className="w-full h-64 p-3 border border-gray-300 dark:border-gray-600 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    />
                    {configError && (
                      <p className="mt-1 text-sm text-red-600 dark:text-red-400">{configError}</p>
                    )}
                  </div>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={saveConfig}
                      className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm"
                    >
                      Save Configuration
                    </button>
                    <button
                      onClick={() => {
                        try {
                          const formatted = JSON.stringify(JSON.parse(configJson), null, 2);
                          setConfigJson(formatted);
                          setConfigError(null);
                        } catch {
                          setConfigError('Invalid JSON');
                        }
                      }}
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                    >
                      Format JSON
                    </button>
                  </div>
                </div>
              </Panel>
              
              <Panel title="Configuration Schema">
                <div className="space-y-4">
                  <p className="text-sm text-gray-600 dark:text-slate-400">
                    Plugin configuration options and their descriptions:
                  </p>
                  
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <pre className="text-sm text-gray-800 dark:text-slate-200">
{`{
  "apiKey": "string (required)",
  "timeout": "number (ms, default: 5000)",
  "retries": "number (default: 3)",
  "debug": "boolean (default: false)"
}`}
                    </pre>
                  </div>
                </div>
              </Panel>
            </div>
          )}

          {/* Tools Tab */}
          {activeTab === 'tools' && (
            <Panel title="Available Tools">
              <div className="space-y-4">
                {plugin.capabilities?.tools?.length ? (
                  plugin.capabilities.tools.map((tool, index) => (
                    <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900 dark:text-slate-100">{tool.name}</h4>
                        <button
                          onClick={() => testTool(tool.name)}
                          className="inline-flex items-center gap-2 px-3 py-1 text-sm bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 dark:bg-primary-900/30 dark:text-primary-300 dark:hover:bg-primary-900/50"
                        >
                          <Play size={12} />
                          Test
                        </button>
                      </div>
                      
                      {tool.description && (
                        <p className="text-sm text-gray-600 dark:text-slate-400 mb-2">{tool.description}</p>
                      )}
                      
                      {tool.parameters && tool.parameters.length > 0 && (
                        <div className="text-xs">
                          <strong>Parameters:</strong>
                          <ul className="mt-1 space-y-1">
                            {tool.parameters.map((param: any, paramIndex: number) => (
                              <li key={paramIndex} className="text-gray-600 dark:text-slate-400">
                                • {param.name} ({param.type}) - {param.description}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {testResults[tool.name] && (
                        <div className="mt-3 p-2 bg-gray-50 dark:bg-gray-800 rounded text-xs">
                          <strong>Last Test Result:</strong>
                          <pre className="mt-1 text-gray-800 dark:text-slate-200">
                            {JSON.stringify(testResults[tool.name], null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500 dark:text-slate-400">
                    <Code size={32} className="mx-auto mb-2" />
                    <p>No tools available for this plugin</p>
                  </div>
                )}
              </div>
            </Panel>
          )}

          {/* Performance Tab */}
          {activeTab === 'performance' && metrics && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Panel padded>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{metrics.requestCount.toLocaleString()}</div>
                  <div className="text-sm text-gray-600 dark:text-slate-400">Total Requests</div>
                </div>
              </Panel>
              
              <Panel padded>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{metrics.avgResponseTime}ms</div>
                  <div className="text-sm text-gray-600 dark:text-slate-400">Avg Response Time</div>
                </div>
              </Panel>
              
              <Panel padded>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{metrics.errorRate.toFixed(1)}%</div>
                  <div className="text-sm text-gray-600 dark:text-slate-400">Error Rate</div>
                </div>
              </Panel>
              
              <Panel padded>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {metrics.lastUsed ? new Date(metrics.lastUsed).toLocaleDateString() : 'Never'}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-slate-400">Last Used</div>
                </div>
              </Panel>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Panel title="Permissions">
                <div className="space-y-2">
                  {plugin.capabilities?.permissions?.length ? (
                    plugin.capabilities.permissions.map((permission, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                        <span className="text-sm text-gray-900 dark:text-slate-100">{permission}</span>
                        <Shield size={14} className="text-green-500" />
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500 dark:text-slate-400">No specific permissions required</p>
                  )}
                </div>
              </Panel>
              
              <Panel title="Dependencies">
                <div className="space-y-2">
                  {plugin.capabilities?.dependencies?.length ? (
                    plugin.capabilities.dependencies.map((dep, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                        <span className="text-sm text-gray-900 dark:text-slate-100">{dep}</span>
                        <CheckCircle size={14} className="text-green-500" />
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500 dark:text-slate-400">No external dependencies</p>
                  )}
                </div>
              </Panel>
            </div>
          )}

          {/* Logs Tab */}
          {activeTab === 'logs' && (
            <Panel title="Plugin Logs">
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {pluginLogs.map((log, index) => (
                  <div key={index} className="flex items-start gap-3 text-sm p-2 rounded bg-gray-50 dark:bg-gray-800">
                    <span className="text-gray-500 dark:text-slate-400 font-mono text-xs">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      log.level === 'error' ? 'bg-red-100 text-red-800' :
                      log.level === 'warn' ? 'bg-yellow-100 text-yellow-800' :
                      log.level === 'info' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {log.level}
                    </span>
                    <span className="flex-1 text-gray-900 dark:text-slate-100">{log.message}</span>
                  </div>
                ))}
                
                {pluginLogs.length === 0 && (
                  <div className="text-center py-8 text-gray-500 dark:text-slate-400">
                    <FileText size={32} className="mx-auto mb-2" />
                    <p>No logs available</p>
                  </div>
                )}
              </div>
            </Panel>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
