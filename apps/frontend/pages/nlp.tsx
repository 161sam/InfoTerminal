import { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { getApis } from '@/lib/config';

export default function NLPPage() {
  const { DOC_ENTITIES_API } = getApis();
  const [text, setText] = useState('');
  const [lang, setLang] = useState('en');
  const [doSummary, setDoSummary] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [tab, setTab] = useState<'html' | 'json'>('html');
  const [error, setError] = useState<string | null>(null);
  const [linkStatus, setLinkStatus] = useState<string | null>(null);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => {
      setText(reader.result as string);
    };
    reader.readAsText(f);
  };

  const annotate = async () => {
    try {
      const r = await fetch(`${DOC_ENTITIES_API}/annotate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, lang, do_summary: doSummary })
      });
      if (!r.ok) throw new Error('bad response');
      const data = await r.json();
      setResult(data);
      setError(null);
    } catch {
      setError('NLP service unavailable');
    }
  };

  const link = async () => {
    if (!result) return;
    setLinkStatus('pending');
    const r = await fetch(`${DOC_ENTITIES_API}/link-entities`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ doc_id: result.doc_id, entities: result.entities })
    });
    setLinkStatus(r.ok ? 'ok' : 'error');
  };

  return (
    <DashboardLayout title="NLP Annotation">
      <div className="max-w-4xl mx-auto space-y-6">
        {error && (
          <div className="p-4 bg-red-100 text-red-800 rounded">{error}</div>
        )}
        <Panel title="Input">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={8}
            className="w-full border p-2 rounded mb-2"
            placeholder="Paste text or upload a PDF/text file"
          />
          <input type="file" accept=".txt,application/pdf" onChange={handleFile} className="mb-2" />
          <div className="flex items-center gap-4 mb-2">
            <label className="flex items-center gap-1">
              <span>Lang:</span>
              <select value={lang} onChange={(e) => setLang(e.target.value)} className="border p-1 rounded">
                <option value="en">en</option>
                <option value="de">de</option>
              </select>
            </label>
            <label className="flex items-center gap-1">
              <input type="checkbox" checked={doSummary} onChange={(e) => setDoSummary(e.target.checked)} />
              <span>Summary</span>
            </label>
            <button onClick={annotate} className="px-4 py-1 bg-blue-600 text-white rounded">Annotate</button>
          </div>
        </Panel>

        {result && (
          <Panel title="Result">
            <div className="mb-2 flex gap-2">
              <button onClick={() => setTab('html')} className={`px-2 py-1 border rounded ${tab === 'html' ? 'bg-gray-200' : ''}`}>HTML</button>
              <button onClick={() => setTab('json')} className={`px-2 py-1 border rounded ${tab === 'json' ? 'bg-gray-200' : ''}`}>JSON</button>
              <button onClick={link} className="ml-auto px-2 py-1 border rounded">In Graph verknüpfen</button>
            </div>
            {linkStatus && <div className="text-sm mb-2">Hook: {linkStatus}</div>}
            {tab === 'html' && (
              <div className="border p-2 rounded" dangerouslySetInnerHTML={{ __html: result.html }} />
            )}
            {tab === 'json' && (
              <pre className="text-sm bg-gray-50 p-2 rounded overflow-x-auto">{JSON.stringify(result, null, 2)}</pre>
            )}
          </Panel>
        )}
      </div>
    </DashboardLayout>
  );
}
