import Panel from "@/components/layout/Panel";
import { SearchFilters as SearchFiltersType, RESULT_TYPES } from "@/lib/search/search-config";

interface SearchFiltersProps {
  filters: SearchFiltersType;
  setFilters: (
    filters: SearchFiltersType | ((prev: SearchFiltersType) => SearchFiltersType),
  ) => void;
  show: boolean;
}

export default function SearchFilters({ filters, setFilters, show }: SearchFiltersProps) {
  if (!show) return null;

  return (
    <Panel>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
            Type
          </label>
          <select
            value={filters.type}
            onChange={(e) => setFilters((prev) => ({ ...prev, type: e.target.value }))}
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
          <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
            Date Range
          </label>
          <select
            value={filters.dateRange}
            onChange={(e) => setFilters((prev) => ({ ...prev, dateRange: e.target.value }))}
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
          <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
            Source
          </label>
          <select
            value={filters.source}
            onChange={(e) => setFilters((prev) => ({ ...prev, source: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="all">All Sources</option>
            <option value="documents">Documents</option>
            <option value="entities">Entities</option>
            <option value="graph">Graph</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
            Min Score
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={filters.minScore}
            onChange={(e) =>
              setFilters((prev) => ({ ...prev, minScore: parseFloat(e.target.value) }))
            }
            className="w-full"
          />
          <div className="text-xs text-gray-500 dark:text-slate-400 mt-1">{filters.minScore}</div>
        </div>
      </div>
    </Panel>
  );
}
