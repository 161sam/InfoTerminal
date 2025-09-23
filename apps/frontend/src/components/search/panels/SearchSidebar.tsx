import { Clock } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import { SearchFilters, RESULT_TYPES, RECENT_SEARCHES } from '@/lib/search/search-config';

interface SearchSidebarProps {
  filters: SearchFilters;
  setFilters: (filters: SearchFilters | ((prev: SearchFilters) => SearchFilters)) => void;
  onSearchSuggestion: (suggestion: string) => void;
}

export default function SearchSidebar({ 
  filters, 
  setFilters, 
  onSearchSuggestion 
}: SearchSidebarProps) {
  return (
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
          {RECENT_SEARCHES.map((search, index) => (
            <button
              key={index}
              onClick={() => onSearchSuggestion(search)}
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
  );
}
