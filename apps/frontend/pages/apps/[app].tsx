import { useRouter } from "next/router";
import { useEffect, useMemo, useRef, useState } from "react";
import { externalApps, getExternalUrl } from "@/lib/routes";

export default function ExternalAppPage() {
  const { query } = useRouter();
  const key = String(query.app || "");
  const meta = useMemo(() => Object.values(externalApps).find(a => a.path.endsWith("/" + key)), [key]);
  const url = useMemo(() => {
    const k = (key as any) as keyof typeof externalApps;
    return (externalApps as any)[k] ? getExternalUrl(k) : null;
  }, [key]);

  const [loaded, setLoaded] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const ref = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    const onResize = () => {
      if (!ref.current) return;
      const header = 48; // px
      ref.current.style.height = `${window.innerHeight - header - 24}px`;
    };
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  if (!meta) return <div className="text-red-400">Unbekannte App: {key}</div>;
  if (!url) {
    return (
      <div className="rounded-md border border-amber-400 bg-amber-950/30 p-4 text-sm">
        <b>{meta.label}</b> ist nicht konfiguriert. Setze <code>{meta.env}</code> in <code>.env.local</code>.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold">{meta.label}</h2>
      <div className="text-xs text-neutral-500">Quelle: {url}</div>

      {!loaded && !err && (
        <div className="rounded-lg border border-neutral-800 p-6 text-sm text-neutral-400">Lade {meta.label}…</div>
      )}

      {err && (
        <div className="rounded-lg border border-red-500/50 bg-red-950/30 p-4 text-sm text-red-300">
          Einbettung fehlgeschlagen: {err}<br/>
          Prüfe X-Frame-Options/CSP (frame-ancestors). Reverse-Proxy anpassen.
        </div>
      )}

      <iframe
        ref={ref}
        title={meta.label}
        src={url}
        className="w-full rounded-md border border-neutral-800"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-downloads"
        referrerPolicy="no-referrer"
        onLoad={() => setLoaded(true)}
        onError={() => setErr("Iframe load error")}
      />
    </div>
  );
}
