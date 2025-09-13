import { useRef, useState, useEffect } from "react";
import { 
  Search, 
  Filter, 
  SortAsc, 
  Calendar, 
  FileText, 
  Users, 
  MapPin, 
  Clock,
  Star,
  ExternalLink,
  Download,
  Eye,
  Loader
} from 'lucide-react';
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import config from "@/lib/config";
import DossierButton from "@/components/DossierButton";
import dynamic from "next/dynamic";
const MapPanel = dynamic(() => import("@/components/MapPanel"), { ssr: false });

interface SearchResult {
  id: string;
  title?: string;
  snippet?: string;
  score?: number;
  date?: string;
  type?: string;
  source?: string;
  entities?: string[];
  url?: string;
}

interface SearchFilters {
  type: string;
  dateRange: string;
  source: string;
  minScore: number;
}

const SEARCH_SUGGESTIONS = [
  { text: "financial networks", category: "Analysis" },
  { text: "ACME Corporation", category: "Organizations" },
  { text: "recent documents", category: "Documents" },
  { text: "entity connections", category: "Graph" },
  { text: "risk indicators", category: "Analysis" },
  { text: "John Smith", category: "People" },
  { text: "London office", category: "Locations" }
];

const SORT_OPTIONS = [
  { value: "relevance", label: "Relevance", icon: Star },
  { value: "date_desc", label: "Newest First", icon: Calendar },
  { value: "date_asc", label: "Oldest First", icon: Calendar },
  { value: "score", label: "Score", icon: SortAsc }
];

