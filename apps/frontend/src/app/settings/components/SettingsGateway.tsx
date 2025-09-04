'use client';

import { useState } from 'react';
import { loadGateway, saveGateway, getEndpoints } from '../../../../lib/endpoints';

export default function SettingsGateway() {
  const [state, setState] = useState(loadGateway());
  const [result, setResult] = useState<'ok' | 'degraded' | 'fail' | null>(null);

  const update = (next: typeof state) => {
    setState(next);
    saveGateway(next);
  };

  const handleToggle = (e: React.ChangeEvent<HTMLInputElement>) => {
    update({ ...state, enabled: e.target.checked });
  };

  const handleUrl = (e: React.ChangeEvent<HTMLInputElement>) => {
    update({ ...state, url: e.target.value });
  };

  const handleTest = async () => {
    const eps = getEndpoints();
    try {
      const r = await fetch(`${eps.SEARCH_API}/healthz`);
      setResult(r.ok ? 'ok' : 'fail');
    } catch {
      setResult('fail');
    }
  };

  return (
    <div className="space-y-2">
      <label className="flex items-center gap-2">
        <input type="checkbox" checked={state.enabled} onChange={handleToggle} aria-label="Use Gateway proxy" />
        Use Gateway proxy (/api/*)
      </label>
      <label className="flex flex-col">
        Gateway URL
        <input
          type="text"
          value={state.url}
          onChange={handleUrl}
          aria-label="Gateway URL"
          className="border p-1"
        />
      </label>
      <button onClick={handleTest}>Test</button>
      {result && <span data-testid="test-result">{result}</span>}
      <p className="text-xs text-gray-500">
        Traffic läuft über 8610 und kann via OPA geprüft/auditiert werden.
      </p>
    </div>
  );
}
