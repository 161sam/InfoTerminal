import { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

export default function GraphMLPage() {
  const [pr, setPr] = useState<any[]>([]);
  const [emb, setEmb] = useState<any>({ items: [] });
  const [loading, setLoading] = useState(false);

  const runPR = async () => {
    setLoading(true);
    try {
      const r = await fetch('/api/graph/analytics/pagerank?limit=20');
      const data = await r.json();
      setPr(data.nodes || []);
    } finally { setLoading(false); }
  };
  const runN2V = async () => {
    setLoading(true);
    try {
      const r = await fetch('/api/graph/analytics/embeddings/node2vec?dimensions=8');
      const data = await r.json();
      setEmb(data || { items: [] });
    } finally { setLoading(false); }
  };

  return (
    <DashboardLayout title="Graph ML" subtitle="PageRank and Node2Vec">
      <div className="max-w-6xl mx-auto p-4 space-y-6">
        <Panel title="PageRank">
          <div className="flex items-center gap-2 mb-2">
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={runPR} disabled={loading}>Run PageRank</button>
          </div>
          <div className="space-y-1">
            {(pr || []).map((n: any, i: number) => (
              <div key={i} className="text-sm flex justify-between">
                <span>{n.name || n.node_id}</span>
                <span className="text-gray-500">{(n.score ?? n.centrality_score ?? 0).toFixed(4)}</span>
              </div>
            ))}
            {!pr.length && <div className="text-sm text-gray-500">No results yet</div>}
          </div>
        </Panel>
        <Panel title="Node2Vec (8D preview)">
          <div className="flex items-center gap-2 mb-2">
            <button className="px-4 py-2 bg-gray-800 text-white rounded" onClick={runN2V} disabled={loading}>Run Node2Vec</button>
          </div>
          <div className="grid grid-cols-2 gap-2">
            {(emb.items || []).slice(0, 20).map((e: any, i: number) => (
              <div key={i} className="text-xs p-2 border rounded">
                <div className="font-medium">{e.name || `node_${i}`}</div>
                <div className="text-gray-500">[{(e.embedding || []).slice(0, 8).map((x: number) => x.toFixed(2)).join(', ')}]</div>
              </div>
            ))}
            {!emb.items?.length && <div className="text-sm text-gray-500">No embeddings yet</div>}
          </div>
        </Panel>
      </div>
    </DashboardLayout>
  );
}

