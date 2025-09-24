import React from "react";
import { Search, Plus, Download } from "lucide-react";
import Panel from "@/components/layout/Panel";
import { EntityFilter, SortConfig, RISK_LEVELS } from "./types";

interface EntitySearchAndFiltersProps {
  filters: EntityFilter;
  onFiltersChange: (filters: EntityFilter) => void;
  sortConfig: SortConfig;
  onSort: (key: string) => void;
  onClearFilters: () => void;
  onCreateEntity: () => void;
  onExportEntities: () => void;
  totalEntities: number;
  filteredCount: number;
}

export default function EntitySearchAndFilters({
  filters,
  onFiltersChange,
  sortConfig,
  onSort,
  onClearFilters,
  onCreateEntity,
  onExportEntities,
  totalEntities,
  filteredCount,
}: EntitySearchAndFiltersProps) {
  const hasActiveFilters =
    filters.searchTerm ||
    filters.type !== "all" ||
    filters.verified !== "all" ||
    filters.riskLevel !== "all" ||
    filters.minMentions > 0;

  return (
    <Panel>
      <div className="space-y-4">
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
              onClick={onExportEntities}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <Download size={14} />
              Export
            </button>
          </div>
        </div>

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
              onChange={(e) => onFiltersChange({ ...filters, searchTerm: e.target.value })}
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

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          <div>
            <select
              value={filters.type}
              onChange={(e) => onFiltersChange({ ...filters, type: e.target.value })}
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

          <div>
            <select
              value={filters.verified}
              onChange={(e) => onFiltersChange({ ...filters, verified: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="all">All Status</option>
              <option value="verified">Verified</option>
              <option value="pending">Pending</option>
            </select>
          </div>

          <div>
            <select
              value={filters.riskLevel}
              onChange={(e) => onFiltersChange({ ...filters, riskLevel: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              {RISK_LEVELS.map((level) => (
                <option key={level.value} value={level.value}>
                  {level.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <input
              type="number"
              min="0"
              placeholder="Min mentions"
              value={filters.minMentions || ""}
              onChange={(e) =>
                onFiltersChange({ ...filters, minMentions: parseInt(e.target.value) || 0 })
              }
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            />
          </div>

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

        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-slate-400">
          <span>
            Showing {filteredCount} of {totalEntities} entities
          </span>
          {hasActiveFilters && (
            <span className="text-blue-600 dark:text-blue-400">Filters applied</span>
          )}
        </div>
      </div>
    </Panel>
  );
}
