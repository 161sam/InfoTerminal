import { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

export default function LegalPage() {
  const [q, setQ] = useState('§23 Arbeitsschutz');
  const [entity, setEntity] = useState('Automotive');
  const [results, setResults] = useState<any[]>([]);
  const [rerank, setRerank] = useState(true);
  const [linkSector, setLinkSector] = useState<Record<string,string>>({});
  const [context, setContext] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    setLoading(true);
    try {
      const r = await fetch(`/api/rag/law/retrieve?q=${encodeURIComponent(q)}&rerank=${rerank ? '1' : '0'}`);
      const data = await r.json();
      setResults(data.items || []);
    } finally { setLoading(false); }
  };
  const loadContext = async () => {
    setLoading(true);
    try {
      const r = await fetch(`/api/rag/law/context?entity=${encodeURIComponent(entity)}`);
      const data = await r.json();
      setContext(data.laws || []);
    } finally { setLoading(false); }
  };

  return (
    <DashboardLayout title="Legal / Compliance" subtitle="Law retrieval and compliance context">
      <div className="max-w-6xl mx-auto space-y-6 p-4">
        <Panel title="Retrieve Laws">
          <div className="flex gap-2 items-center">
            <input className="flex-1 border rounded px-3 py-2" value={q} onChange={e => setQ(e.target.value)} placeholder="Query (e.g., §23 ArbSchG)" />
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={search} disabled={loading}>Search</button>
          </div>
          <div className="mt-2 flex items-center gap-2 text-sm">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={rerank} onChange={e => setRerank(e.target.checked)} />
              Rerank results (basic)
            </label>
          </div>
          <div className="mt-4 space-y-3">
            {results.map((it, idx) => (
              <div key={idx} className="p-3 border rounded space-y-2">
                <div className="text-sm text-gray-500">{it.id}</div>
                <div className="font-medium">{it.title || it.paragraph || 'Law paragraph'}</div>
                <div className="text-sm text-gray-700 whitespace-pre-wrap">{it.text}</div>
                <div className="flex gap-2 items-center pt-2 border-t">
                  <input
                    className="flex-1 border rounded px-2 py-1 text-sm"
                    placeholder="Sector (e.g., Automotive)"
                    value={linkSector[it.id] || ''}
                    onChange={e => setLinkSector(prev => ({...prev, [it.id]: e.target.value}))}
                  />
                  <button
                    className="px-3 py-1.5 text-sm bg-gray-800 text-white rounded"
                    onClick={async () => {
                      const sector = (linkSector[it.id] || '').trim();
                      if (!sector) return alert('Please enter a sector name');
                      const payload = { doc: { id: it.id, title: it.title || it.paragraph || '', text: it.text || '' }, applies_to: [sector] };
                      const r = await fetch('/api/rag/graph/law/upsert', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
                      if (r.ok) alert(`Linked ${it.id} to sector '${sector}'`); else alert(`Link failed: ${await r.text()}`);
                    }}
                  >
                    Link to Sector
                  </button>
                  <button
                    className="px-3 py-1.5 text-sm bg-gray-600 text-white rounded"
                    onClick={async () => {
                      const firm = prompt('Firm name to link to:', 'Firma A')?.trim();
                      if (!firm) return;
                      const payload = { doc: { id: it.id, title: it.title || it.paragraph || '', text: it.text || '' }, firms: [firm] };
                      const r = await fetch('/api/rag/graph/law/upsert', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
                      if (r.ok) alert(`Linked ${it.id} to firm '${firm}'`); else alert(`Link failed: ${await r.text()}`);
                    }}
                  >
                    Link to Firm
                  </button>
                </div>
              </div>
            ))}
            {!results.length && <div className="text-sm text-gray-500">No results yet</div>}
          </div>
        </Panel>

        <Panel title="Context by Entity">
          <div className="flex gap-2 items-center">
            <input className="flex-1 border rounded px-3 py-2" value={entity} onChange={e => setEntity(e.target.value)} placeholder="Entity/Sector" />
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={loadContext} disabled={loading}>Load Context</button>
          </div>
          <div className="mt-4 space-y-3">
            {context.map((it, idx) => (
              <div key={idx} className="p-3 border rounded">
                <div className="text-sm text-gray-500">{it.id}</div>
                <div className="font-medium">{it.title || it.paragraph || 'Law paragraph'}</div>
              </div>
            ))}
            {!context.length && <div className="text-sm text-gray-500">No context yet</div>}
          </div>
        </Panel>
      </div>
    </DashboardLayout>
  );
}
