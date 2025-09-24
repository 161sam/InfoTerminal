import React, { useState } from "react";
import { Scale } from "lucide-react";
import Panel from "@/components/layout/Panel";
import { LoadingSpinner } from "@/components/ui/loading";
import { inputStyles, buttonStyles, textStyles, cardStyles, compose } from "@/styles/design-tokens";

export default function NLPLegalAnalysis() {
  const [query, setQuery] = useState("§23 Arbeitsschutz");
  const [entity, setEntity] = useState("Automotive");
  const [results, setResults] = useState<any[]>([]);
  const [hybrid, setHybrid] = useState(false);
  const [alpha, setAlpha] = useState(0.6);
  const [rerank, setRerank] = useState(true);
  const [domain, setDomain] = useState("");
  const [source, setSource] = useState("");
  const [dateGte, setDateGte] = useState("");
  const [dateLte, setDateLte] = useState("");
  const [context, setContext] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    setLoading(true);
    try {
      if (hybrid) {
        const filters: any = {};
        if (domain.trim())
          filters.domain = domain
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);
        if (source.trim())
          filters.source = source
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);
        if (dateGte) filters.date_gte = dateGte;
        if (dateLte) filters.date_lte = dateLte;
        const r = await fetch("/api/rag/law/hybrid", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ q: query, top_k: 20, k: 50, alpha, filters }),
        });
        const data = await r.json();
        setResults(data.items || []);
      } else {
        const r = await fetch(
          `/api/rag/law/retrieve?q=${encodeURIComponent(query)}&rerank=${rerank ? "1" : "0"}`,
        );
        const data = await r.json();
        setResults(data.items || []);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadContext = async () => {
    setLoading(true);
    try {
      const r = await fetch(`/api/rag/law/context?entity=${encodeURIComponent(entity)}`);
      const data = await r.json();
      setContext(data.laws || []);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Panel title="Legal Document Retrieval">
        <div className="space-y-4">
          <div className="flex gap-2 items-center">
            <input
              className={`flex-1 ${inputStyles.base}`}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Query (e.g., §23 ArbSchG)"
            />
            <button
              className={compose.button("primary", loading ? "opacity-50 cursor-not-allowed" : "")}
              onClick={search}
              disabled={loading}
            >
              {loading ? <LoadingSpinner size="sm" variant="primary" layout="inline" /> : "Search"}
            </button>
          </div>

          <div className="flex items-center gap-4 text-sm">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={rerank}
                onChange={(e) => setRerank(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <span className={textStyles.body}>Rerank results</span>
            </label>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={hybrid}
                onChange={(e) => setHybrid(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <span className={textStyles.body}>Hybrid (BM25 + kNN)</span>
            </label>
            {hybrid && (
              <div className="flex items-center gap-2">
                <span className={textStyles.body}>Alpha:</span>
                <input
                  type="number"
                  min={0}
                  max={1}
                  step={0.1}
                  value={alpha}
                  onChange={(e) => setAlpha(parseFloat(e.target.value || "0.6"))}
                  className={`w-20 ${inputStyles.base}`}
                />
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
            <input
              className={inputStyles.base}
              placeholder="Domain filter"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
            />
            <input
              className={inputStyles.base}
              placeholder="Source filter"
              value={source}
              onChange={(e) => setSource(e.target.value)}
            />
            <input
              type="date"
              className={inputStyles.base}
              value={dateGte}
              onChange={(e) => setDateGte(e.target.value)}
            />
            <input
              type="date"
              className={inputStyles.base}
              value={dateLte}
              onChange={(e) => setDateLte(e.target.value)}
            />
          </div>

          <div className="space-y-3">
            {results.map((item, idx) => (
              <div key={idx} className={`${cardStyles.base} ${cardStyles.padding} space-y-2`}>
                <div className={textStyles.bodySmall}>{item.id}</div>
                <div className={textStyles.h4}>
                  {item.title || item.paragraph || "Legal document"}
                </div>
                <div className={`${textStyles.body} whitespace-pre-wrap`}>{item.text}</div>
              </div>
            ))}
            {!results.length && (
              <div className={`text-center py-8 ${textStyles.body}`}>
                <Scale size={32} className="mx-auto mb-2 opacity-50" />
                <p>No legal documents found. Try adjusting your search query.</p>
              </div>
            )}
          </div>
        </div>
      </Panel>

      <Panel title="Legal Context by Entity">
        <div className="space-y-4">
          <div className="flex gap-2 items-center">
            <input
              className={`flex-1 ${inputStyles.base}`}
              value={entity}
              onChange={(e) => setEntity(e.target.value)}
              placeholder="Entity/Sector (e.g., Automotive)"
            />
            <button
              className={compose.button(
                "secondary",
                loading ? "opacity-50 cursor-not-allowed" : "",
              )}
              onClick={loadContext}
              disabled={loading}
            >
              {loading ? (
                <LoadingSpinner size="sm" variant="secondary" layout="inline" />
              ) : (
                "Load Context"
              )}
            </button>
          </div>

          <div className="space-y-3">
            {context.map((item, idx) => (
              <div key={idx} className={`${cardStyles.base} p-3`}>
                <div className={textStyles.bodySmall}>{item.id}</div>
                <div className={textStyles.h4}>
                  {item.title || item.paragraph || "Legal context"}
                </div>
              </div>
            ))}
            {!context.length && <div className={textStyles.body}>No legal context found</div>}
          </div>
        </div>
      </Panel>
    </div>
  );
}
