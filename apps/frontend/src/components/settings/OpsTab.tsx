import { useEffect, useState } from 'react';
import Panel from '@/components/layout/Panel';
import Button from '@/components/ui/Button';
import { toast } from '@/components/ui/toast';
import {
  listStacks,
  stackStatus,
  stackUp,
  stackDown,
  stackRestart,
  stackScale,
  streamLogs,
} from '@/lib/ops';

interface StackInfo {
  title: string;
  files: string[];
}

export default function OpsTab() {
  const [stacks, setStacks] = useState<Record<string, StackInfo>>({});
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<any | null>(null);
  const [logText, setLogText] = useState('');
  const [logStack, setLogStack] = useState<string | null>(null);
  const [scaleService, setScaleService] = useState('');
  const [scaleReplicas, setScaleReplicas] = useState(1);
  const [logController, setLogController] = useState<AbortController | null>(null);

  useEffect(() => {
    listStacks().then((d) => setStacks(d.stacks || {}));
  }, []);

  const handle = async (action: string, name: string) => {
    setLoading(true);
    try {
      if (action === 'status') setStatus(await stackStatus(name));
      if (action === 'up') await stackUp(name);
      if (action === 'down') await stackDown(name);
      if (action === 'restart') await stackRestart(name);
    } catch (e) {
      toast('Action failed', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleScale = async (name: string) => {
    if (!scaleService) {
      toast('Select service', { variant: 'error' });
      return;
    }
    if (scaleReplicas < 0 || scaleReplicas > 10) {
      toast('Replicas 0..10', { variant: 'error' });
      return;
    }
    setLoading(true);
    try {
      await stackScale(name, scaleService, scaleReplicas);
    } catch (e) {
      toast('Scale failed', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleLogs = async (name: string) => {
    logController?.abort();
    const controller = new AbortController();
    setLogController(controller);
    setLogText('');
    setLogStack(name);
    try {
      const res = await streamLogs(name, { signal: controller.signal });
      const reader = res.body?.getReader();
      if (!reader) return;
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        setLogText((t) => t + decoder.decode(value));
      }
    } catch (e) {
      toast('Log stream failed', { variant: 'error' });
    }
  };

  const stopLogs = () => {
    logController?.abort();
    setLogController(null);
    setLogStack(null);
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600 dark:text-slate-400">Aktionen werden protokolliert (Audit)</p>
      {Object.entries(stacks).map(([name, info]) => (
        <Panel key={name} className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-medium">{info.title} ({name})</h3>
            <div className="space-x-2">
              <Button size="sm" onClick={() => handle('status', name)} disabled={loading}>Status</Button>
              <Button size="sm" onClick={() => handle('up', name)} disabled={loading}>Start</Button>
              <Button size="sm" onClick={() => handle('down', name)} disabled={loading}>Stop</Button>
              <Button size="sm" onClick={() => handle('restart', name)} disabled={loading}>Restart</Button>
              <Button size="sm" onClick={() => handleLogs(name)} disabled={loading}>Logs</Button>
            </div>
          </div>
          {status?.stack === name && (
            <>
              <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-2 rounded overflow-auto max-h-40">
                {JSON.stringify(status.services, null, 2)}
              </pre>
              <div className="flex items-center space-x-2">
                <select
                  className="border rounded p-1 text-sm"
                  value={scaleService}
                  onChange={(e) => setScaleService(e.target.value)}
                >
                  <option value="">service</option>
                  {status.services?.map((s: any) => (
                    <option key={s.Service} value={s.Service}>
                      {s.Service}
                    </option>
                  ))}
                </select>
                <input
                  type="number"
                  min={0}
                  max={10}
                  className="border rounded p-1 w-16 text-sm"
                  value={scaleReplicas}
                  onChange={(e) => setScaleReplicas(Number(e.target.value))}
                />
                <Button size="sm" onClick={() => handleScale(name)} disabled={loading}>
                  Scale
                </Button>
              </div>
            </>
          )}
          {logStack === name && (
            <>
              <div className="flex justify-end">
                <Button size="sm" onClick={stopLogs}>
                  Stop
                </Button>
              </div>
              <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-2 rounded overflow-auto max-h-40 whitespace-pre-wrap">
                {logText}
              </pre>
            </>
          )}
        </Panel>
      ))}
    </div>
  );
}
