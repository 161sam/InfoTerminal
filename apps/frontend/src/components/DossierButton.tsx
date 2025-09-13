"use client";
import { useState } from "react";
import config from "@/lib/config";

export default function DossierButton({ getPayload }: { getPayload: () => any }) {
  const [busy, setBusy] = useState(false);
  const [format, setFormat] = useState('md');
  const [links, setLinks] = useState<{ md?: string; pdf?: string } | null>(null);
  const cfg = config || { VIEWS_API: process.env.NEXT_PUBLIC_VIEWS_API || 'http://localhost:8403' };

  async function build() {
    setBusy(true);
    setLinks(null);
    const payload = { ...getPayload(), format };
    const res = await fetch(`${cfg.VIEWS_API}/dossier`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setBusy(false);
    setLinks({ md: data.md_path, pdf: data.pdf_path });
  }

  return (
    <div className="flex items-center gap-2">
      <select
        value={format}
        onChange={(e) => setFormat(e.target.value)}
        className="border rounded px-2 py-1"
      >
        <option value="md">MD</option>
        <option value="pdf">PDF</option>
        <option value="both">Both</option>
      </select>
      <button disabled={busy} onClick={build} className="px-3 py-2 rounded-xl border">
        {busy ? 'Erzeuge Dossier…' : 'Dossier exportieren'}
      </button>
      {links && (
        <span className="text-sm opacity-75">
          {links.md && (
            <a href={links.md} className="underline mr-2">
              MD
            </a>
          )}
          {links.pdf && (
            <a href={links.pdf} className="underline">
              PDF
            </a>
          )}
        </span>
      )}
    </div>
  );
}
