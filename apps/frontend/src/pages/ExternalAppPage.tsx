import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import { appRoutes, getExternalUrl } from "../routes/appRoutes";

/**
 * Generische Seite für externe GUIs via iframe
 * - sichere Defaults (sandbox, referrerPolicy)
 * - automatische Höhe (Window minus Header)
 * - simple Fehleranzeige, wenn X-Frame-Options/CSP blockiert
 */
export default function ExternalAppPage() {
  const { pathname } = useLocation();
  const route = useMemo(() => appRoutes.find(r => r.path === pathname), [pathname]);
  const url = route ? getExternalUrl(route) : null;

  const [err, setErr] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);
  const ref = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    const onMessage = (ev: MessageEvent) => {
      // optional: postMessage handshake für Integrationen
    };
    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, []);

  useEffect(() => {
    const onResize = () => {
      if (!ref.current) return;
      const headerHeight = 48; // Höhe des Topbars (px), falls angepasst → mitziehen
      ref.current.style.height = `${window.innerHeight - headerHeight - 16 /* padding estimate */}px`;
    };
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  if (!route) return <div className="text-red-600">Route not found.</div>;
  if (!url) {
    return (
      <div className="rounded-md border border-amber-300 bg-amber-50 p-4 text-sm">
        <b>{route.label}</b> ist nicht konfiguriert. Bitte setze <code>{route.urlEnvVar}</code> in deiner <code>.env</code>.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold">{route.label}</h2>
      <div className="text-xs text-neutral-500">Quelle: {url}</div>

      {!loaded && !err && (
        <div className="rounded-lg border p-6 text-sm text-neutral-500">Lade {route.label}…</div>
      )}

      {err && (
        <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-700">
          Einbettung fehlgeschlagen: {err}<br/>
          Prüfe X-Frame-Options oder CSP (frame-ancestors). Siehe „Embedding Hinweise“ in der Doku.
        </div>
      )}

      <iframe
        ref={ref}
        title={route.label}
        src={url}
        className="w-full rounded-lg border"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-downloads"
        referrerPolicy="no-referrer"
        onLoad={() => setLoaded(true)}
        onError={() => setErr("Iframe load error")}
      />
    </div>
  );
}
