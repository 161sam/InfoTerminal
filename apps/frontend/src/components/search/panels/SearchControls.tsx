import { Search, Filter, Download } from "lucide-react";
import { LoadingSpinner } from "@/components/ui/loading";
import { SORT_OPTIONS, SearchResult, SearchFilters } from "@/lib/search/search-config";

interface SearchControlsProps {
  query: string;
  isLoading: boolean;
  showFilters: boolean;
  setShowFilters: (show: boolean) => void;
  sort: string;
  setSort: (sort: string) => void;
  onSearch: () => void;
  results: SearchResult[];
  showMap: boolean;
  setShowMap: (show: boolean) => void;
  onExport: () => void;
}

export default function SearchControls({
  query,
  isLoading,
  showFilters,
  setShowFilters,
  sort,
  setSort,
  onSearch,
  results,
  showMap,
  setShowMap,
  onExport,
}: SearchControlsProps) {
  return (
    <div className="flex items-center justify-between bg-white dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-4">
        <button
          onClick={onSearch}
          disabled={!query.trim() || isLoading}
          className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <LoadingSpinner size="sm" variant="primary" layout="inline" />
          ) : (
            <Search size={16} />
          )}
          Search
        </button>

        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
            showFilters
              ? "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
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
            {showMap ? "Hide Map" : "Show Map"}
          </button>
          <button
            onClick={onExport}
            className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
          >
            <Download size={14} />
            Export
          </button>
        </div>
      )}
    </div>
  );
}
