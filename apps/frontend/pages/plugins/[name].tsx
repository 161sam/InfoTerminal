import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { Switch } from '@headlessui/react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuth } from '@/components/auth/AuthProvider';

interface PluginItem {
  name: string;
  version?: string;
  provider?: string;
  endpoints?: { baseUrl?: string };
  enabled?: boolean;
}

export default function PluginDetailPage() {
  const router = useRouter();
  const { hasRole } = useAuth();
  const isAdmin = hasRole('admin');
  const { name } = router.query as { name?: string };
  const [plugin, setPlugin] = useState<PluginItem | null>(null);
  const [health, setHealth] = useState('unknown');
  const [scope, setScope] = useState<'user' | 'global'>('user');
  const [ready, setReady] = useState(false);
  const [showFallback, setShowFallback] = useState(false);

  useEffect(() => {
    if (!name) return;
    let cancelled = false;
    async function load() {
      const [reg, state] = await Promise.all([
        fetch('/api/plugins/registry').then((r) => r.json()),
        fetch('/api/plugins/state').then((r) => r.json()),
      ]);
      const base = (reg.items || []).find((p: any) => p.name === name);
      const st = (state.items || []).find((p: any) => p.name === name);
      if (!cancelled) setPlugin({ ...base, ...st });
      fetch(`/api/plugins/${name}/health`)
        .then((r) => r.json())
        .then((d) => !cancelled && setHealth(d.status || 'unknown'))
        .catch(() => !cancelled && setHealth('unknown'));
    }
    load();
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

  const toggle = async (enabled: boolean) => {
    if (!name) return;
    await fetch(`/api/plugins/${name}/enable`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled, scope }),
    });
    setPlugin((p) => (p ? { ...p, enabled } : p));
  };

  const src = plugin?.endpoints?.baseUrl;

  return (
    <DashboardLayout title={plugin?.name || 'Plugin'} subtitle={plugin?.provider}>
      <div className="p-6 space-y-4">
        <div className="flex items-center gap-2">
          <span
            className={`text-xs px-2 py-1 rounded ${
              health === 'up'
                ? 'bg-green-100 text-green-800'
                : health === 'down'
                ? 'bg-red-100 text-red-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {health}
          </span>
          <Switch
            checked={plugin?.enabled !== false}
            onChange={toggle}
            className={`${
              plugin?.enabled !== false ? 'bg-primary-600' : 'bg-gray-200'
            } relative inline-flex h-6 w-11 items-center rounded-full`}
          >
            <span className="sr-only">Enable</span>
            <span
              className={`${
                plugin?.enabled !== false ? 'translate-x-6' : 'translate-x-1'
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
        {src && ready && !showFallback ? (
          <iframe
            src={src}
            className="w-full h-96 border rounded"
            sandbox="allow-same-origin allow-scripts allow-forms"
          />
        ) : (
          <div className="border rounded p-6 text-center space-y-2">
            <p className="text-sm">Plugin UI unavailable</p>
            {src && (
              <a
                href={src}
                target="_blank"
                rel="noopener"
                className="text-primary-600 underline"
              >
                Open externally
              </a>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

