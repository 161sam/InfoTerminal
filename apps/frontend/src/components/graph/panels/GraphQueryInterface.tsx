import React, { useState } from "react";
import { Play, Code2 } from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import { LoadingSpinner } from "@/components/ui/loading";
import config from "@/lib/config";

interface QueryInterfaceProps {
  initialQuery?: string;
  onQueryResult?: (result: any) => void;
}

const SAMPLE_QUERIES = [
  {
    name: "All Nodes Overview",
    query: "MATCH (n) RETURN n LIMIT 25",
    description: "Get a general overview of your graph",
  },
  {
    name: "Person Connections",
    query: "MATCH (p:Person)-[r]-(n) RETURN p, r, n LIMIT 20",
    description: "Find connections between people",
  },
  {
    name: "Organizations Network",
    query: "MATCH (o:Organization)-[r]-(n) RETURN o, r, n LIMIT 15",
    description: "Explore organizational relationships",
  },
  {
    name: "Central Nodes",
    query: "MATCH (n)-[r]-() RETURN n, COUNT(r) as degree ORDER BY degree DESC LIMIT 10",
    description: "Find the most connected nodes",
  },
];

export default function GraphQueryInterface({
  initialQuery = "MATCH (n) RETURN n LIMIT 10",
  onQueryResult,
}: QueryInterfaceProps) {
  const [customQuery, setCustomQuery] = useState(initialQuery);
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryStatus, setQueryStatus] = useState<Status>();

  const runCustomQuery = async () => {
    setQueryStatus("loading");
    const base = config?.GRAPH_API;
    if (!base) {
      setQueryStatus("fail");
      const error = { error: "Graph API not configured" };
      setQueryResult(error);
      onQueryResult?.(error);
      return;
    }

    try {
      let response = await fetch(`${base}/query`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query: customQuery }),
      });

      if (response.status === 404) {
        response = await fetch(`${base}/nodes?limit=25`);
      }

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const result = await response.json();
      setQueryResult(result);
      setQueryStatus("ok");
      onQueryResult?.(result);
    } catch (e: any) {
      setQueryStatus("fail");
      const error = { error: e.message || "Query failed" };
      setQueryResult(error);
      onQueryResult?.(error);
    }
  };

  return (
    <div className="space-y-6">
      <Panel title="Custom Graph Queries">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
              Cypher Query
            </label>
            <textarea
              value={customQuery}
              onChange={(e) => setCustomQuery(e.target.value)}
              className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-mono text-sm"
              rows={4}
            />
          </div>

          <div className="flex items-center gap-2">
            <Button onClick={runCustomQuery} disabled={queryStatus === "loading"}>
              {queryStatus === "loading" ? (
                <LoadingSpinner size="sm" text="" />
              ) : (
                <Play size={16} className="mr-2" />
              )}
              Execute Query
            </Button>

            {queryStatus && queryStatus !== "loading" && <StatusPill status={queryStatus} />}
          </div>
        </div>
      </Panel>

      <Panel title="Query Examples">
        <div className="space-y-3">
          {SAMPLE_QUERIES.map((sample, index) => (
            <div
              key={index}
              className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 dark:text-slate-100">{sample.name}</h4>
                  <p className="text-sm text-gray-600 dark:text-slate-400 mt-1">
                    {sample.description}
                  </p>
                  <code className="text-xs bg-gray-100 dark:bg-gray-800 p-2 rounded mt-2 block">
                    {sample.query}
                  </code>
                </div>
                <Button size="sm" variant="secondary" onClick={() => setCustomQuery(sample.query)}>
                  Use
                </Button>
              </div>
            </div>
          ))}
        </div>
      </Panel>

      {queryResult && (
        <Panel title="Query Results">
          <pre className="text-sm bg-gray-50 dark:bg-gray-800 p-4 rounded-lg overflow-auto max-h-96">
            {JSON.stringify(queryResult, null, 2)}
          </pre>
        </Panel>
      )}
    </div>
  );
}
