import { useState } from 'react';
import { useDemoLoader } from '@/hooks/useDemoLoader';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

export default function DemoPage() {
  const { loading, result, loadDemo } = useDemoLoader();
  const [opts, setOpts] = useState({
    ingestAleph: true,
    annotate: true,
    seedGraph: false,
    seedSearch: false,
    reset: false,
  });

  const toggle = (k: string) => setOpts((o) => ({ ...o, [k]: !(o as any)[k] }));

  return (
    <DashboardLayout title="Demo & Beispiele">
      <div className="max-w-2xl space-y-6">
        <h1 className="text-2xl font-semibold">Demo & Beispiele</h1>
        <Panel>
          <div className="space-y-4">
            <div className="space-y-1">
              {Object.keys(opts).map((k) => (
                <label key={k} className="block text-sm">
                  <input
                    type="checkbox"
                    className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    checked={(opts as any)[k]}
                    onChange={() => toggle(k)}
                  />
                  {k}
                </label>
              ))}
            </div>
            <button
              className="btn btn-primary"
              onClick={() => loadDemo(opts)}
              disabled={loading}
            >
              {loading ? 'Lade…' : 'Demo-Daten laden'}
            </button>
            {loading && <div>Loading...</div>}
            {result && (
              <div>
                <h3 className="font-semibold mb-2">Ergebnis</h3>
                <ul className="list-disc list-inside">
                  {result.ingested.map((r: any) => (
                    <li key={r.file}>{r.file}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </Panel>
      </div>
    </DashboardLayout>
  );
}
