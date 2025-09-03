import { useState } from 'react';
import Header from '@/components/layout/Header';
import { useDemoLoader } from '@/hooks/useDemoLoader';

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
    <>
      {/* TODO: Replace with DashboardLayout to avoid duplicate headers */}
      <Header />
      <main style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'ui-sans-serif' }}>
        <h1>Demo & Beispiele</h1>
        <div>
          {Object.keys(opts).map((k) => (
            <label key={k} style={{ display: 'block' }}>
              <input type="checkbox" checked={(opts as any)[k]} onChange={() => toggle(k)} /> {k}
            </label>
          ))}
          <button onClick={() => loadDemo(opts)} disabled={loading}>
            Demo-Daten laden
          </button>
        </div>
        {loading && <div>Loading...</div>}
        {result && (
          <div>
            <h3>Ergebnis</h3>
            <ul>
              {result.ingested.map((r: any) => (
                <li key={r.file}>{r.file}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </>
  );
}
