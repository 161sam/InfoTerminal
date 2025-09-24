import { useCallback, useEffect, useRef, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import config from "@/lib/config";
import dynamic from "next/dynamic";
import { useRouter } from "next/router";

// Import modularized components
import SearchHeader from "@/components/search/panels/SearchHeader";
import SearchControls from "@/components/search/panels/SearchControls";
import SearchFilters from "@/components/search/panels/SearchFilters";
import SearchResults from "@/components/search/panels/SearchResults";
import SearchSidebar from "@/components/search/panels/SearchSidebar";

// Import types and utilities
import {
  SearchResult,
  SearchFilters as SearchFiltersType,
  createSearchExportData,
} from "@/lib/search/search-config";

const MapPanel = dynamic(() => import("@/components/MapPanel"), { ssr: false });

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [showMap, setShowMap] = useState(false);
  const [totalResults, setTotalResults] = useState(0);
  const [searchTime, setSearchTime] = useState(0);

  const [filters, setFilters] = useState<SearchFiltersType>({
    type: "all",
    dateRange: "all",
    source: "all",
    minScore: 0,
  });

  const [sort, setSort] = useState("relevance");
  const controller = useRef<AbortController | null>(null);

  const performSearch = useCallback(
    async (searchTerm: string) => {
      if (!searchTerm.trim()) return;

      const filterParams: Record<string, string> = {
        type: filters.type,
        dateRange: filters.dateRange,
        source: filters.source,
        minScore: String(filters.minScore),
      };

      const params = new URLSearchParams({
        q: searchTerm,
        sort,
        limit: "20",
        ...filterParams,
      });

      setIsLoading(true);
      setError(null);

      // Cancel previous request
      controller.current?.abort();
      const c = new AbortController();
      controller.current = c;

      const startTime = performance.now();

      try {
        let response = await fetch(`/api/search?${params.toString()}`, { signal: c.signal });

        if (response.status === 404) {
          const base = config?.SEARCH_API;
          if (!base) throw new Error("Search API not configured");
          response = await fetch(`${base}/search?${params.toString()}`, { signal: c.signal });
        }

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        const searchResults = data.items || data.results || [];

        setResults(searchResults);
        setTotalResults(data.total || searchResults.length);
        setSearchTime(Math.round(performance.now() - startTime));
      } catch (e: any) {
        if (e.name !== "AbortError") {
          setError(e.message || "Search failed");
        }
      } finally {
        setIsLoading(false);
      }
    },
    [filters.dateRange, filters.minScore, filters.source, filters.type, sort],
  );

  const runSearch = useCallback(
    async (searchQuery?: string) => {
      const searchTerm = searchQuery || query;
      if (!searchTerm.trim()) return;
      await performSearch(searchTerm);
    },
    [performSearch, query],
  );

  const clearSearch = () => {
    setQuery("");
    setResults([]);
    setError(null);
    setTotalResults(0);
  };

  const exportResults = () => {
    const exportData = createSearchExportData(
      query,
      filters,
      sort,
      results,
      totalResults,
      searchTime,
    );
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `search-results-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const selectSuggestion = (suggestion: string) => {
    setQuery(suggestion);
    runSearch(suggestion);
  };

  const router = useRouter();

  useEffect(() => {
    const initialQuery = router.query?.q;
    if (typeof initialQuery === "string" && initialQuery.trim()) {
      setQuery(initialQuery);
      performSearch(initialQuery);
    }
  }, [router.query?.q, performSearch]);

  return (
    <DashboardLayout title="Intelligent Search" subtitle="Search across all your data sources">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Search Header */}
        <SearchHeader
          query={query}
          setQuery={setQuery}
          onSearch={runSearch}
          onClear={clearSearch}
        />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* Search Controls */}
            <SearchControls
              query={query}
              isLoading={isLoading}
              showFilters={showFilters}
              setShowFilters={setShowFilters}
              sort={sort}
              setSort={setSort}
              onSearch={runSearch}
              results={results}
              showMap={showMap}
              setShowMap={setShowMap}
              onExport={exportResults}
            />

            {/* Filters Panel */}
            <SearchFilters filters={filters} setFilters={setFilters} show={showFilters} />

            {/* Search Results */}
            <SearchResults
              query={query}
              results={results}
              totalResults={totalResults}
              searchTime={searchTime}
              isLoading={isLoading}
              error={error}
              onRetry={runSearch}
            />
          </div>

          {/* Sidebar */}
          <SearchSidebar
            filters={filters}
            setFilters={setFilters}
            onSearchSuggestion={selectSuggestion}
          />
        </div>

        {/* Map Panel */}
        {showMap && (
          <Panel title="Geographic View">
            <MapPanel />
          </Panel>
        )}
      </div>
    </DashboardLayout>
  );
}
