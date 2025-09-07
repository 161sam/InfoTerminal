'use client';

import { useEffect, useState } from 'react';
import { toast } from '@/components/ui/toast';
import {
  buildGraphDeepLink,
  getGraphDeeplinkBase,
  DEEPLINK_STORAGE_KEY,
} from '@/lib/deeplink';
import { GRAPH_DEEPLINK_FALLBACK } from '@/lib/config';

export default function SettingsGraphDeepLink() {
  const [value, setValue] = useState('');
  const [mode, setMode] = useState<'rel' | 'abs'>('rel');
  const [testLink, setTestLink] = useState<string | null>(null);

  useEffect(() => {
    const base = getGraphDeeplinkBase();
    setValue(base);
    setMode(base.startsWith('http://') || base.startsWith('https://') ? 'abs' : 'rel');
  }, []);

  const validate = (val: string): boolean => {
    if (mode === 'rel') {
      return val.startsWith('/') && val.includes('focus=');
    }
    try {
      const u = new URL(val);
      return val.includes('focus=') && !!u;
    } catch {
      return false;
    }
  };

  const handleSave = () => {
    if (!validate(value)) {
      toast('Invalid base', { variant: 'error' });
      return;
    }
    if (typeof window !== 'undefined') {
      localStorage.setItem(DEEPLINK_STORAGE_KEY, value);
    }
    toast('Saved', { variant: 'success' });
  };

  const handleTest = () => {
    const link = buildGraphDeepLink({ id: 'demo', base: value });
    setTestLink(link);
    toast('Generated', { variant: 'success' });
  };

  const handleReset = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(DEEPLINK_STORAGE_KEY);
    }
    setValue(GRAPH_DEEPLINK_FALLBACK);
    setMode(
      GRAPH_DEEPLINK_FALLBACK.startsWith('http://') ||
        GRAPH_DEEPLINK_FALLBACK.startsWith('https://')
        ? 'abs'
        : 'rel'
    );
    toast('Reset', { variant: 'success' });
  };

  return (
    <div className="space-y-2">
      <label className="flex flex-col">
        Graph Deep-Link Base
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          aria-label="Graph Deep-Link Base"
          className="border p-1"
        />
      </label>
      <div className="flex gap-4">
        <label className="flex items-center gap-1">
          <input
            type="radio"
            name="dl-mode"
            value="rel"
            checked={mode === 'rel'}
            onChange={() => setMode('rel')}
          />
          Relativ (z. B. /graphx?focus=)
        </label>
        <label className="flex items-center gap-1">
          <input
            type="radio"
            name="dl-mode"
            value="abs"
            checked={mode === 'abs'}
            onChange={() => setMode('abs')}
          />
          Absolut (z. B. https://graph.dev/graphx?focus=)
        </label>
      </div>
      <div className="flex gap-2">
        <button onClick={handleTest}>Test</button>
        <button onClick={handleSave}>Speichern</button>
        <button onClick={handleReset}>Zurücksetzen</button>
      </div>
      {testLink && (
        <div data-testid="test-link" className="text-xs">
          <code>{testLink}</code>
        </div>
      )}
    </div>
  );
}
