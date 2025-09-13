import React, { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/Button";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import GraphViewerCytoscape from "@/components/GraphViewerCytoscape";
import config from "@/lib/config";
import { getEgo, loadPeople, getShortestPath, exportDossier } from "@/lib/api";
import { toast } from "@/components/ui/toast";
import DossierButton from "@/components/DossierButton";
import AnalysisPanel from "@/components/graph/AnalysisPanel";

function DevPanel() {
  if (process.env.NODE_ENV === "production") return null;

  const seed = async () => {
    const rows = [
      { id: "alice", name: "Alice", knows_id: "bob" },
      { id: "bob", name: "Bob", knows_id: "carol" },
      { id: "carol", name: "Carol", knows_id: null },
    ];
    try {
      const { inserted } = await loadPeople(rows);
      alert(`Seed OK: inserted=${inserted}`);
    } catch (e: any) {
      alert(`Seed failed: ${e?.message || e}`);
    }
  };

  const ego = async () => {
    try {
      const { data } = await getEgo({ label: "Person", key: "id", value: "alice", depth: 2, limit: 50 });
      const nodes = data?.nodes?.length ?? 0;
      const edges = data?.relationships?.length ?? 0;
      alert(`Ego(Person id=alice): nodes=${nodes} edges=${edges}`);
    } catch (e: any) {
      alert(`Ego failed: ${e?.message || e}`);
    }
  };

  const exportAlice = async () => {
    try {
      const r = await exportDossier({ label: "Person", key: "id", value: "alice", depth: 2 });
      const blob = new Blob([JSON.stringify(r, null, 2)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "dossier_person_alice.json";
      a.click();
      URL.revokeObjectURL(a.href);
    } catch (e: any) {
      alert(`Export failed: ${e?.message || e}`);
    }
  };

  const exportEgo = async () => {
    try {
      const { data } = await getEgo({ label: "Person", key: "id", value: "alice", depth: 2, limit: 50 });
      const blob = new Blob([JSON.stringify({ ok: true, data }, null, 2)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "ego_person_alice.json";
      a.click();
      URL.revokeObjectURL(a.href);
    } catch (e: any) {
      alert(`Export failed: ${e?.message || e}`);
    }
  };

  return (
    <div style={{ display: "grid", gap: 8, padding: 12, border: "1px dashed var(--border, #555)", borderRadius: 8, marginTop: 16 }}>
      <strong>Dev Tools (local)</strong>
      <button onClick={seed} style={{ padding: 8, borderRadius: 8 }}>Seed Demo People</button>
      <button onClick={ego} style={{ padding: 8, borderRadius: 8 }}>Test Ego(Alice)</button>
      <button onClick={exportAlice} style={{ padding: 8, borderRadius: 8 }}>Export Dossier (Alice)</button>
      <button onClick={exportEgo} style={{ padding: 8, borderRadius: 8 }}>Export Ego (Alice)</button>
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
  const [egoInfo, setEgoInfo] = useState("");
  const [srcLabel, setSrcLabel] = useState("Person");
  const [srcKey, setSrcKey] = useState("id");
  const [srcValue, setSrcValue] = useState("");
  const [dstLabel, setDstLabel] = useState("Person");
  const [dstKey, setDstKey] = useState("id");
  const [dstValue, setDstValue] = useState("");
  const [maxLen, setMaxLen] = useState(4);
  const [directed, setDirected] = useState(false);
  const [elements, setElements] = useState<any[]>([]);

  const pingGraph = async () => {
    setGraphStatus("loading");
    setGraphStatus(await ping(config?.GRAPH_API));
  };
  const pingViews = async () => {
    setViewsStatus("loading");
    setViewsStatus(await ping(config?.VIEWS_API));
  };

  const runEgo = async () => {
    try {
      const { data, counts } = await getEgo({ label:"Person", key:"id", value:"alice", depth:2, limit:50 });
      setEgoInfo(`nodes=${counts.nodes ?? data.nodes?.length ?? 0}, rels=${counts.relationships ?? data.relationships?.length ?? 0}`);
    } catch (e: any) {
      toast(e?.message || "Ego failed", { variant: 'error' });
    }
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

  const findPath = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await getShortestPath({
        srcLabel,
        srcKey,
        srcValue,
        dstLabel,
        dstKey,
        dstValue,
        maxLen,
      });
      const nodes = (data.nodes || []).map((n: any) => ({
        data: { id: String(n.id), label: n.properties?.name || String(n.id) },
      }));
      const edges = (data.relationships || []).map((r: any) => ({
        data: {
          id: String(r.id),
          source: String(r.start),
          target: String(r.end),
          label: r.type,
        },
      }));
      setElements([...nodes, ...edges]);
    } catch (e: any) {
      toast(e?.message || "path failed", { variant: 'error' });
    }
  };

  return (
    <DashboardLayout title="GraphX">
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold mb-6">GraphX</h1>
        <Panel>
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
        </Panel>

        <Panel>
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
        </Panel>

        {/* Export graph query as dossier */}
        <DossierButton getPayload={() => ({ query, entities: [], graphSelection: { nodes: [], edges: [] } })} />

        <Panel>
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
        </Panel>

        <Panel>
          <h2 className="mb-2">Ego Sample</h2>
          <Button onClick={runEgo}>Run Ego(Person id=alice)</Button>
          {egoInfo && <p className="mt-2 text-sm">{egoInfo}</p>}
        </Panel>

        <Panel>
          <h2 className="mb-2">Shortest Path</h2>
          <form onSubmit={findPath} className="grid gap-2 md:grid-cols-3">
            <input
              placeholder="srcLabel"
              value={srcLabel}
              onChange={(e) => setSrcLabel(e.target.value)}
              className="rounded border p-1"
            />
            <input
              placeholder="srcKey"
              value={srcKey}
              onChange={(e) => setSrcKey(e.target.value)}
              className="rounded border p-1"
            />
            <input
              placeholder="srcValue"
              value={srcValue}
              onChange={(e) => setSrcValue(e.target.value)}
              className="rounded border p-1"
            />
            <input
              placeholder="dstLabel"
              value={dstLabel}
              onChange={(e) => setDstLabel(e.target.value)}
              className="rounded border p-1"
            />
            <input
              placeholder="dstKey"
              value={dstKey}
              onChange={(e) => setDstKey(e.target.value)}
              className="rounded border p-1"
            />
            <input
              placeholder="dstValue"
              value={dstValue}
              onChange={(e) => setDstValue(e.target.value)}
              className="rounded border p-1"
            />
            <input
              type="number"
              placeholder="maxLen"
              value={maxLen}
              onChange={(e) => setMaxLen(parseInt(e.target.value, 10))}
              className="rounded border p-1"
            />
            <label className="flex items-center gap-1">
              <input
                type="checkbox"
                checked={directed}
                onChange={(e) => setDirected(e.target.checked)}
              />
              Directed
            </label>
            <Button type="submit">Find</Button>
          </form>
          {elements.length > 0 && (
            <div className="mt-4">
              <GraphViewerCytoscape elements={elements} directed={directed} />
            </div>
          )}
        </Panel>
      </div>
      <AnalysisPanel />
      <DevPanel />
    </DashboardLayout>
  );
}
