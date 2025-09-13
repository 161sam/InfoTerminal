import { useRef, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/Button";
import Field from "@/components/ui/Field";
import StatusPill from "@/components/ui/StatusPill";
import config from "@/lib/config";
import DossierButton from "@/components/DossierButton";
import dynamic from "next/dynamic";
const MapPanel = dynamic(() => import("@/components/MapPanel"), { ssr: false });

type SearchResult = {
  id: string;
  title?: string;
  snippet?: string;
  score?: number;
  date?: string;
};

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [sort, setSort] = useState("relevance");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const controller = useRef<AbortController | null>(null);
  const [showMap, setShowMap] = useState(false);

  const runSearch = async () => {
    const params = new URLSearchParams({ q, sort, limit: "20" });
    setIsLoading(true);
    setError(null);
    controller.current?.abort();
    const c = new AbortController();
    controller.current = c;
    try {
      let r = await fetch(`/api/search?${params.toString()}`, { signal: c.signal });
      if (r.status === 404) {
        const base = config?.SEARCH_API;
        if (!base) throw new Error("Search API not configured");
        r = await fetch(`${base}/search?${params.toString()}`, { signal: c.signal });
      }
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      setResults(j.items || j.results || []);
    } catch (e: any) {
      if (e.name !== "AbortError") setError(e.message || "search failed");
    } finally {
      setIsLoading(false);
    }
  };

  const chips = ["demo", "graph", "open source"];

  return (
    <DashboardLayout title="Search">
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold mb-6">Search</h1>
        <Panel>
          <div className="mb-4 flex items-end gap-2">
          <Field
            label="Query"
            name="searchQuery"
            id="search-query"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="flex-1"
          />
          <div>
            <label className="mb-1 block text-sm font-medium">Sort</label>
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="rounded-md border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:ring-primary-500"
            >
              <option value="relevance">relevance</option>
              <option value="date_desc">date_desc</option>
              <option value="date_asc">date_asc</option>
            </select>
          </div>
          <Button onClick={runSearch} isLoading={isLoading} disabled={!q}>
            Search
          </Button>
          </div>
          <div className="mb-2 flex gap-2">
        {chips.map((c) => (
          <button
            key={c}
            className="rounded-full bg-gray-200 px-3 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500"
            onClick={() => setQ(c)}
          >
            {c}
          </button>
        ))}
          {error && <StatusPill status="fail">{error}</StatusPill>}
          </div>
        </Panel>
        {/* Export current search as dossier */}
        <DossierButton getPayload={() => ({ query: q, entities: [], graphSelection: { nodes: [], edges: [] } })} />
        <Button variant="secondary" onClick={() => setShowMap((v) => !v)}>
          {showMap ? "Hide Map" : "Show Map"}
        </Button>
        <div className="space-y-4">
          {isLoading && <div>Loading...</div>}
          {!isLoading &&
            results.map((r) => (
              <Panel key={r.id}>
                <h3 className="font-semibold">{r.title || r.id}</h3>
                {r.snippet && <p className="text-sm text-gray-600 dark:text-slate-300">{r.snippet}</p>}
                {r.score !== undefined && (
                  <p className="text-xs text-gray-500">Score: {r.score}</p>
                )}
                {r.date && <p className="text-xs text-gray-500">{r.date}</p>}
              </Panel>
            ))}
        </div>
        {showMap && <MapPanel />}
      </div>
    </DashboardLayout>
  );
}
