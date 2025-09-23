import { useEffect, useRef, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

export default function GraphMLPage() {
  const [pr, setPr] = useState<any[]>([]);
  const [emb, setEmb] = useState<any>({ items: [] });
  const [loading, setLoading] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [hover, setHover] = useState<{ name: string; x: number; y: number } | null>(null);
  const pointsRef = useRef<{ name: string; x: number; y: number }[]>([]);

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

  // Draw embeddings on canvas (first two dimensions)
  useEffect(() => {
    const items = emb.items || [];
    const cv = canvasRef.current;
    if (!cv) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;
    const W = cv.width = cv.clientWidth || 600;
    const H = cv.height = 400;
    ctx.clearRect(0, 0, W, H);
    if (!items.length) return;
    const points = items
      .map((e: any) => ({ name: e.name || '', x: (e.embedding?.[0] ?? 0), y: (e.embedding?.[1] ?? 0) }));
    let minX = Math.min(...points.map(p => p.x));
    let maxX = Math.max(...points.map(p => p.x));
    let minY = Math.min(...points.map(p => p.y));
    let maxY = Math.max(...points.map(p => p.y));
    const pad = 20;
    const scaleX = (x: number) => pad + (W - 2*pad) * ((x - minX) / (maxX - minX || 1));
    const scaleY = (y: number) => pad + (H - 2*pad) * (1 - (y - minY) / (maxY - minY || 1));
    ctx.fillStyle = '#e11d48';
    const screenPts: { name: string; x: number; y: number }[] = [];
    for (const p of points) {
      const x = scaleX(p.x);
      const y = scaleY(p.y);
      screenPts.push({ name: p.name, x, y });
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fill();
    }
    pointsRef.current = screenPts;
  }, [emb]);

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
          <div className="mb-3 border rounded relative" style={{ height: 400 }}>
            <canvas
              ref={canvasRef}
              style={{ width: '100%', height: 400 }}
              onMouseMove={(e) => {
                const rect = (e.target as HTMLCanvasElement).getBoundingClientRect();
                const mx = e.clientX - rect.left;
                const my = e.clientY - rect.top;
                let best: { name: string; x: number; y: number } | null = null;
                let bestD = 1e9;
                for (const p of pointsRef.current) {
                  const dx = p.x - mx; const dy = p.y - my; const d = Math.sqrt(dx*dx + dy*dy);
                  if (d < bestD) { bestD = d; best = p; }
                }
                if (best && bestD < 12) setHover({ ...best }); else setHover(null);
              }}
              onMouseLeave={() => setHover(null)}
            />
            {hover && (
              <div
                style={{ position: 'absolute', left: hover.x + 8, top: hover.y + 8 }}
                className="text-xs bg-black/80 text-white px-2 py-1 rounded pointer-events-none"
              >
                {hover.name || '(node)'}
              </div>
            )}
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
