import { useState } from 'react';
import config from '@/lib/config';

interface Props {
  onResult?: (alg: string, items: any[]) => void;
}

export default function AnalysisPanel({ onResult }: Props) {
  const [status, setStatus] = useState<'idle' | 'loading' | 'done' | 'error'>('idle');
  const [lastAlg, setLastAlg] = useState<string | null>(null);

  const run = async (alg: string) => {
    setStatus('loading');
    setLastAlg(alg);
    try {
      const r = await fetch(`${config.GRAPH_API}/alg/${alg}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
      });
      const data = await r.json();
      onResult?.(alg, data.items || []);
      setStatus('done');
    } catch (e) {
      setStatus('error');
    }
  };

  const badge = () => {
    if (status === 'loading') return <span className="text-xs text-blue-600">{lastAlg}…</span>;
    if (status === 'done') return <span className="text-xs text-green-600">{lastAlg} ✓</span>;
    if (status === 'error') return <span className="text-xs text-red-600">{lastAlg} ✗</span>;
    return null;
  };

  return (
    <div className="space-y-2">
      <div className="flex gap-2">
        <button onClick={() => run('degree')} className="px-2 py-1 border rounded">Degree</button>
        <button onClick={() => run('betweenness')} className="px-2 py-1 border rounded">Betweenness</button>
        <button onClick={() => run('louvain')} className="px-2 py-1 border rounded">Louvain</button>
        {badge()}
      </div>
    </div>
  );
}
