import React, { useState } from "react";
import Layout from "@/components/Layout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import config from "@/lib/config";
import { getEgo, loadPeople } from "@/lib/api";

function DevPanel() {
  if (process.env.NODE_ENV === "production") return null;

  const seed = async () => {
    const rows = [
      { id: "alice", name: "Alice", knows_id: "bob" },
      { id: "bob", name: "Bob", knows_id: "carol" },
      { id: "carol", name: "Carol", knows_id: null },
    ];
    try {
      const r = await loadPeople(rows);
      alert(`Seed OK: nodesCreated=${r.nodesCreated} relsCreated=${r.relsCreated}`);
    } catch (e: any) {
      alert(`Seed failed: ${e?.message || e}`);
    }
  };

  const ego = async () => {
    try {
      const data = await getEgo({ label: "Person", key: "id", value: "alice", depth: 2, limit: 50 });
      const nodes = data?.nodes?.length ?? 0;
      const edges = data?.relationships?.length ?? 0;
      alert(`Ego(Person id=alice): nodes=${nodes} edges=${edges}`);
    } catch (e: any) {
      alert(`Ego failed: ${e?.message || e}`);
    }
  };

  return (
    <div style={{ display: "grid", gap: 8, padding: 12, border: "1px dashed var(--border, #555)", borderRadius: 8, marginTop: 16 }}>
      <strong>Dev Tools (local)</strong>
      <button onClick={seed} style={{ padding: 8, borderRadius: 8 }}>Seed Demo People</button>
      <button onClick={ego} style={{ padding: 8, borderRadius: 8 }}>Test Ego(Alice)</button>
    </div>
  );
}

/** Ping a URL's /healthz endpoint. */
async function ping(url?: string): Promise<Status> {
  if (!url) return "fail";
  try {
    const r = await fetch(url + "/healthz");
    return r.ok ? "ok" : "fail";
  } catch {
    return "fail";
  }
}

export default function GraphXPage() {
  const [graphStatus, setGraphStatus] = useState<Status>();
  const [viewsStatus, setViewsStatus] = useState<Status>();
  const [query, setQuery] = useState("MATCH (n) RETURN n LIMIT 5");
  const [output, setOutput] = useState<any>(null);
  const [runStatus, setRunStatus] = useState<Status>();

  const pingGraph = async () => {
    setGraphStatus("loading");
    setGraphStatus(await ping(config?.GRAPH_API));
  };
  const pingViews = async () => {
    setViewsStatus("loading");
    setViewsStatus(await ping(config?.VIEWS_API));
  };

  const runQuery = async () => {
    setRunStatus("loading");
    const base = config?.GRAPH_API;
    if (!base) {
      setRunStatus("fail");
      setOutput({ error: "Graph API not configured" });
      return;
    }
    try {
      let r = await fetch(`${base}/query`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (r.status === 404) {
        r = await fetch(`${base}/nodes?limit=25`);
      }
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      setOutput(j);
      setRunStatus("ok");
    } catch (e: any) {
      setRunStatus("fail");
      setOutput({ error: e.message || "query failed" });
    }
  };

  return (
    <Layout showHealth>
      <h1 className="mb-4">GraphX</h1>
      <div className="space-y-6">
        <Card>
          <h2 className="mb-2">Connections</h2>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2">
              <Button onClick={pingGraph}>Ping Graph API</Button>
              {graphStatus && <StatusPill status={graphStatus} />}
            </div>
            <div className="flex items-center gap-2">
              <Button onClick={pingViews}>Ping Views API</Button>
              {viewsStatus && <StatusPill status={viewsStatus} />}
            </div>
          </div>
        </Card>

        <Card>
          <h2 className="mb-2">Query</h2>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="mb-2 w-full rounded-md border-gray-300 p-2 text-sm focus:border-primary-500 focus:ring-primary-500"
            rows={4}
          />
          <div className="flex items-center gap-2">
            <Button onClick={runQuery} isLoading={runStatus === "loading"}>
              Run
            </Button>
            {runStatus && runStatus !== "loading" && (
              <StatusPill status={runStatus} />
            )}
          </div>
        </Card>

        <Card>
          <h2 className="mb-2">Output</h2>
          {output ? (
            <pre className="max-h-96 overflow-auto text-xs">
              {JSON.stringify(output, null, 2)}
            </pre>
          ) : (
            <p className="text-sm text-gray-600">
              Run a query to see results
            </p>
          )}
        </Card>
      </div>
      <DevPanel />
    </Layout>
  );
}
