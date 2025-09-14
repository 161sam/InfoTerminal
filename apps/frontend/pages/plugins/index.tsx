import { useEffect, useState, useMemo } from 'react';
import { invokeTool } from '../../lib/plugins';
import Link from 'next/link';
import {
  Puzzle,
  Search,
  Filter,
  Plus,
  Settings,
  Play,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Clock,
  Download,
  Upload,
  RefreshCw,
  Eye,
  Zap,
  Shield,
  Globe,
  Code,
  BarChart3,
  Users,
  Server
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
    tools?: any[];
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
}

interface PluginStats {
  total: number;
  enabled: number;
  healthy: number;
  categories: Record<string, number>;
}

interface PluginFilter {
  search: string;
  category: string;
  status: string;
  scope: 'user' | 'global';
}

const PLUGIN_CATEGORIES = [
  { value: 'all', label: 'All Categories', icon: Puzzle },
  { value: 'integration', label: 'Integrations', icon: Globe },
  { value: 'analytics', label: 'Analytics', icon: BarChart3 },
  { value: 'security', label: 'Security', icon: Shield },
  { value: 'automation', label: 'Automation', icon: Zap },
  { value: 'development', label: 'Development', icon: Code },
  { value: 'collaboration', label: 'Collaboration', icon: Users }
];

const STATUS_FILTERS = [
  { value: 'all', label: 'All Status' },
  { value: 'enabled', label: 'Enabled' },
  { value: 'disabled', label: 'Disabled' },
  { value: 'healthy', label: 'Healthy' },
  { value: 'unhealthy', label: 'Unhealthy' }
];

function getHealthIcon(health: string) {
  switch (health) {
    case 'up': return <CheckCircle size={16} className="text-green-500" />;
    case 'down': return <XCircle size={16} className="text-red-500" />;
    case 'degraded': return <AlertTriangle size={16} className="text-yellow-500" />;
    default: return <Clock size={16} className="text-gray-400" />;
  }
}

