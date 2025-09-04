import { useRef, useState } from "react";
import Layout from "../components/Layout";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Field from "../components/ui/Field";
import StatusPill from "../components/ui/StatusPill";
import config from "../lib/config";

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
    <Layout>
      <h1 className="mb-4">Search</h1>
      <div className="mb-4 flex items-end gap-2">
        <Field
          label="Query"
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
      <div className="mb-4 flex gap-2">
        {chips.map((c) => (
          <button
            key={c}
            className="rounded-full bg-gray-200 px-3 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500"
            onClick={() => setQ(c)}
          >
            {c}
          </button>
        ))}
      </div>
      {error && <StatusPill status="fail">{error}</StatusPill>}
      <div className="space-y-4">
        {isLoading && <div>Loading...</div>}
        {!isLoading &&
          results.map((r) => (
            <Card key={r.id}>
              <h3 className="font-semibold">{r.title || r.id}</h3>
              {r.snippet && <p className="text-sm text-gray-600">{r.snippet}</p>}
              {r.score !== undefined && (
                <p className="text-xs text-gray-500">Score: {r.score}</p>
              )}
              {r.date && <p className="text-xs text-gray-500">{r.date}</p>}
            </Card>
          ))}
      </div>
    </Layout>
  );
}
