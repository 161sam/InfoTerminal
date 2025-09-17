import { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

export default function EthicsPage() {
  const [text, setText] = useState('Die Firma A traf am 01/08/2025 eine Vereinbarung.');
  const [query, setQuery] = useState('Firma Vereinbarung');
  const [explain, setExplain] = useState<any>(null);

  const run = async () => {
    const r = await fetch('/api/xai/explain', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text, query }) });
    setExplain(await r.json());
  };

  return (
    <DashboardLayout title="Ethical AI Toolkit" subtitle="Basic text explanations and model card">
      <div className="max-w-5xl mx-auto space-y-6 p-4">
        <Panel title="Explain Text">
          <div className="space-y-2">
            <textarea className="w-full border rounded p-2" rows={4} value={text} onChange={e => setText(e.target.value)} />
            <input className="w-full border rounded p-2" value={query} onChange={e => setQuery(e.target.value)} placeholder="Query terms" />
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={run}>Explain</button>
          </div>
          {explain && (
            <div className="mt-4">
              <div className="text-sm text-gray-600">Highlights:</div>
              <div className="mt-2 p-2 border rounded">
                {(explain.tokens || []).map((t: string, i: number) => {
                  const matched = (explain.highlights || []).some((h: any) => h.index === i);
                  return <span key={i} className={matched ? 'bg-yellow-200 mx-0.5' : 'mx-0.5'}>{t}</span>;
                })}
              </div>
            </div>
          )}
        </Panel>
      </div>
    </DashboardLayout>
  );
}

