// apps/frontend/src/components/search/Search.tsx
import React, { useState, useEffect } from 'react';
import { Search as SearchIcon, Filter, SortDesc, Sparkles, X, Loader2 } from 'lucide-react';
import { useSearch } from '@/hooks/useSearch';
import { useSearchParams } from '@/hooks/useSearchParams';
import EntityBadge from '../entities/EntityBadge';
import { normalizeLabel } from '@/lib/entities';
import SearchResultCard from './SearchResultCard';
import FacetPanel from './FacetPanel';
import FilterChips from './FilterChips';

export default function Search() {
  const { params, set } = useSearchParams();
  const [query, setQuery] = useState((params.q as string) || '');
  const [showFilters, setShowFilters] = useState(false);
  
  const searchParams = {
    q: query,
    page: parseInt((params.page as string) || '1', 10),
    pageSize: parseInt((params.pageSize as string) || '20', 10),
    sort: (params.sort as string) || 'relevance',
    rerank: params.rerank === '1',
    filters: {} as Record<string, string[]>,
    entity: Array.isArray(params.entity) ? params.entity as string[] : params.entity ? [params.entity as string] : undefined,
    value: Array.isArray(params.value) ? params.value as string[] : params.value ? [params.value as string] : undefined
  };

  // Extract filters from params
  Object.entries(params).forEach(([key, value]) => {
    if (key.startsWith('filter.')) {
      const facetName = key.replace('filter.', '');
      const filterValues = Array.isArray(value) ? value as string[] : value ? [value as string] : [];
      searchParams.filters[facetName] = filterValues;
    }
  });

  const { data, loading, error } = useSearch(searchParams);

  // Update URL when query changes with debouncing
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (query !== params.q) {
        set('q', query || undefined);
        set('page', 1);
      }
    }, 300);
    return () => clearTimeout(timeoutId);
  }, [query, params.q, set]);

  const handleSortChange = (sort: string) => {
    set('sort', sort);
    set('page', 1);
  };

  const toggleRerank = () => {
    set('rerank', params.rerank === '1' ? undefined : '1');
    set('page', 1);
  };

  const handleFilterToggle = (facet: string, value: string) => {
    const key = `filter.${facet}`;
    const current = searchParams.filters[facet] || [];
    const updated = current.includes(value) 
      ? current.filter(v => v !== value)
      : [...current, value];
    
    set(key, updated.length ? updated.join(',') : undefined);
    set('page', 1);
  };

  const handlePageChange = (page: number) => {
    set('page', page);
  };

  const clearAllFilters = () => {
    Object.keys(params).forEach(key => {
      if (key.startsWith('filter.') || key === 'entity' || key === 'value') {
        set(key, undefined);
      }
    });
    set('page', 1);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Search Header */}
      <div className="mb-8">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <SearchIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search documents, entities, connections..."
            className="block w-full pl-10 pr-12 py-4 text-lg rounded-xl shadow-sm transition-all
             border border-gray-300 dark:border-gray-600
             bg-white dark:bg-gray-800
             text-gray-900 dark:text-gray-100
             placeholder:text-gray-400 dark:placeholder:text-gray-400
             focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            data-search-input
          />
          {loading && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              <Loader2 className="h-5 w-5 text-gray-400 animate-spin" />
            </div>
          )}
        </div>

        {/* Search Controls */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors ${
                showFilters 
                  ? 'bg-primary-50 border-primary-200 text-primary-700' 
                  : 'bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600\n    text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              <Filter size={16} />
              Filters
              {data?.aggregations && Object.keys(data.aggregations).length > 0 && (
                <span className="bg-primary-100 text-primary-800 text-xs font-medium px-2 py-0.5 rounded-full">
                  {Object.values(data.aggregations).reduce((sum, buckets) => sum + buckets.length, 0)}
                </span>
              )}
            </button>

            <button
              onClick={toggleRerank}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors ${
                searchParams.rerank
                  ? 'bg-purple-50 border-purple-200 text-purple-700'
                  : 'bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600\n    text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              <Sparkles size={16} />
              AI Rerank
            </button>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500">Sort by:</span>
            <select
              value={searchParams.sort}
              onChange={(e) => handleSortChange(e.target.value)}
              className="px-3 py-2 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500
            border border-gray-300 dark:border-gray-600
            bg-white dark:bg-gray-800
            text-gray-900 dark:text-gray-100"
            >
              <option value="relevance">Relevance</option>
              <option value="date_desc">Newest First</option>
              <option value="date_asc">Oldest First</option>
            </select>
          </div>
        </div>

        {/* Filter Chips */}
        <FilterChips
          filters={searchParams.filters}
          entity={searchParams.entity}
          value={searchParams.value}
          onRemove={(facet, value) => {
            const key = `filter.${facet}`;
            const current = searchParams.filters[facet] || [];
            const updated = current.filter(v => v !== value);
            set(key, updated.length ? updated.join(',') : undefined);
          }}
          onRemoveEntity={(entity) => {
            const current = searchParams.entity || [];
            const updated = current.filter(e => e !== entity);
            set('entity', updated.length ? updated : undefined);
          }}
          onRemoveValue={(value) => {
            const current = searchParams.value || [];
            const updated = current.filter(v => v !== value);
            set('value', updated.length ? updated : undefined);
          }}
          onClearAll={clearAllFilters}
        />
      </div>

      {/* Results Summary */}
      {data && (
        <div className="mb-6 flex items-center justify-between">
          <p className="text-sm text-gray-600">
            {data.total > 0 ? (
              <>
                Found <span className="font-medium text-gray-900">{data.total.toLocaleString()}</span> results
                {typeof data.tookMs === 'number' && (
                  <> in <span className="font-medium text-gray-900">{data.tookMs}</span> ms</>
                )}
                {query && <> for "<span className="font-medium text-gray-900">{query}</span>"</>}
              </>
            ) : (
              <>No results found{query && <> for "{query}"</>}</>
            )}
          </p>
          {loading && (
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Loader2 size={14} className="animate-spin" />
              Searching...
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-xl p-4">
          <p className="text-red-800">Error loading results: {error.message}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Filters Sidebar */}
        {showFilters && data?.aggregations && (
          <div className="lg:col-span-1">
            <FacetPanel
              aggregations={data.aggregations}
              selectedFilters={searchParams.filters}
              onToggle={handleFilterToggle}
            />
          </div>
        )}

        {/* Results */}
        <div className={showFilters && data?.aggregations ? 'lg:col-span-3' : 'lg:col-span-4'}>
          {data?.items && data.items.length > 0 ? (
            <>
              <div className="space-y-4">
                {data.items.map((item) => (
                  <SearchResultCard key={item.id} item={item} />
                ))}
              </div>
              
              {/* Pagination */}
              {data.total > searchParams.pageSize && (
                <div className="mt-8 flex items-center justify-center">
                  <SearchPagination
                    page={searchParams.page}
                    pageSize={searchParams.pageSize}
                    total={data.total}
                    onPageChange={handlePageChange}
                  />
                </div>
              )}
            </>
          ) : !loading && query && (
            <div className="text-center py-12">
              <SearchIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-4 text-lg font-medium text-gray-900">No results found</h3>
              <p className="mt-2 text-gray-500">Try adjusting your search terms or filters.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

interface SearchPaginationProps {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

function SearchPagination({ page, pageSize, total, onPageChange }: SearchPaginationProps) {
  const totalPages = Math.ceil(total / pageSize);
  const startItem = (page - 1) * pageSize + 1;
  const endItem = Math.min(page * pageSize, total);

  return (
    <div className="flex items-center justify-between px-4 py-3 sm:px-6 rounded-lg
                 bg-white dark:bg-gray-900
                 border border-gray-200 dark:border-gray-800">
      <div className="flex flex-1 justify-between sm:hidden">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page === 1}
          className="relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md
            text-gray-700 dark:text-gray-200
            bg-white dark:bg-gray-800
            border border-gray-300 dark:border-gray-600
            hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page === totalPages}
          className="relative ml-3 inline-flex items-center px-4 py-2 text-sm font-medium rounded-md
            text-gray-700 dark:text-gray-200
            bg-white dark:bg-gray-800
            border border-gray-300 dark:border-gray-600
            hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
      
      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-gray-700">
            Showing <span className="font-medium">{startItem}</span> to{' '}
            <span className="font-medium">{endItem}</span> of{' '}
            <span className="font-medium">{total}</span> results
          </p>
        </div>
        
        <div>
          <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm">
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page === 1}
              className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            {/* Page numbers */}
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              const pageNum = Math.max(1, page - 2) + i;
              if (pageNum > totalPages) return null;
              
              return (
                <button
                  key={pageNum}
                  onClick={() => onPageChange(pageNum)}
                  className={`relative inline-flex items-center px-4 py-2 text-sm font-semibold ${
                    pageNum === page
                      ? 'z-10 bg-primary-600 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600'
                      : 'text-gray-900 dark:text-gray-100 ring-1 ring-inset ring-gray-300 dark:ring-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 focus:z-20 focus:outline-offset-0'
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
            
            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page === totalPages}
              className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </nav>
        </div>
      </div>
    </div>
  );
}
