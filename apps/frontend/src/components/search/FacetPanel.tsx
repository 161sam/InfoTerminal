// apps/frontend/src/components/search/FacetPanel.tsx
import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Search, X } from 'lucide-react';
import type { Aggregations } from '@/types/search';

interface Props {
  aggregations?: Aggregations;
  selectedFilters: Record<string, string[]>;
  onToggle: (facet: string, value: string) => void;
}

export default function FacetPanel({ aggregations, selectedFilters, onToggle }: Props) {
  const [expandedFacets, setExpandedFacets] = useState<Set<string>>(new Set());
  const [searchTerms, setSearchTerms] = useState<Record<string, string>>({});
  const [showCounts, setShowCounts] = useState(true);

  if (!aggregations || Object.keys(aggregations).length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
        <p className="text-sm text-gray-500">No filters available</p>
      </div>
    );
  }

  const toggleFacet = (facetName: string) => {
    const newExpanded = new Set(expandedFacets);
    if (newExpanded.has(facetName)) {
      newExpanded.delete(facetName);
    } else {
      newExpanded.add(facetName);
    }
    setExpandedFacets(newExpanded);
  };

  const updateSearchTerm = (facetName: string, term: string) => {
    setSearchTerms(prev => ({
      ...prev,
      [facetName]: term
    }));
  };

  const clearSearchTerm = (facetName: string) => {
    setSearchTerms(prev => {
      const { [facetName]: _, ...rest } = prev;
      return rest;
    });
  };

  const getDisplayName = (facetName: string): string => {
    const displayNames: Record<string, string> = {
      'entity_types': 'Entity Types',
      'source': 'Sources',
      'author': 'Authors',
      'date': 'Date',
      'type': 'Document Type',
      'language': 'Language',
      'category': 'Category',
      'tags': 'Tags'
    };
    
    return displayNames[facetName] || facetName.charAt(0).toUpperCase() + facetName.slice(1).replace('_', ' ');
  };

  const getFilteredBuckets = (facetName: string, buckets: any[]) => {
    const searchTerm = searchTerms[facetName]?.toLowerCase() || '';
    if (!searchTerm) return buckets;
    
    return buckets.filter(bucket => 
      bucket.key.toLowerCase().includes(searchTerm)
    );
  };

  const getTotalSelected = () => {
    return Object.values(selectedFilters).reduce((sum, values) => sum + values.length, 0);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          Filters
          {getTotalSelected() > 0 && (
            <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
              {getTotalSelected()}
            </span>
          )}
        </h3>
        
        <div className="flex items-center gap-2">
          <label className="flex items-center text-sm text-gray-600">
            <input
              type="checkbox"
              checked={showCounts}
              onChange={(e) => setShowCounts(e.target.checked)}
              className="mr-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            Show counts
          </label>
        </div>
      </div>
      
      <div className="space-y-4">
        {Object.entries(aggregations).map(([facetName, buckets]) => {
          const isExpanded = expandedFacets.has(facetName);
          const selectedCount = selectedFilters[facetName]?.length || 0;
          const filteredBuckets = getFilteredBuckets(facetName, buckets);
          const searchTerm = searchTerms[facetName] || '';
          
          return (
            <div key={facetName} className="border border-gray-200 rounded-lg">
              <button
                onClick={() => toggleFacet(facetName)}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-900">
                    {getDisplayName(facetName)}
                  </span>
                  {selectedCount > 0 && (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      {selectedCount}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-1">
                  <span className="text-xs text-gray-500">
                    {buckets.length}
                  </span>
                  {isExpanded ? (
                    <ChevronDown size={16} className="text-gray-400" />
                  ) : (
                    <ChevronRight size={16} className="text-gray-400" />
                  )}
                </div>
              </button>
              
              {isExpanded && (
                <div className="border-t border-gray-200 p-3">
                  {/* Search within facet */}
                  {buckets.length > 5 && (
                    <div className="relative mb-3">
                      <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={14} />
                      <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => updateSearchTerm(facetName, e.target.value)}
                        placeholder={`Search in ${getDisplayName(facetName).toLowerCase()}...`}
                        className="w-full pl-7 pr-7 py-1.5 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                      />
                      {searchTerm && (
                        <button
                          onClick={() => clearSearchTerm(facetName)}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          <X size={14} />
                        </button>
                      )}
                    </div>
                  )}
                  
                  {/* Facet values */}
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {filteredBuckets.length > 0 ? (
                      filteredBuckets.map((bucket) => {
                        const isSelected = selectedFilters[facetName]?.includes(bucket.key) ?? false;
                        const isDisabled = bucket.doc_count === 0;
                        
                        return (
                          <label
                            key={bucket.key}
                            className={`flex items-center justify-between cursor-pointer group ${
                              isDisabled ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                          >
                            <div className="flex items-center min-w-0 flex-1">
                              <input
                                type="checkbox"
                                checked={isSelected}
                                disabled={isDisabled}
                                onChange={() => !isDisabled && onToggle(facetName, bucket.key)}
                                className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500 disabled:opacity-50"
                              />
                              <span 
                                className={`text-sm truncate ${
                                  isSelected ? 'font-medium text-gray-900' : 'text-gray-700'
                                }`}
                                title={bucket.key}
                              >
                                {bucket.key}
                              </span>
                            </div>
                            
                            {showCounts && (
                              <span className={`ml-2 text-xs px-1.5 py-0.5 rounded ${
                                isSelected 
                                  ? 'bg-primary-100 text-primary-800' 
                                  : 'bg-gray-100 text-gray-600'
                              }`}>
                                {bucket.doc_count.toLocaleString()}
                              </span>
                            )}
                          </label>
                        );
                      })
                    ) : (
                      <p className="text-sm text-gray-500 italic">
                        No items match "{searchTerm}"
                      </p>
                    )}
                  </div>
                  
                  {/* Show more/less for long lists */}
                  {buckets.length > 10 && !searchTerm && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <button
                        onClick={() => updateSearchTerm(facetName, '')}
                        className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                      >
                        View all {buckets.length} options
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Clear all filters */}
      {getTotalSelected() > 0 && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <button
            onClick={() => {
              Object.keys(selectedFilters).forEach(facetName => {
                selectedFilters[facetName].forEach(value => {
                  onToggle(facetName, value);
                });
              });
            }}
            className="w-full px-3 py-2 text-sm font-medium text-gray-700 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
}
