"use client";
import { useState } from "react";
import config from "@/lib/config";

export default function DossierButton({ getPayload }: { getPayload: () => any }) {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const cfg = config || { VIEWS_API: process.env.NEXT_PUBLIC_VIEWS_API || "http://localhost:8403" };

  async function build() {
    setBusy(true);
    setMsg(null);
    const payload = getPayload();
    const res = await fetch(`${cfg.VIEWS_API}/dossier`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setBusy(false);
    setMsg(`Erstellt: ${data.md_path}`);
  }

  return (
    <div className="flex items-center gap-2">
      <button disabled={busy} onClick={build} className="px-3 py-2 rounded-xl border">
        {busy ? "Erzeuge Dossier…" : "Dossier exportieren"}
      </button>
      {msg && <span className="text-sm opacity-75">{msg}</span>}
    </div>
  );
}
