// Entity search and filter controls panel
import { Search, Plus, Download } from "lucide-react";
import Panel from "@/components/layout/Panel";
import { EntityFilter, SortConfig, RISK_LEVELS } from "@/lib/entities/entity-config";

interface EntitySearchPanelProps {
  filters: EntityFilter;
  onFiltersChange: (filters: EntityFilter) => void;
  sortConfig: SortConfig;
  onSort: (key: string) => void;
  onClearFilters: () => void;
  onExport: () => void;
  onCreateEntity: () => void;
  resultsCount: number;
  totalCount: number;
}

export function EntitySearchPanel({
  filters,
  onFiltersChange,
  sortConfig,
  onSort,
  onClearFilters,
  onExport,
  onCreateEntity,
  resultsCount,
  totalCount,
}: EntitySearchPanelProps) {
  const hasActiveFilters =
    filters.searchTerm ||
    filters.type !== "all" ||
    filters.verified !== "all" ||
    filters.riskLevel !== "all" ||
    filters.minMentions > 0;

  const updateFilter = (key: keyof EntityFilter, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value,
    });
  };

  return (
    <Panel>
      <div className="space-y-4">
        {/* Header with title and action buttons */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            Entity Explorer
          </h3>
          <div className="flex items-center gap-2">
            <button
              onClick={onCreateEntity}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              <Plus size={14} />
              Add Entity
            </button>
            <button
              onClick={onExport}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <Download size={14} />
              Export
            </button>
          </div>
        </div>

        {/* Search bar */}
        <div className="flex items-center gap-4">
          <div className="flex-1 relative">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={16}
            />
            <input
              type="text"
              placeholder="Search entities, descriptions, aliases..."
              value={filters.searchTerm}
              onChange={(e) => updateFilter("searchTerm", e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            />
          </div>

          <button
            onClick={onClearFilters}
            className="px-3 py-2 text-sm text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200"
          >
            Clear Filters
          </button>
        </div>

        {/* Filter controls */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {/* Entity type filter */}
          <div>
            <select
              value={filters.type}
              onChange={(e) => updateFilter("type", e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="all">All Types</option>
              <option value="Person">Person</option>
              <option value="Organization">Organization</option>
              <option value="Location">Location</option>
              <option value="Email">Email</option>
              <option value="Domain">Domain</option>
            </select>
          </div>

          {/* Verification status filter */}
          <div>
            <select
              value={filters.verified}
              onChange={(e) => updateFilter("verified", e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="all">All Status</option>
              <option value="verified">Verified</option>
              <option value="pending">Pending</option>
            </select>
          </div>

          {/* Risk level filter */}
          <div>
            <select
              value={filters.riskLevel}
              onChange={(e) => updateFilter("riskLevel", e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              {RISK_LEVELS.map((level) => (
                <option key={level.value} value={level.value}>
                  {level.label}
                </option>
              ))}
            </select>
          </div>

          {/* Minimum mentions filter */}
          <div>
            <input
              type="number"
              min="0"
              placeholder="Min mentions"
              value={filters.minMentions || ""}
              onChange={(e) => updateFilter("minMentions", parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            />
          </div>

          {/* Sort control */}
          <div>
            <select
              value={sortConfig.key}
              onChange={(e) => onSort(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="mentions">Sort by Mentions</option>
              <option value="confidence">Sort by Confidence</option>
              <option value="name">Sort by Name</option>
              <option value="lastSeen">Sort by Last Seen</option>
              <option value="riskScore">Sort by Risk Score</option>
            </select>
          </div>
        </div>

        {/* Results summary */}
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-slate-400">
          <span>
            Showing {resultsCount} of {totalCount} entities
          </span>
          {hasActiveFilters && (
            <span className="text-blue-600 dark:text-blue-400">Filters applied</span>
          )}
        </div>
      </div>
    </Panel>
  );
}

export default EntitySearchPanel;
