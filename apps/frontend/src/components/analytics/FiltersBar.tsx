// Global filters bar for analytics dashboard
import React from 'react';
import { Calendar, Filter, Tag, RefreshCw } from 'lucide-react';
import { AnalyticsFilters, TIME_RANGES, ENTITY_TYPES, SOURCE_TYPES, WORKFLOW_TYPES } from './types';

interface FiltersBarProps {
  filters: AnalyticsFilters;
  onFiltersChange: (filters: Partial<AnalyticsFilters>) => void;
  onRefresh?: () => void;
  className?: string;
}

export function FiltersBar({ filters, onFiltersChange, onRefresh, className = '' }: FiltersBarProps) {
  const handleTimeRangeChange = (timeRange: string) => {
    const range = TIME_RANGES.find(r => r.value === timeRange);
    let dateRange = undefined;

    if (timeRange !== 'custom' && range?.days) {
      const to = new Date();
      const from = new Date(to);
      from.setDate(from.getDate() - range.days);
      
      dateRange = {
        from: from.toISOString().split('T')[0],
        to: to.toISOString().split('T')[0],
      };
    }

    onFiltersChange({ timeRange, dateRange });
  };

  const handleEntityTypesChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedTypes = Array.from(e.target.selectedOptions, option => option.value);
    onFiltersChange({ entityTypes: selectedTypes });
  };

  const handleSourcesChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedSources = Array.from(e.target.selectedOptions, option => option.value);
    onFiltersChange({ sources: selectedSources });
  };

  const handleWorkflowsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedWorkflows = Array.from(e.target.selectedOptions, option => option.value);
    onFiltersChange({ workflows: selectedWorkflows });
  };

  const handleTagsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const tags = e.target.value.split(',').map(tag => tag.trim()).filter(Boolean);
    onFiltersChange({ tags });
  };

  const handleCustomDateChange = (field: 'from' | 'to', value: string) => {
    const dateRange = { ...filters.dateRange, [field]: value };
    onFiltersChange({ dateRange });
  };

  const clearFilters = () => {
    onFiltersChange({
      timeRange: '30d',
      entityTypes: [],
      sources: [],
      tags: [],
      collections: [],
      workflows: [],
      dateRange: undefined,
    });
  };

  return (
    <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-gray-600 dark:text-gray-400" />
          <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">Analytics Filters</h3>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={clearFilters}
            className="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            Clear All
          </button>
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="inline-flex items-center gap-1 px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
            >
              <RefreshCw size={14} />
              Refresh
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4">
        {/* Time Range */}
        <div>
          <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
            <Calendar size={14} className="inline mr-1" />
            Time Range
          </label>
          <select
            value={filters.timeRange}
            onChange={(e) => handleTimeRangeChange(e.target.value)}
            className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            {TIME_RANGES.map(range => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
        </div>

        {/* Custom Date Range */}
        {filters.timeRange === 'custom' && (
          <>
            <div>
              <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">From</label>
              <input
                type="date"
                value={filters.dateRange?.from || ''}
                onChange={(e) => handleCustomDateChange('from', e.target.value)}
                className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">To</label>
              <input
                type="date"
                value={filters.dateRange?.to || ''}
                onChange={(e) => handleCustomDateChange('to', e.target.value)}
                className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            </div>
          </>
        )}

        {/* Entity Types */}
        <div>
          <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Entity Types</label>
          <select
            multiple
            value={filters.entityTypes}
            onChange={handleEntityTypesChange}
            className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            style={{ height: '70px' }}
          >
            {ENTITY_TYPES.map(type => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* Source Types */}
        <div>
          <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Sources</label>
          <select
            multiple
            value={filters.sources}
            onChange={handleSourcesChange}
            className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            style={{ height: '70px' }}
          >
            {SOURCE_TYPES.map(type => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* Workflows */}
        <div>
          <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Workflows</label>
          <select
            multiple
            value={filters.workflows}
            onChange={handleWorkflowsChange}
            className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            style={{ height: '70px' }}
          >
            {WORKFLOW_TYPES.map(type => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* Tags */}
        <div>
          <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
            <Tag size={14} className="inline mr-1" />
            Tags
          </label>
          <input
            type="text"
            value={filters.tags.join(', ')}
            onChange={handleTagsChange}
            placeholder="tag1, tag2, ..."
            className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          />
        </div>
      </div>

      {/* Active Filters Summary */}
      {(filters.entityTypes.length > 0 || filters.sources.length > 0 || filters.tags.length > 0 || filters.workflows.length > 0) && (
        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-wrap gap-1">
            {filters.entityTypes.map(type => (
              <span key={type} className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 rounded">
                Entity: {type}
                <button
                  onClick={() => onFiltersChange({ entityTypes: filters.entityTypes.filter(t => t !== type) })}
                  className="ml-1 hover:text-blue-900 dark:hover:text-blue-200"
                >
                  ×
                </button>
              </span>
            ))}
            {filters.sources.map(source => (
              <span key={source} className="inline-flex items-center px-2 py-1 text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300 rounded">
                Source: {source}
                <button
                  onClick={() => onFiltersChange({ sources: filters.sources.filter(s => s !== source) })}
                  className="ml-1 hover:text-green-900 dark:hover:text-green-200"
                >
                  ×
                </button>
              </span>
            ))}
            {filters.tags.map(tag => (
              <span key={tag} className="inline-flex items-center px-2 py-1 text-xs bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300 rounded">
                Tag: {tag}
                <button
                  onClick={() => onFiltersChange({ tags: filters.tags.filter(t => t !== tag) })}
                  className="ml-1 hover:text-purple-900 dark:hover:text-purple-200"
                >
                  ×
                </button>
              </span>
            ))}
            {filters.workflows.map(workflow => (
              <span key={workflow} className="inline-flex items-center px-2 py-1 text-xs bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300 rounded">
                Workflow: {workflow}
                <button
                  onClick={() => onFiltersChange({ workflows: filters.workflows.filter(w => w !== workflow) })}
                  className="ml-1 hover:text-orange-900 dark:hover:text-orange-200"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default FiltersBar;
