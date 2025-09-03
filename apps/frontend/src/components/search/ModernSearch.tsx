// apps/frontend/src/components/search/ModernSearch.tsx
import React, { useState, useEffect } from 'react';
import { Search, Filter, SortDesc, Sparkles, X, Loader2 } from 'lucide-react';
import { useSearch } from '../../hooks/useSearch';
import { useSearchParams } from '../../hooks/useSearchParams';
import EntityBadge from '../entities/EntityBadge';
import { normalizeLabel } from '../../lib/entities';

export default function ModernSearch() {
  const { params, set } = useSearchParams();
  const [query, setQuery] = useState((params.q as string) || '');
  const [showFilters, setShowFilters] = useState(false);
  
  const searchParams = {
    q: query,
    page: 1,
    pageSize: 20,
    sort: (params.sort as string) || 'relevance',
    rerank: params.rerank === '1'
  };

  const { data, loading, error } = useSearch(searchParams);

  // Update URL when query changes
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (query) {
        set('q', query);
      }
    }, 300);
    return () => clearTimeout(timeoutId);
  }, [query, set]);

  const handleSortChange = (sort: string) => {
    set('sort', sort);
  };

  const toggleRerank = () => {
    set('rerank', params.rerank === '1' ? undefined : '1');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Search Header */}
      <div className="mb-8">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search documents, entities, connections..."
            className="block w-full pl-10 pr-12 py-4 text-lg border border-gray-300 rounded-xl bg-white shadow-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
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
                  : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Filter size={16} />
              Filters
              {data?.aggregations && Object.keys(data.aggregations).length > 0 && (
                <span className="bg-primary-100 text-primary-800 text-xs font-medium px-2 py-0.5 rounded-full">
                  {Object.values(data.aggregations).flat().length}
                </span>
              )}
            </button>

            <button
              onClick={toggleRerank}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors ${
                params.rerank === '1'
                  ? 'bg-purple-50 border-purple-200 text-purple-700'
                  : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
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
              className="px-3 py-2 border border-gray-300 rounded-lg bg-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="relevance">Relevance</option>
              <option value="date_desc">Newest First</option>
              <option value="date_asc">Oldest First</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Summary */}
      {data && (
        <div className="mb-6 flex items-center justify-between">
          <p className="text-sm text-gray-600">
            {data.total > 0 ? (
              <>
                Found <span className="font-medium text-gray-900">{data.total.toLocaleString()}</span> results
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

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Filters Sidebar */}
        {showFilters && data?.aggregations && (
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
                <button 
                  onClick={() => setShowFilters(false)}
                  className="lg:hidden p-1 text-gray-400 hover:text-gray-600"
                >
                  <X size={16} />
                </button>
              </div>
              
              {Object.entries(data.aggregations).map(([facetName, buckets]) => (
                <div key={facetName} className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-3 capitalize">
                    {facetName.replace('_', ' ')}
                  </h4>
                  <div className="space-y-2">
                    {buckets.slice(0, 5).map((bucket) => (
                      <label key={bucket.key} className="flex items-center">
                        <input 
                          type="checkbox" 
                          className="h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                        />
                        <span className="ml-3 text-sm text-gray-600 flex-1">{bucket.key}</span>
                        <span className="text-xs text-gray-400">({bucket.doc_count})</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Results */}
        <div className={showFilters && data?.aggregations ? 'lg:col-span-3' : 'lg:col-span-4'}>
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
              <p className="text-red-800">Error loading results: {error.message}</p>
            </div>
          )}

          {data?.items && data.items.length > 0 ? (
            <div className="space-y-4">
              {data.items.map((item) => (
                <SearchResultCard key={item.id} item={item} />
              ))}
            </div>
          ) : !loading && query && (
            <div className="text-center py-12">
              <Search className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-4 text-lg font-medium text-gray-900">No results found</h3>
              <p className="mt-2 text-gray-500">Try adjusting your search terms or filters.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function SearchResultCard({ item }: { item: any }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {item.title || item.id}
          </h3>
          
          {item.snippet && (
            <p className="text-gray-600 mb-3 line-clamp-2">{item.snippet}</p>
          )}
          
          {/* Entity Badges */}
          {item.entity_types && (
            <div className="flex flex-wrap gap-2 mb-3">
              {item.entity_types.map((type: string) => (
                <EntityBadge 
                  key={type} 
                  label={normalizeLabel(type)} 
                  size="sm"
                />
              ))}
            </div>
          )}
          
          <div className="flex items-center gap-4 text-sm text-gray-500">
            {item.source && (
              <span className="inline-flex items-center gap-1">
                Source: <span className="font-medium">{item.source}</span>
              </span>
            )}
            {item.score && (
              <span>Relevance: {(item.score * 100).toFixed(1)}%</span>
            )}
          </div>
        </div>
        
        <div className="ml-4 flex-shrink-0">
          {item.node_id && (
            <a
              href={`/graphx?focus=${item.node_id}`}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-primary-700 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
            >
              <Network size={16} />
              Graph
            </a>
          )}
        </div>
      </div>
    </div>
  );
}