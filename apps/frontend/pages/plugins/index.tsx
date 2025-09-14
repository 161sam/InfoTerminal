import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Switch } from '@headlessui/react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuth } from '@/components/auth/AuthProvider';

interface PluginItem {
  name: string;
  version?: string;
  provider?: string;
  capabilities?: { tools?: any[] };
  enabled?: boolean;
  endpoints?: { baseUrl?: string };
  config?: Record<string, any>;
}

function PluginCard({
  plugin,
  isAdmin,
  health,
  onToggle,
  onConfig,
  onQuickTest,
}: {
  plugin: PluginItem;
  isAdmin: boolean;
  health?: string;
  onToggle: (enabled: boolean, scope: 'user' | 'global') => void;
  onConfig: (scope: 'user' | 'global') => void;
  onQuickTest: () => void;
}) {
  const [scope, setScope] = useState<'user' | 'global'>('user');
  const enabled = plugin.enabled !== false;
  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-900 space-y-2">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="font-semibold">{plugin.name}</h3>
          <p className="text-sm text-gray-500">
            {plugin.provider} {plugin.version}
          </p>
        </div>
        <span
          className={`text-xs px-2 py-1 rounded ${
            health === 'up'
              ? 'bg-green-100 text-green-800'
              : health === 'down'
              ? 'bg-red-100 text-red-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {health || '...'}
        </span>
      </div>
      <p className="text-sm">Tools: {plugin.capabilities?.tools?.length || 0}</p>
      <div className="flex items-center gap-2">
        <Switch
          checked={enabled}
          onChange={(v) => onToggle(v, scope)}
          className={`${
            enabled ? 'bg-primary-600' : 'bg-gray-200'
          } relative inline-flex h-6 w-11 items-center rounded-full`}
        >
          <span className="sr-only">Enable</span>
          <span
            className={`${
              enabled ? 'translate-x-6' : 'translate-x-1'
            } inline-block h-4 w-4 transform rounded-full bg-white`}
          />
        </Switch>
        {isAdmin && (
          <select
            value={scope}
            onChange={(e) => setScope(e.target.value as 'user' | 'global')}
            className="text-sm border rounded p-1"
          >
            <option value="user">user</option>
            <option value="global">global</option>
          </select>
        )}
      </div>
      <div className="flex gap-2 pt-1">
        <button
          onClick={onQuickTest}
          className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded"
        >
          Quick Test
        </button>
        <button
          onClick={() => onConfig(scope)}
          className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded"
        >
          Config
        </button>
        <Link
          href={`/plugins/${plugin.name}`}
          className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded"
        >
          Details
        </Link>
      </div>
    </div>
  );
}

export default function PluginsPage() {
  const { hasRole } = useAuth();
  const isAdmin = hasRole('admin');
  const [items, setItems] = useState<PluginItem[]>([]);
  const [health, setHealth] = useState<Record<string, string>>({});

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [reg, state] = await Promise.all([
          fetch('/api/plugins/registry').then((r) => r.json()),
          fetch('/api/plugins/state').then((r) => r.json()),
        ]);
        const merged: PluginItem[] = (reg.items || []).map((p: any) => ({
          ...p,
          ...(state.items || []).find((s: any) => s.name === p.name),
        }));
        if (!cancelled) {
          setItems(merged);
          merged.forEach((p) => {
            const controller = new AbortController();
            fetch(`/api/plugins/${p.name}/health`, { signal: controller.signal })
              .then((r) => r.json())
              .then((d) => !cancelled && setHealth((h) => ({ ...h, [p.name]: d.status || 'unknown' })))
              .catch(() => !cancelled && setHealth((h) => ({ ...h, [p.name]: 'unknown' })));
          });
        }
      } catch {
        if (!cancelled) setItems([]);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const toggle = async (name: string, enabled: boolean, scope: 'user' | 'global') => {
    await fetch(`/api/plugins/${name}/enable`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled, scope }),
    });
    setItems((arr) => arr.map((p) => (p.name === name ? { ...p, enabled } : p)));
  };

  const openConfig = async (p: PluginItem, scope: 'user' | 'global') => {
    const current = p.config || {};
    const text = prompt('Config JSON', JSON.stringify(current, null, 2));
    if (!text) return;
    try {
      const cfg = JSON.parse(text);
      await fetch(`/api/plugins/${p.name}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config: cfg, scope }),
      });
    } catch {
      alert('Invalid JSON');
    }
  };

  const quickTest = async (p: PluginItem) => {
    const tool = prompt('Tool name');
    if (!tool) return;
    let payload: any = {};
    const text = prompt('JSON payload', '{}');
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch {
        alert('Invalid JSON');
        return;
      }
    }
    const res = await fetch(`/api/plugins/invoke/${p.name}/${tool}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    alert(JSON.stringify(data));
  };

  return (
    <DashboardLayout title="Plugins" subtitle="Manage external integrations">
      <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((p) => (
          <PluginCard
            key={p.name}
            plugin={p}
            isAdmin={isAdmin}
            health={health[p.name]}
            onToggle={(v, scope) => toggle(p.name, v, scope)}
            onConfig={(scope) => openConfig(p, scope)}
            onQuickTest={() => quickTest(p)}
          />
        ))}
      </div>
    </DashboardLayout>
  );
}