function getHealthBadgeClass(health: string) {
  switch (health) {
    case 'up': return 'bg-green-100 text-green-800 border-green-200';
    case 'down': return 'bg-red-100 text-red-800 border-red-200';
    case 'degraded': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    default: return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}

function PluginCard({
  plugin,
  isAdmin,
  health,
  onToggle,
  onConfig,
  onQuickTest,
  onRefreshHealth
}: {
  plugin: PluginItem;
  isAdmin: boolean;
  health?: string;
  onToggle: (enabled: boolean, scope: 'user' | 'global') => void;
  onConfig: (scope: 'user' | 'global') => void;
  onQuickTest: () => void;
  onRefreshHealth: () => void;
}) {
  const [scope, setScope] = useState<'user' | 'global'>('user');
  const [isUpdating, setIsUpdating] = useState(false);
  const enabled = plugin.enabled !== false;

  const handleToggle = async (newEnabled: boolean) => {
    setIsUpdating(true);
    try {
      await onToggle(newEnabled, scope);
    } finally {
      setIsUpdating(false);
    }
  };

  const getCategoryIcon = (category?: string) => {
    const found = PLUGIN_CATEGORIES.find(c => c.value === category);
    return found ? found.icon : Puzzle;
  };

  const CategoryIcon = getCategoryIcon(plugin.category);

  return (
    <Panel className="hover:shadow-md transition-shadow">
      <div className="space-y-4">

        {/* Plugin Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
              {plugin.icon ? (
                <img src={plugin.icon} alt={plugin.name} className="w-6 h-6" />
              ) : (
                <CategoryIcon size={24} className="text-gray-600 dark:text-slate-400" />
              )}
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-slate-100">{plugin.name}</h3>
              <p className="text-sm text-gray-500 dark:text-slate-400">
                by {plugin.provider} • v{plugin.version}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onRefreshHealth}
              className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
            >
              <RefreshCw size={14} />
            </button>
            <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getHealthBadgeClass(health || 'unknown')}`}>
              {getHealthIcon(health || 'unknown')}
              {health || 'unknown'}
            </div>
          </div>
        </div>

        {/* Plugin Description */}
        {plugin.description && (
          <p className="text-sm text-gray-600 dark:text-slate-400 line-clamp-2">
            {plugin.description}
          </p>
        )}

        {/* Plugin Stats */}
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div className="text-center">
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {plugin.capabilities?.tools?.length || 0}
            </div>
            <div className="text-gray-500 dark:text-slate-400">Tools</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {plugin.downloadCount || 0}
            </div>
            <div className="text-gray-500 dark:text-slate-400">Downloads</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {plugin.rating ? `${plugin.rating}/5` : 'N/A'}
            </div>
            <div className="text-gray-500 dark:text-slate-400">Rating</div>
          </div>
        </div>

        {/* Plugin Categories & Tags */}
        {plugin.category && (
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full dark:bg-blue-900/30 dark:text-blue-300">
              {plugin.category}
            </span>
            {plugin.capabilities?.permissions?.slice(0, 2).map((perm, index) => (
              <span key={index} className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full dark:bg-gray-800 dark:text-slate-400">
                {perm}
              </span>
            ))}
          </div>
        )}

        {/* Controls */}
        <div className="space-y-3 pt-2 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="relative">
                <input
                  type="checkbox"
                  checked={enabled}
                  onChange={(e) => handleToggle(e.target.checked)}
                  disabled={isUpdating}
                  className="sr-only"
                />
                <div
                  onClick={() => !isUpdating && handleToggle(!enabled)}
                  className={`w-11 h-6 rounded-full cursor-pointer transition-colors ${
                    enabled ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
                  } ${isUpdating ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  <div className={`w-4 h-4 bg-white rounded-full transition-transform duration-200 ease-in-out transform ${
                    enabled ? 'translate-x-6' : 'translate-x-1'
                  } mt-1`} />
                </div>
              </div>
              <span className="text-sm text-gray-600 dark:text-slate-400">
                {enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>

            {isAdmin && (
              <select
                value={scope}
                onChange={(e) => setScope(e.target.value as 'user' | 'global')}
                className="px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              >
                <option value="user">User</option>
                <option value="global">Global</option>
              </select>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onQuickTest}
              className="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <Play size={12} />
              Test
            </button>

            <button
              onClick={() => onConfig(scope)}
              className="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <Settings size={12} />
              Config
            </button>

            <Link
              href={`/plugins/${plugin.name}`}
              className="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-primary-700 bg-primary-100 rounded-lg hover:bg-primary-200 dark:bg-primary-900/30 dark:text-primary-300 dark:hover:bg-primary-900/50"
            >
              <Eye size={12} />
              Details
            </Link>
          </div>
        </div>
      </div>
    </Panel>
  );
}

export default function PluginsPage() {
  const { hasRole } = useAuth();
  const isAdmin = hasRole('admin');
  const [items, setItems] = useState<PluginItem[]>([]);
  const [health, setHealth] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const [filters, setFilters] = useState<PluginFilter>({
    search: '',
    category: 'all',
    status: 'all',
    scope: 'user'
  });

  const pluginStats: PluginStats = useMemo(() => {
    const stats = {
      total: items.length,
      enabled: items.filter(p => p.enabled !== false).length,
      healthy: Object.values(health).filter(h => h === 'up').length,
      categories: {} as Record<string, number>
    };

    items.forEach(plugin => {
      const category = plugin.category || 'other';
      stats.categories[category] = (stats.categories[category] || 0) + 1;
    });

    return stats;
  }, [items, health]);

  const filteredPlugins = useMemo(() => {
    return items.filter(plugin => {
      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        if (
          !plugin.name.toLowerCase().includes(searchLower) &&
          !plugin.description?.toLowerCase().includes(searchLower) &&
          !plugin.provider?.toLowerCase().includes(searchLower)
        ) {
          return false;
        }
      }

      // Category filter
      if (filters.category !== 'all' && plugin.category !== filters.category) {
        return false;
      }

      // Status filter
      if (filters.status !== 'all') {
        switch (filters.status) {
          case 'enabled':
            if (plugin.enabled === false) return false;
            break;
          case 'disabled':
            if (plugin.enabled !== false) return false;
            break;
          case 'healthy':
            if (health[plugin.name] !== 'up') return false;
            break;
          case 'unhealthy':
            if (health[plugin.name] === 'up') return false;
            break;
        }
      }

      return true;
    });
  }, [items, health, filters]);

  useEffect(() => {
    loadPlugins();
  }, []);

  const loadPlugins = async () => {
    setLoading(true);
    try {
      const [reg, state] = await Promise.all([
        fetch('/api/plugins/registry').then((r) => r.json()),
        fetch('/api/plugins/state').then((r) => r.json()),
      ]);

      const merged: PluginItem[] = (reg.items || []).map((p: any) => ({
        ...p,
        description: p.description || `${p.name} plugin by ${p.provider}`,
        category: p.category || 'integration',
        downloadCount: Math.floor(Math.random() * 10000), // Mock data
        rating: Math.round((Math.random() * 2 + 3) * 10) / 10, // Mock rating 3-5
        ...(state.items || []).find((s: any) => s.name === p.name),
      }));

      setItems(merged);

      // Load health for all plugins
      await refreshAllHealth(merged);
    } catch (error) {
      console.error('Failed to load plugins:', error);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  const refreshAllHealth = async (pluginList = items) => {
    setRefreshing(true);
    const healthPromises = pluginList.map(async (plugin) => {
      try {
        const response = await fetch(`/api/plugins/${plugin.name}/health`);
        const data = await response.json();
        return { name: plugin.name, status: data.status || 'unknown' };
      } catch {
        return { name: plugin.name, status: 'unknown' };
      }
    });

    try {
      const healthResults = await Promise.all(healthPromises);
      const healthMap = Object.fromEntries(
        healthResults.map(h => [h.name, h.status])
      );
      setHealth(healthMap);
    } finally {
      setRefreshing(false);
    }
  };

  const refreshPluginHealth = async (pluginName: string) => {
    try {
      const response = await fetch(`/api/plugins/${pluginName}/health`);
      const data = await response.json();
      setHealth(prev => ({ ...prev, [pluginName]: data.status || 'unknown' }));
    } catch {
      setHealth(prev => ({ ...prev, [pluginName]: 'unknown' }));
    }
  };

  const togglePlugin = async (name: string, enabled: boolean, scope: 'user' | 'global') => {
    try {
      await fetch(`/api/plugins/${name}/enable`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled, scope }),
      });

      setItems(prev => prev.map(p => p.name === name ? { ...p, enabled } : p));
    } catch (error) {
      console.error('Failed to toggle plugin:', error);
    }
  };

  const openConfig = async (plugin: PluginItem, scope: 'user' | 'global') => {
    const current = plugin.config || {};
    const text = prompt('Plugin Configuration (JSON):', JSON.stringify(current, null, 2));

    if (!text) return;

    try {
      const config = JSON.parse(text);
      await fetch(`/api/plugins/${plugin.name}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config, scope }),
      });

      // Update local state
      setItems(prev => prev.map(p =>
        p.name === plugin.name ? { ...p, config } : p
      ));
    } catch {
      alert('Invalid JSON configuration');
    }
  };

  const quickTest = async (plugin: PluginItem) => {
    const tool = prompt('Tool name:');
    if (!tool) return;

    let payload: any = {};
    const payloadText = prompt('JSON payload:', '{}');

    if (payloadText) {
      try {
        payload = JSON.parse(payloadText);
      } catch {
        alert('Invalid JSON payload');
        return;
      }
    }

    try {
      const result = await invokeTool(plugin.name, tool, payload);
      alert(`Result:\n${JSON.stringify(result, null, 2)}`);
    } catch (error) {
      alert(`Test failed: ${error}`);
    }
  };

  const exportConfig = () => {
    const config = {
      plugins: items.map(p => ({
        name: p.name,
        version: p.version,
        enabled: p.enabled,
        config: p.config
      })),
      exportedAt: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `plugins-config-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <DashboardLayout title="Plugins" subtitle="Manage external integrations">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <RefreshCw size={32} className="animate-spin mx-auto mb-4 text-primary-600" />
            <p className="text-gray-600 dark:text-slate-400">Loading plugins...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Plugin Marketplace" subtitle="Extend your platform with powerful integrations">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">Total Plugins</p>
                <p className="text-2xl font-bold text-blue-800 dark:text-blue-300">{pluginStats.total}</p>
              </div>
              <Puzzle size={24} className="text-blue-500" />
            </div>
          </div>

          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 dark:text-green-400 font-medium">Enabled</p>
                <p className="text-2xl font-bold text-green-800 dark:text-green-300">{pluginStats.enabled}</p>
              </div>
              <CheckCircle size={24} className="text-green-500" />
            </div>
          </div>

          <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 dark:text-purple-400 font-medium">Healthy</p>
                <p className="text-2xl font-bold text-purple-800 dark:text-purple-300">{pluginStats.healthy}</p>
              </div>
              <Server size={24} className="text-purple-500" />
            </div>
          </div>

          <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600 dark:text-orange-400 font-medium">Categories</p>
                <p className="text-2xl font-bold text-orange-800 dark:text-orange-300">
                  {Object.keys(pluginStats.categories).length}
                </p>
              </div>
              <Filter size={24} className="text-orange-500" />
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 flex-1">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
              <input
                type="text"
                placeholder="Search plugins..."
                value={filters.search}
                onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            </div>

            <select
              value={filters.category}
              onChange={(e) => setFilters(prev => ({ ...prev, category: e.target.value }))}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              {PLUGIN_CATEGORIES.map(category => (
                <option key={category.value} value={category.value}>{category.label}</option>
              ))}
            </select>

            <select
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              {STATUS_FILTERS.map(status => (
                <option key={status.value} value={status.value}>{status.label}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => refreshAllHealth()}
              disabled={refreshing}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''} />
              Refresh
            </button>

            <button
              onClick={exportConfig}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <Download size={14} />
              Export
            </button>

            <button className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700">
              <Plus size={14} />
              Add Plugin
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-600 dark:text-slate-400">
                  Showing {filteredPlugins.length} of {items.length} plugins
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {filteredPlugins.map((plugin) => (
                  <PluginCard
                    key={plugin.name}
                    plugin={plugin}
                    isAdmin={isAdmin}
                    health={health[plugin.name]}
                    onToggle={(enabled, scope) => togglePlugin(plugin.name, enabled, scope)}
                    onConfig={(scope) => openConfig(plugin, scope)}
                    onQuickTest={() => quickTest(plugin)}
                    onRefreshHealth={() => refreshPluginHealth(plugin.name)}
                  />
                ))}

                {filteredPlugins.length === 0 && (
                  <div className="col-span-2 text-center py-12">
                    <Puzzle size={48} className="mx-auto text-gray-400 dark:text-slate-500 mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">
                      No plugins found
                    </h3>
                    <p className="text-gray-500 dark:text-slate-400">
                      {filters.search || filters.category !== 'all' || filters.status !== 'all'
                        ? 'Try adjusting your filters'
                        : 'No plugins are currently installed'
                      }
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">

            {/* Categories */}
            <Panel title="Categories">
              <div className="space-y-2">
                {PLUGIN_CATEGORIES.filter(c => c.value !== 'all').map((category) => {
                  const count = pluginStats.categories[category.value] || 0;
                  const Icon = category.icon;

                  return (
                    <button
                      key={category.value}
                      onClick={() => setFilters(prev => ({
                        ...prev,
                        category: category.value === filters.category ? 'all' : category.value
                      }))}
                      className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                        filters.category === category.value
                          ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                          : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <Icon size={16} />
                        <span className="text-sm font-medium">{category.label}</span>
                      </div>
                      <span className="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded-full">
                        {count}
                      </span>
                    </button>
                  );
                })}
              </div>
            </Panel>

            {/* Quick Actions */}
            <Panel title="Quick Actions">
              <div className="space-y-2">
                <button className="w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center gap-3">
                    <Upload size={16} className="text-blue-500" />
                    <div>
                      <div className="font-medium text-sm">Install Plugin</div>
                      <div className="text-xs text-gray-500 dark:text-slate-400">Upload .zip file</div>
                    </div>
                  </div>
                </button>

                <button className="w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center gap-3">
                    <Zap size={16} className="text-green-500" />
                    <div>
                      <div className="font-medium text-sm">Bulk Enable</div>
                      <div className="text-xs text-gray-500 dark:text-slate-400">Enable all healthy plugins</div>
                    </div>
                  </div>
                </button>

                <button className="w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center gap-3">
                    <BarChart3 size={16} className="text-purple-500" />
                    <div>
                      <div className="font-medium text-sm">Usage Report</div>
                      <div className="text-xs text-gray-500 dark:text-slate-400">Generate plugin analytics</div>
                    </div>
                  </div>
                </button>
              </div>
            </Panel>

            {/* Health Summary */}
            <Panel title="Health Overview">
              <div className="space-y-3">
                {Object.entries(['up', 'down', 'degraded', 'unknown']).map(([_, status]) => {
                  const count = Object.values(health).filter(h => h === status).length;
                  if (count === 0) return null;

                  return (
                    <div key={status} className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        {getHealthIcon(status)}
                        <span className="capitalize text-gray-700 dark:text-slate-300">{status}</span>
                      </div>
                      <span className="font-medium text-gray-900 dark:text-slate-100">{count}</span>
                    </div>
                  );
                })}
              </div>
            </Panel>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
