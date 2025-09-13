import { useState } from 'react';
import config from '@/lib/config';

export default function AnalysisPanel() {
  const [result, setResult] = useState<any>(null);

  const run = async (alg: string) => {
    try {
      const r = await fetch(`${config.GRAPH_API}/alg/${alg}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
      });
      const data = await r.json();
      setResult(data);
    } catch (e) {
      setResult({ error: String(e) });
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex gap-2">
        <button onClick={() => run('degree')} className="px-2 py-1 border rounded">Degree</button>
        <button onClick={() => run('betweenness')} className="px-2 py-1 border rounded">Betweenness</button>
        <button onClick={() => run('communities')} className="px-2 py-1 border rounded">Communities</button>
      </div>
      {result && (
        <pre className="bg-gray-100 p-2 text-xs overflow-auto">{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}
