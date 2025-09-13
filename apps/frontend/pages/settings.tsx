import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Field from "@/components/ui/Field";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import { toast } from "@/components/ui/toast";
import {
  loadEndpoints,
  saveEndpoints,
  sanitizeUrl,
  validateUrl,
  EndpointSettings,
} from "@/lib/endpoints";
import { safe, safeLog } from "@/lib/safe";
import SettingsGateway from "@/components/settings/SettingsGateway";
import SettingsGraphDeepLink from "@/components/settings/SettingsGraphDeepLink";

export default function SettingsPage() {
  const endpoints = [
    { key: "SEARCH_API", label: "Search API" },
    { key: "GRAPH_API", label: "Graph API" },
    { key: "DOCENTITIES_API", label: "Document Entities API" },
    { key: "VIEWS_API", label: "Views API" },
    { key: "NLP_API", label: "NLP API" },
  ];
  const [values, setValues] = useState(loadEndpoints());
  const [status, setStatus] = useState<Record<string, Status>>({});
  const runtime = typeof window === "undefined" ? "server" : "client";

  const handlePing = async (key: string, url?: string) => {
    setStatus((s) => ({ ...s, [key]: "loading" }));
    const target = sanitizeUrl(url || "");
    const start = performance.now();
    try {
      const r = await fetch(target + "/healthz");
      const latency = Math.round(performance.now() - start);
      setStatus((s) => ({ ...s, [key]: r.ok ? "ok" : "fail" }));
      if (r.ok) toast(`${key} ${latency}ms`, { variant: 'success' });
    } catch (e) {
      safeLog("test connection failed", e);
      setStatus((s) => ({ ...s, [key]: "fail" }));
    }
  };

  const handleSave = () => {
    const sanitized: EndpointSettings = {} as any;
    for (const [k, v] of Object.entries(values)) {
      const s = sanitizeUrl(v || '');
      if (s && !validateUrl(s)) {
        toast(`Invalid URL for ${k}`, { variant: 'error' });
        return;
      }
      sanitized[k] = s;
    }
    saveEndpoints(sanitized);
    toast("Saved", { variant: 'success' });
  };

  return (
    <DashboardLayout title="Settings">
      <h1 className="mb-4">Settings</h1>
      <div className="space-y-6">

        <Card>
          <h2 className="mb-4">API Endpoints</h2>
          <div className="space-y-4">
            {endpoints.map((e) => (
              <div key={e.key} className="flex items-center gap-2">
                <Field
                  label={e.label}
                  name={`endpoint-${e.key.toLowerCase()}`}
                  id={`endpoint-${e.key.toLowerCase()}`}
                  value={values[e.key]}
                  onChange={(ev) =>
                    setValues((v) => ({ ...v, [e.key]: ev.target.value }))
                  }
                  helper={!values[e.key] ? "Not configured" : undefined}
                  className="flex-1"
                />
                <Button onClick={() => handlePing(e.key, values[e.key])}>Test</Button>
                {status[e.key] && <StatusPill status={status[e.key]} />}
              </div>
            ))}
            <div className="pt-2">
              <Button onClick={handleSave}>Save</Button>
            </div>
          </div>
        </Card>

        <Card>
          <h2 className="mb-4">Gateway</h2>
          <SettingsGateway />
        </Card>

        <Card>
          <h2 className="mb-4">Graph Deep-Link</h2>
          <SettingsGraphDeepLink />
        </Card>

        <Card>
          <h2 className="mb-2">Environment</h2>
          <ul className="text-sm text-gray-600">
            <li>NODE_ENV: {safe(process.env.NODE_ENV, "development")}</li>
            <li>Runtime: {runtime}</li>
          </ul>
        </Card>

        <p className="text-xs text-gray-500">Saved to localStorage under it.settings.endpoints</p>
      </div>
    </DashboardLayout>
  );
}
