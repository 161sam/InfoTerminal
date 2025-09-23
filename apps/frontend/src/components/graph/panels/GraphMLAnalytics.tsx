import React, { useState, useRef, useEffect } from 'react';
import { BarChart3, Brain } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import Button from '@/components/ui/button';
import { LoadingSpinner, EmptyState } from '@/components/ui/loading';

interface MLAnalyticsProps {
  onAnalysisResult?: (algorithm: string, items: any[]) => void;
}

export default function GraphMLAnalytics({ onAnalysisResult }: MLAnalyticsProps) {
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
      const nodes = data.nodes || [];
      setPr(nodes);
      onAnalysisResult?.('pagerank', nodes);
    } finally { 
      setLoading(false); 
    }
  };

  const runN2V = async () => {
    setLoading(true);
    try {
      const r = await fetch('/api/graph/analytics/embeddings/node2vec?dimensions=8');
      const data = await r.json();
      const items = data || { items: [] };
      setEmb(items);
      onAnalysisResult?.('node2vec', items.items || []);
    } finally { 
      setLoading(false); 
    }
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
    <div className="space-y-6">
      <Panel title="PageRank Centrality">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Button 
              onClick={runPR} 
              disabled={loading}
              className="inline-flex items-center gap-2"
            >
              {loading ? (
                <LoadingSpinner size="sm" text="" />
              ) : (
                <BarChart3 size={16} />
              )}
              Run PageRank
            </Button>
            <span className="text-sm text-gray-500 dark:text-slate-400">
              Identify most influential nodes
            </span>
          </div>
          
          <div className="space-y-1 max-h-64 overflow-y-auto">
            {loading ? (
              <LoadingSpinner layout="block" text="Running PageRank Analysis" />
            ) : pr.length > 0 ? (
              pr.map((n: any, i: number) => (
                <div key={i} className="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
                  <span className="font-medium text-gray-900 dark:text-slate-100">
                    {n.name || n.node_id}
                  </span>
                  <span className="text-sm text-gray-500 dark:text-slate-400 font-mono">
                    {(n.score ?? n.centrality_score ?? 0).toFixed(4)}
                  </span>
                </div>
              ))
            ) : (
              <EmptyState
                icon={BarChart3}
                title="No PageRank Results"
                message="Click 'Run PageRank' to analyze node centrality"
                action={{
                  label: "Run Analysis",
                  onClick: runPR
                }}
              />
            )}
          </div>
        </div>
      </Panel>

      <Panel title="Node2Vec Embeddings">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Button 
              onClick={runN2V} 
              disabled={loading}
              variant="secondary"
              className="inline-flex items-center gap-2"
            >
              {loading ? (
                <LoadingSpinner size="sm" text="" />
              ) : (
                <Brain size={16} />
              )}
              Run Node2Vec
            </Button>
            <span className="text-sm text-gray-500 dark:text-slate-400">
              Generate 8D embeddings (2D preview)
            </span>
          </div>
          
          <div className="relative border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden" style={{ height: 400 }}>
            {loading ? (
              <LoadingSpinner layout="overlay" text="Generating Embeddings" />
            ) : (
              <>
                <canvas
                  ref={canvasRef}
                  style={{ width: '100%', height: 400 }}
                  className="cursor-crosshair"
                  onMouseMove={(e) => {
                    const rect = (e.target as HTMLCanvasElement).getBoundingClientRect();
                    const mx = e.clientX - rect.left;
                    const my = e.clientY - rect.top;
                    let best: { name: string; x: number; y: number } | null = null;
                    let bestD = 1e9;
                    for (const p of pointsRef.current) {
                      const dx = p.x - mx; 
                      const dy = p.y - my; 
                      const d = Math.sqrt(dx*dx + dy*dy);
                      if (d < bestD) { 
                        bestD = d; 
                        best = p; 
                      }
                    }
                    if (best && bestD < 12) setHover({ ...best }); 
                    else setHover(null);
                  }}
                  onMouseLeave={() => setHover(null)}
                />
                {hover && (
                  <div
                    style={{ position: 'absolute', left: hover.x + 8, top: hover.y + 8 }}
                    className="text-xs bg-black/80 text-white px-2 py-1 rounded pointer-events-none z-10"
                  >
                    {hover.name || '(node)'}
                  </div>
                )}
                {!emb.items?.length && !loading && (
                  <EmptyState
                    icon={Brain}
                    title="No Embeddings Generated"
                    message="Click 'Run Node2Vec' to generate embeddings"
                    action={{
                      label: "Generate Embeddings",
                      onClick: runN2V
                    }}
                  />
                )}
              </>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-48 overflow-y-auto">
            {(emb.items || []).slice(0, 20).map((e: any, i: number) => (
              <div key={i} className="text-xs p-2 border border-gray-200 dark:border-gray-700 rounded">
                <div className="font-medium text-gray-900 dark:text-slate-100">
                  {e.name || `node_${i}`}
                </div>
                <div className="text-gray-500 dark:text-slate-400 font-mono">
                  [{(e.embedding || []).slice(0, 8).map((x: number) => x.toFixed(2)).join(', ')}]
                </div>
              </div>
            ))}
          </div>
        </div>
      </Panel>
    </div>
  );
}
