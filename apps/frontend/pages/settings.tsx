import { useState, useEffect } from "react";
import { 
  Settings, 
  Server, 
  Database, 
  Network, 
  Eye, 
  Brain, 
  Search, 
  Save, 
  RefreshCw, 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  Monitor, 
  Globe,
  Shield,
  Palette,
  Bell,
  User,
  Download
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/Button";
import Field from "@/components/ui/Field";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import { toast } from "@/components/ui/toast";
import {
  loadEndpoints,
  saveEndpoints,
  sanitizeUrl,
  validateUrl,
  EndpointSettings,
} from "@/lib/endpoints";
import SettingsGateway from "@/components/settings/SettingsGateway";
import SettingsGraphDeepLink from "@/components/settings/SettingsGraphDeepLink";
import OpsTab from "@/components/settings/OpsTab";
import { useAuth } from "@/components/auth/AuthProvider";

type SettingsTab = 'endpoints' | 'ops' | 'gateway' | 'appearance' | 'notifications' | 'security' | 'about';

interface ServiceEndpoint {
  key: keyof EndpointSettings;
  label: string;
  description: string;
  icon: LucideIcon;
  required: boolean;
  defaultPort?: string;
}

const SERVICE_ENDPOINTS: ServiceEndpoint[] = [
  {
    key: "SEARCH_API",
    label: "Search API",
    description: "Full-text search and document indexing service",
    icon: Search,
    required: true,
    defaultPort: "8001"
  },
  {
    key: "GRAPH_API",
    label: "Graph Database API",
    description: "Neo4j graph database for relationship analysis",
    icon: Database,
    required: true,
    defaultPort: "7474"
  },
  {
    key: "DOCENTITIES_API",
    label: "Document Entities API",
    description: "NLP service for entity extraction and document processing",
    icon: Brain,
    required: true,
    defaultPort: "8003"
  },
  {
    key: "VIEWS_API",
    label: "Views API",
    description: "Data visualization and analytics service",
    icon: Eye,
    required: false,
    defaultPort: "8004"
  },
  {
    key: "NLP_API",
    label: "NLP Processing API",
    description: "Advanced natural language processing capabilities",
    icon: Brain,
    required: false,
    defaultPort: "8005"
  }
];

const THEMES = [
  { id: 'light', name: 'Light Mode', description: 'Clean light interface' },
  { id: 'dark', name: 'Dark Mode', description: 'Easy on the eyes' },
  { id: 'system', name: 'System Default', description: 'Follow system preference' }
];

async function testEndpoint(url: string): Promise<{ status: Status; latency?: number; info?: any }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  const start = performance.now();
  
  try {
    const response = await fetch(url + "/healthz", { signal: controller.signal });
    const latency = Math.round(performance.now() - start);
    clearTimeout(timeout);
    
    if (!response.ok) {
      return { status: "fail", latency };
    }
    
    const info = await response.json().catch(() => ({}));
    let status: Status = "ok";
    
    if (info.status === 'degraded') status = 'degraded';
    else if (info.status === 'fail') status = 'fail';
    else if (info.status !== 'ok' && info.status) status = 'fail';
    
    return { status, latency, info };
  } catch (error) {
    clearTimeout(timeout);
    return { status: "fail" };
  }
}

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<SettingsTab>('endpoints');
  const [endpointValues, setEndpointValues] = useState<EndpointSettings>(loadEndpoints());
  const [endpointStatus, setEndpointStatus] = useState<Record<string, { status: Status; latency?: number; info?: any }>>({});
  const [isSaving, setIsSaving] = useState(false);
  const [testingEndpoint, setTestingEndpoint] = useState<string | null>(null);
  
  // Theme settings
  const [currentTheme, setCurrentTheme] = useState('system');
  
  // Notification settings
  const [notifications, setNotifications] = useState({
    desktop: true,
    email: false,
    searchResults: true,
    systemAlerts: true,
    graphUpdates: false
  });

  const { user } = useAuth();
  const roles = user?.roles || [];
  const FEATURE_OPS = process.env.NEXT_PUBLIC_FEATURE_OPS === "1";
  const hasOpsRole = roles.includes("admin") || roles.includes("ops");

  const handleEndpointTest = async (endpoint: ServiceEndpoint) => {
    const url = sanitizeUrl(endpointValues[endpoint.key] || '');
    if (!url) {
      toast(`No URL configured for ${endpoint.label}`, { variant: 'error' });
      return;
    }

    if (!validateUrl(url)) {
      toast(`Invalid URL for ${endpoint.label}`, { variant: 'error' });
      return;
    }

    setTestingEndpoint(String(endpoint.key));
    setEndpointStatus((prev) => ({
      ...prev,
      [String(endpoint.key)]: { status: "loading" as Status },
    }));

    try {
      const result = await testEndpoint(url);
      setEndpointStatus(prev => ({ ...prev, [endpoint.key]: result }));
      
      if (result.status === 'ok') {
        toast(`${endpoint.label} is healthy${result.latency ? ` (${result.latency}ms)` : ''}`, { variant: 'success' });
      } else {
        toast(`${endpoint.label} connection failed`, { variant: 'error' });
      }
    } catch (error) {
      setEndpointStatus((prev) => ({
        ...prev,
        [String(endpoint.key)]: { status: "fail" as Status },
      }));
      toast(`${endpoint.label} test failed`, { variant: 'error' });
    } finally {
      setTestingEndpoint(null);
    }
  };

  const handleTestAllEndpoints = async () => {
    const configuredEndpoints = SERVICE_ENDPOINTS.filter(ep => endpointValues[ep.key]);
    
    if (configuredEndpoints.length === 0) {
      toast('No endpoints configured to test', { variant: 'error' });
      return;
    }

    setTestingEndpoint('all');
    
    const results = await Promise.allSettled(
      configuredEndpoints.map(async (endpoint) => {
        const url = sanitizeUrl(endpointValues[endpoint.key] || '');
        const result = await testEndpoint(url);
        return { endpoint: endpoint.key, result };
      })
    );

    const newStatus: Record<string, any> = {};
    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        newStatus[result.value.endpoint] = result.value.result;
      } else {
        newStatus[configuredEndpoints[index].key] = { status: 'fail' };
      }
    });

    setEndpointStatus(prev => ({ ...prev, ...newStatus }));
    setTestingEndpoint(null);

    const successCount = Object.values(newStatus).filter(r => r.status === 'ok').length;
    toast(`Tested ${configuredEndpoints.length} endpoints: ${successCount} healthy, ${configuredEndpoints.length - successCount} failed`, {
      variant: successCount === configuredEndpoints.length ? 'success' : 'error'
    });
  };

  const handleSaveEndpoints = async () => {
    setIsSaving(true);
    
    try {
      const sanitized: EndpointSettings = {} as any;
      
      for (const [key, value] of Object.entries(endpointValues)) {
        const sanitizedUrl = sanitizeUrl(value || '');
        if (sanitizedUrl && !validateUrl(sanitizedUrl)) {
          toast(`Invalid URL for ${key}`, { variant: 'error' });
          setIsSaving(false);
          return;
        }
        sanitized[key as keyof EndpointSettings] = sanitizedUrl;
      }
      
      saveEndpoints(sanitized);
      toast("Settings saved successfully", { variant: 'success' });
    } catch (error) {
      toast("Failed to save settings", { variant: 'error' });
    } finally {
      setIsSaving(false);
    }
  };

  const handleThemeChange = (theme: string) => {
    setCurrentTheme(theme);
    // Here you would implement actual theme switching logic
    toast(`Theme changed to ${theme}`, { variant: 'success' });
  };

  const TabButton = ({ id, label, icon: Icon }: { id: SettingsTab; label: string; icon: LucideIcon }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`inline-flex items-center gap-2 px-4 py-3 text-sm rounded-lg transition-colors ${
        activeTab === id
          ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
          : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200 hover:bg-gray-100 dark:hover:bg-gray-800'
      }`}
    >
      <Icon size={16} />
      {label}
    </button>
  );

  const getEndpointSummary = () => {
    const total = SERVICE_ENDPOINTS.length;
    const configured = SERVICE_ENDPOINTS.filter(ep => endpointValues[ep.key]).length;
    const healthy = Object.values(endpointStatus).filter(s => s.status === 'ok').length;
    return { total, configured, healthy };
  };

  return (
    <DashboardLayout title="Settings" subtitle="Configure your intelligence platform">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Settings Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
            <div className="flex items-center gap-3">
              <Server size={20} className="text-blue-600 dark:text-blue-400" />
              <div>
                <div className="text-sm text-blue-600 dark:text-blue-400 font-medium">Services</div>
                <div className="text-lg font-bold text-blue-800 dark:text-blue-300">
                  {getEndpointSummary().configured}/{getEndpointSummary().total}
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/30">
            <div className="flex items-center gap-3">
              <CheckCircle size={20} className="text-green-600 dark:text-green-400" />
              <div>
                <div className="text-sm text-green-600 dark:text-green-400 font-medium">Healthy</div>
                <div className="text-lg font-bold text-green-800 dark:text-green-300">
                  {getEndpointSummary().healthy}
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-900/30">
            <div className="flex items-center gap-3">
              <Palette size={20} className="text-purple-600 dark:text-purple-400" />
              <div>
                <div className="text-sm text-purple-600 dark:text-purple-400 font-medium">Theme</div>
                <div className="text-lg font-bold text-purple-800 dark:text-purple-300 capitalize">
                  {currentTheme}
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-900/30">
            <div className="flex items-center gap-3">
              <Monitor size={20} className="text-orange-600 dark:text-orange-400" />
              <div>
                <div className="text-sm text-orange-600 dark:text-orange-400 font-medium">Runtime</div>
                <div className="text-lg font-bold text-orange-800 dark:text-orange-300">
                  {typeof window === "undefined" ? "Server" : "Client"}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
          <TabButton id="endpoints" label="API Endpoints" icon={Server} />
          {FEATURE_OPS && hasOpsRole && (
            <TabButton id="ops" label="Ops" icon={Monitor} />
          )}
          <TabButton id="gateway" label="Gateway" icon={Network} />
          <TabButton id="appearance" label="Appearance" icon={Palette} />
          <TabButton id="notifications" label="Notifications" icon={Bell} />
          <TabButton id="security" label="Security" icon={Shield} />
          <TabButton id="about" label="About" icon={Info} />
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          
          {/* API Endpoints Tab */}
          {activeTab === 'endpoints' && (
            <>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">Service Endpoints</h3>
                  <p className="text-sm text-gray-600 dark:text-slate-400">Configure connections to your backend services</p>
                </div>
                
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    onClick={handleTestAllEndpoints}
                    disabled={testingEndpoint !== null}
                  >
                    {testingEndpoint === 'all' ? (
                      <RefreshCw size={16} className="animate-spin mr-2" />
                    ) : (
                      <RefreshCw size={16} className="mr-2" />
                    )}
                    Test All
                  </Button>
                  
                  <Button
                    onClick={handleSaveEndpoints}
                    disabled={isSaving}
                  >
                    {isSaving ? (
                      <RefreshCw size={16} className="animate-spin mr-2" />
                    ) : (
                      <Save size={16} className="mr-2" />
                    )}
                    Save
                  </Button>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-6">
                {SERVICE_ENDPOINTS.map((endpoint) => (
                  <Panel key={endpoint.key} className={endpoint.required ? 'border-l-4 border-l-blue-500' : ''}>
                    <div className="flex items-start gap-4">
                      <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                        <endpoint.icon size={24} className="text-gray-600 dark:text-slate-400" />
                      </div>
                      
                      <div className="flex-1 space-y-4">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold text-gray-900 dark:text-slate-100">{endpoint.label}</h4>
                            {endpoint.required && (
                              <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">Required</span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 dark:text-slate-400">{endpoint.description}</p>
                          {endpoint.defaultPort && (
                            <p className="text-xs text-gray-500 dark:text-slate-500 mt-1">
                              Default port: {endpoint.defaultPort}
                            </p>
                          )}
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <Field
                            label=""
                            name={`endpoint-${String(endpoint.key).toLowerCase()}`}
                            id={`endpoint-${String(endpoint.key).toLowerCase()}`}
                            value={endpointValues[endpoint.key] || ''}
                            onChange={(e) => setEndpointValues(prev => ({ 
                              ...prev, 
                              [endpoint.key]: e.target.value 
                            }))}
                            placeholder={`http://localhost:${endpoint.defaultPort || '8000'}`}
                            className="flex-1"
                          />
                          
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleEndpointTest(endpoint)}
                            disabled={testingEndpoint !== null || !endpointValues[endpoint.key]}
                          >
                            {testingEndpoint === String(endpoint.key) ? (
                              <RefreshCw size={14} className="animate-spin" />
                            ) : (
                              'Test'
                            )}
                          </Button>
                          
                          {endpointStatus[endpoint.key] && (
                            <div className="flex items-center gap-2">
                              <StatusPill status={endpointStatus[endpoint.key].status} />
                              {endpointStatus[endpoint.key].latency && (
                                <span className="text-xs text-gray-500">
                                  {endpointStatus[endpoint.key].latency}ms
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                        
                        {endpointStatus[endpoint.key]?.info && Object.keys(endpointStatus[endpoint.key].info).length > 0 && (
                          <details className="text-xs">
                            <summary className="cursor-pointer text-gray-600 dark:text-slate-400">Service Info</summary>
                            <pre className="mt-1 p-2 bg-gray-50 dark:bg-gray-900 rounded overflow-auto">
                              {JSON.stringify(endpointStatus[endpoint.key].info, null, 2)}
                            </pre>
                          </details>
                        )}
                      </div>
                    </div>
                  </Panel>
                ))}
              </div>
            </>
          )}

          {/* Gateway Tab */}
          {FEATURE_OPS && hasOpsRole && activeTab === 'ops' && (
            <OpsTab />
          )}
          {activeTab === 'gateway' && (
            <Panel>
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">API Gateway Configuration</h3>
                  <p className="text-sm text-gray-600 dark:text-slate-400">Configure routing and load balancing for your services</p>
                </div>
                <SettingsGateway />
              </div>
            </Panel>
          )}

          {/* Appearance Tab */}
          {activeTab === 'appearance' && (
            <div className="space-y-6">
              <Panel>
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">Theme Preferences</h3>
                    <p className="text-sm text-gray-600 dark:text-slate-400">Customize the look and feel of your dashboard</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {THEMES.map((theme) => (
                      <button
                        key={theme.id}
                        onClick={() => handleThemeChange(theme.id)}
                        className={`p-4 text-left rounded-lg border-2 transition-colors ${
                          currentTheme === theme.id
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                      >
                        <div className="font-medium text-gray-900 dark:text-slate-100">{theme.name}</div>
                        <div className="text-sm text-gray-600 dark:text-slate-400 mt-1">{theme.description}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </Panel>
              
              <Panel>
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">Graph Visualization</h3>
                  <SettingsGraphDeepLink />
                </div>
              </Panel>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === 'notifications' && (
            <Panel>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">Notification Preferences</h3>
                  <p className="text-sm text-gray-600 dark:text-slate-400">Control when and how you receive notifications</p>
                </div>
                
                <div className="space-y-4">
                  {[
                    { key: 'desktop', label: 'Desktop Notifications', description: 'Show browser notifications for important events' },
                    { key: 'email', label: 'Email Notifications', description: 'Receive email alerts for critical updates' },
                    { key: 'searchResults', label: 'Search Results', description: 'Notify when new search results are available' },
                    { key: 'systemAlerts', label: 'System Alerts', description: 'Alerts for service issues and maintenance' },
                    { key: 'graphUpdates', label: 'Graph Updates', description: 'Notifications for significant graph changes' }
                  ].map((setting) => (
                    <div key={setting.key} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-slate-100">{setting.label}</h4>
                        <p className="text-sm text-gray-600 dark:text-slate-400">{setting.description}</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={notifications[setting.key as keyof typeof notifications]}
                          onChange={(e) => setNotifications(prev => ({
                            ...prev,
                            [setting.key]: e.target.checked
                          }))}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            </Panel>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <Panel>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">Security Settings</h3>
                  <p className="text-sm text-gray-600 dark:text-slate-400">Manage security and access control settings</p>
                </div>
                
                <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-900/30 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <AlertTriangle size={20} className="text-yellow-600 dark:text-yellow-400 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-yellow-800 dark:text-yellow-300">Security Notice</h4>
                      <p className="text-sm text-yellow-700 dark:text-yellow-400 mt-1">
                        Security settings are managed at the system level. Please contact your administrator for access control configuration.
                      </p>
                    </div>
                  </div>
                </div>
                
                <Button variant="outline" className="w-full">
                  <Shield size={16} className="mr-2" />
                  View Security Dashboard
                </Button>
              </div>
            </Panel>
          )}

          {/* About Tab */}
          {activeTab === 'about' && (
            <div className="space-y-6">
              <Panel>
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">System Information</h3>
                    <p className="text-sm text-gray-600 dark:text-slate-400">Technical details about your installation</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-slate-400">Environment:</span>
                        <span className="font-mono text-gray-900 dark:text-slate-100">
                          {process.env.NODE_ENV || 'development'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-slate-400">Runtime:</span>
                        <span className="font-mono text-gray-900 dark:text-slate-100">
                          {typeof window === "undefined" ? "Server" : "Client"}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-slate-400">Build Time:</span>
                        <span className="font-mono text-gray-900 dark:text-slate-100">
                          {new Date().toLocaleString()}
                        </span>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-slate-400">User Agent:</span>
                        <span className="font-mono text-gray-900 dark:text-slate-100 text-xs truncate max-w-32" title={typeof window !== 'undefined' ? navigator.userAgent : 'N/A'}>
                          {typeof window !== 'undefined' ? navigator.userAgent.split(' ')[0] : 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-slate-400">Storage:</span>
                        <span className="font-mono text-gray-900 dark:text-slate-100">
                          localStorage
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Panel>
              
              <Panel>
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">Storage & Data</h3>
                  <div className="text-sm text-gray-600 dark:text-slate-400">
                    <p className="mb-2">Settings are stored locally in your browser using localStorage with the key:</p>
                    <code className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
                      it.settings.endpoints
                    </code>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      <Download size={14} className="mr-2" />
                      Export Settings
                    </Button>
                    <Button variant="outline" size="sm">
                      <Globe size={14} className="mr-2" />
                      Clear Cache
                    </Button>
                  </div>
                </div>
              </Panel>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
