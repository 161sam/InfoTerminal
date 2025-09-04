import { useState } from "react";
import Layout from "../components/Layout";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Field from "../components/ui/Field";
import StatusPill, { Status } from "../components/ui/StatusPill";
import config from "../lib/config";
import safe from "../lib/safe";

/** Ping an endpoint and return status. */
async function ping(url?: string): Promise<Status> {
  if (!url) return "fail";
  const target = url.endsWith("/healthz") ? url : `${url}/healthz`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 3000);
  try {
    const r = await fetch(target, { signal: controller.signal });
    clearTimeout(timeout);
    return r.ok ? "ok" : "fail";
  } catch {
    return "fail";
  }
}

export default function SettingsPage() {
  if (!config) {
    return (
      <Layout>
        <h1 className="mb-4 text-2xl font-semibold">Settings</h1>
        <StatusPill status="fail">Config not loaded (check import)</StatusPill>
      </Layout>
    );
  }

  const endpoints = [
    { key: "SEARCH_API", label: "Search API", url: config?.SEARCH_API },
    { key: "GRAPH_API", label: "Graph API", url: config?.GRAPH_API },
    { key: "DOCENTITIES_API", label: "Document Entities API", url: config?.DOCENTITIES_API },
    { key: "VIEWS_API", label: "Views API", url: config?.VIEWS_API },
    { key: "NLP_API", label: "NLP API", url: config?.NLP_API },
  ];

  const [status, setStatus] = useState<Record<string, Status>>({});
  const runtime = typeof window === "undefined" ? "server" : "client";

  const handlePing = async (key: string, url?: string) => {
    setStatus((s) => ({ ...s, [key]: "loading" }));
    const st = await ping(url);
    setStatus((s) => ({ ...s, [key]: st }));
  };

  return (
    <Layout>
      <h1 className="mb-4 text-2xl font-semibold">Settings</h1>
      <div className="space-y-6">
        <Card>
          <h2 className="mb-2 text-lg font-semibold">Theme</h2>
          <p className="text-sm text-gray-600">Dark mode toggle coming soon.</p>
        </Card>

        <Card>
          <h2 className="mb-4 text-lg font-semibold">API Endpoints</h2>
          <div className="space-y-4">
            {endpoints.map((e) => (
              <div key={e.key} className="flex items-center gap-2">
                <Field label={e.label} value={e.url ?? ""} readOnly className="flex-1" />
                <Button onClick={() => handlePing(e.key, e.url)}>Ping</Button>
                {status[e.key] && <StatusPill status={status[e.key]} />}
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h2 className="mb-2 text-lg font-semibold">Environment</h2>
          <ul className="text-sm text-gray-600">
            <li>NODE_ENV: {safe(process.env.NODE_ENV, "development")}</li>
            <li>Runtime: {runtime}</li>
          </ul>
        </Card>

        <p className="text-xs text-gray-500">Values are configured via .env.local</p>
      </div>
    </Layout>
  );
}