const RESULT_TYPES = [
  { value: "all", label: "All Results", count: null },
  { value: "document", label: "Documents", count: null },
  { value: "entity", label: "Entities", count: null },
  { value: "connection", label: "Connections", count: null }
];

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [showMap, setShowMap] = useState(false);
  const [totalResults, setTotalResults] = useState(0);
  const [searchTime, setSearchTime] = useState(0);
  
  const [filters, setFilters] = useState<SearchFilters>({
    type: "all",
    dateRange: "all",
    source: "all",
    minScore: 0
  });
  
  const [sort, setSort] = useState("relevance");
  const controller = useRef<AbortController | null>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Focus search input on mount
  useEffect(() => {
    searchInputRef.current?.focus();
  }, []);

  const runSearch = async (searchQuery?: string) => {
    const searchTerm = searchQuery || query;
    if (!searchTerm.trim()) return;

    const params = new URLSearchParams({ 
      q: searchTerm, 
      sort, 
      limit: "20",
      ...filters 
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
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      runSearch();
    }
  };

  const selectSuggestion = (suggestion: string) => {
    setQuery(suggestion);
    runSearch(suggestion);
  };

  const clearSearch = () => {
    setQuery("");
    setResults([]);
    setError(null);
    setTotalResults(0);
    searchInputRef.current?.focus();
  };

  const exportResults = () => {
    const exportData = {
      query,
      filters,
      sort,
      results,
      totalResults,
      searchTime,
      timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `search-results-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <DashboardLayout title="Intelligent Search" subtitle="Search across all your data sources">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Search Header */}
        <div className="space-y-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-6 w-6 text-gray-400" />
            </div>
            <input
              ref={searchInputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search documents, entities, connections..."
              className="block w-full pl-12 pr-4 py-4 text-lg border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400"
            />
            {query && (
              <button
                onClick={clearSearch}
                className="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            )}
          </div>

          {/* Search Suggestions */}
          {!query && (
            <div className="space-y-2">
              <p className="text-sm text-gray-600 dark:text-slate-400">Popular searches:</p>
              <div className="flex flex-wrap gap-2">
                {SEARCH_SUGGESTIONS.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => selectSuggestion(suggestion.text)}
                    className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-slate-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                  >
                    <span>{suggestion.text}</span>
                    <span className="text-xs text-gray-500 dark:text-slate-400">({suggestion.category})</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            
            {/* Search Controls */}
            <div className="flex items-center justify-between bg-white dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => runSearch()}
                  disabled={!query.trim() || isLoading}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? <Loader size={16} className="animate-spin" /> : <Search size={16} />}
                  Search
                </button>

                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                    showFilters 
                      ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700'
                  }`}
                >
                  <Filter size={16} />
                  Filters
                </button>

                <div className="flex items-center gap-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-slate-300">Sort:</label>
                  <select
                    value={sort}
                    onChange={(e) => setSort(e.target.value)}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  >
                    {SORT_OPTIONS.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {results.length > 0 && (
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => setShowMap(!showMap)}
                    className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                  >
                    {showMap ? 'Hide Map' : 'Show Map'}
                  </button>
                  <button
                    onClick={exportResults}
                    className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                  >
                    <Download size={14} />
                    Export
                  </button>
                </div>
              )}
            </div>

            {/* Filters Panel */}
            {showFilters && (
              <Panel>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">Type</label>
                    <select
                      value={filters.type}
                      onChange={(e) => setFilters(prev => ({ ...prev, type: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      {RESULT_TYPES.map((type) => (
                        <option key={type.value} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">Date Range</label>
                    <select
                      value={filters.dateRange}
                      onChange={(e) => setFilters(prev => ({ ...prev, dateRange: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      <option value="all">All Time</option>
                      <option value="today">Today</option>
                      <option value="week">This Week</option>
                      <option value="month">This Month</option>
                      <option value="year">This Year</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">Source</label>
                    <select
                      value={filters.source}
                      onChange={(e) => setFilters(prev => ({ ...prev, source: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      <option value="all">All Sources</option>
                      <option value="documents">Documents</option>
                      <option value="entities">Entities</option>
                      <option value="graph">Graph</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">Min Score</label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={filters.minScore}
                      onChange={(e) => setFilters(prev => ({ ...prev, minScore: parseFloat(e.target.value) }))}
                      className="w-full"
                    />
                    <div className="text-xs text-gray-500 dark:text-slate-400 mt-1">{filters.minScore}</div>
                  </div>
                </div>
              </Panel>
            )}

            {/* Search Results */}
            {error && (
              <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300">
                <div className="flex items-center gap-2">
                  <Search size={16} />
                  Search Error: {error}
                </div>
              </div>
            )}

            {isLoading && (
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <Loader size={32} className="animate-spin mx-auto mb-4 text-primary-600" />
                  <p className="text-gray-600 dark:text-slate-400">Searching...</p>
                </div>
              </div>
            )}

            {!isLoading && query && results.length === 0 && !error && (
              <div className="text-center py-12">
                <Search size={48} className="mx-auto mb-4 text-gray-400 dark:text-slate-500" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">No results found</h3>
                <p className="text-gray-500 dark:text-slate-400">
                  Try adjusting your search terms or filters
                </p>
              </div>
            )}

            {results.length > 0 && (
              <>
                {/* Results Header */}
                <div className="flex items-center justify-between">
                  <p className="text-sm text-gray-600 dark:text-slate-400">
                    {totalResults.toLocaleString()} results found in {searchTime}ms
                  </p>
                  <DossierButton getPayload={() => ({ 
                    query, 
                    entities: [], 
                    graphSelection: { nodes: [], edges: [] },
                    searchResults: results
                  })} />
                </div>

                {/* Results List */}
                <div className="space-y-4">
                  {results.map((result) => (
                    <SearchResultCard key={result.id} result={result} />
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Result Types */}
            <Panel title="Result Types">
              <div className="space-y-2">
                {RESULT_TYPES.map((type) => (
                  <button
                    key={type.value}
                    onClick={() => setFilters(prev => ({ ...prev, type: type.value }))}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                      filters.type === type.value
                        ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                        : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm">{type.label}</span>
                      {type.count && (
                        <span className="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                          {type.count}
                        </span>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </Panel>

            {/* Search Tips */}
            <Panel title="Search Tips">
              <div className="space-y-2 text-sm text-gray-600 dark:text-slate-400">
                <div>• Use quotes for exact phrases: "ACME Corp"</div>
                <div>• Use AND, OR, NOT for boolean search</div>
                <div>• Wildcard search with * and ?</div>
                <div>• Search specific fields: title:report</div>
                <div>• Date ranges: after:2024-01-01</div>
              </div>
            </Panel>

            {/* Recent Searches */}
            <Panel title="Recent Searches">
              <div className="space-y-2">
                {['financial networks', 'ACME Corporation', 'risk analysis'].map((search, index) => (
                  <button
                    key={index}
                    onClick={() => selectSuggestion(search)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
                  >
                    <div className="flex items-center gap-2">
                      <Clock size={14} />
                      {search}
                    </div>
                  </button>
                ))}
              </div>
            </Panel>
          </div>
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

function SearchResultCard({ result }: { result: SearchResult }) {
  const getResultIcon = (type?: string) => {
    switch (type) {
      case 'document': return FileText;
      case 'entity': return Users;
      case 'location': return MapPin;
      default: return FileText;
    }
  };

  const Icon = getResultIcon(result.type);

  return (
    <Panel className="hover:shadow-md transition-shadow">
      <div className="flex items-start gap-4">
        <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <Icon size={20} className="text-gray-600 dark:text-slate-400" />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 dark:text-slate-100 mb-1">
                {result.title || result.id}
              </h3>
              
              {result.snippet && (
                <p className="text-gray-600 dark:text-slate-400 text-sm mb-2 leading-relaxed">
                  {result.snippet}
                </p>
              )}
              
              <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-slate-400">
                {result.score !== undefined && (
                  <div className="flex items-center gap-1">
                    <Star size={12} />
                    Score: {result.score.toFixed(2)}
                  </div>
                )}
                {result.date && (
                  <div className="flex items-center gap-1">
                    <Calendar size={12} />
                    {new Date(result.date).toLocaleDateString()}
                  </div>
                )}
                {result.source && (
                  <div className="flex items-center gap-1">
                    <FileText size={12} />
                    {result.source}
                  </div>
                )}
              </div>

              {result.entities && result.entities.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {result.entities.slice(0, 3).map((entity, index) => (
                    <span
                      key={index}
                      className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full"
                    >
                      {entity}
                    </span>
                  ))}
                  {result.entities.length > 3 && (
                    <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                      +{result.entities.length - 3} more
                    </span>
                  )}
                </div>
              )}
            </div>
            
            <div className="flex items-center gap-2">
              <button className="p-1 text-gray-400 hover:text-gray-600 rounded">
                <Eye size={16} />
              </button>
              {result.url && (
                <button className="p-1 text-gray-400 hover:text-gray-600 rounded">
                  <ExternalLink size={16} />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </Panel>
  );
}
