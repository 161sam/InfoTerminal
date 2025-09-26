/**
 * Smart Search Component with Autocomplete and Suggestions
 *
 * Provides intelligent search with real-time suggestions, recent searches,
 * and saved searches functionality optimized for OSINT workflows.
 */

import React, { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { Search, Clock, Star, TrendingUp, Filter, X, ArrowRight, BookmarkPlus } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useDebounce } from "@/hooks/useDebounce";
import UserJourneyTracker from "@/lib/user-journey-tracker";

interface SearchSuggestion {
  id: string;
  text: string;
  type: "entity" | "query" | "filter" | "recent" | "saved";
  confidence: number;
  metadata?: {
    entityType?: string;
    resultCount?: number;
    lastUsed?: string;
    category?: string;
    query?: string;
  };
}

interface RecentSearch {
  id: string;
  query: string;
  timestamp: Date;
  resultCount: number;
  filters?: Record<string, any>;
}

interface SavedSearch {
  id: string;
  name: string;
  query: string;
  filters?: Record<string, any>;
  createdAt: Date;
  tags: string[];
}

interface SmartSearchProps {
  placeholder?: string;
  onSearch: (query: string, filters?: Record<string, any>) => void;
  onSuggestionSelect?: (suggestion: SearchSuggestion) => void;
  initialValue?: string;
  showFilters?: boolean;
  showHistory?: boolean;
  className?: string;
}

const SmartSearch: React.FC<SmartSearchProps> = ({
  placeholder = "Search entities, domains, or enter OSINT queries...",
  onSearch,
  onSuggestionSelect,
  initialValue = "",
  showFilters = true,
  showHistory = true,
  className = "",
}) => {
  const [query, setQuery] = useState(initialValue);
  const [isOpen, setIsOpen] = useState(false);
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [recentSearches, setRecentSearches] = useState<RecentSearch[]>([]);
  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [isLoading, setIsLoading] = useState(false);
  const [activeFilters, setActiveFilters] = useState<Record<string, any>>({});
  const [showSaveDialog, setShowSaveDialog] = useState(false);

  const searchInputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);
  const debouncedQuery = useDebounce(query, 300);

  const { trackSearch, trackClick } = UserJourneyTracker.useUserJourney();

  // effects moved below to avoid "used before declaration" type errors

  const loadRecentSearches = useCallback(() => {
    try {
      const stored = localStorage.getItem("infoterminal_recent_searches");
      if (stored) {
        const parsed = JSON.parse(stored);
        setRecentSearches(
          parsed.map((item: any) => ({
            ...item,
            timestamp: new Date(item.timestamp),
          })),
        );
      }
    } catch (error) {
      console.warn("Failed to load recent searches:", error);
    }
  }, []);

  const loadSavedSearches = useCallback(() => {
    try {
      const stored = localStorage.getItem("infoterminal_saved_searches");
      if (stored) {
        const parsed = JSON.parse(stored);
        setSavedSearches(
          parsed.map((item: any) => ({
            ...item,
            createdAt: new Date(item.createdAt),
          })),
        );
      }
    } catch (error) {
      console.warn("Failed to load saved searches:", error);
    }
  }, []);

  const saveRecentSearch = useCallback(
    (searchQuery: string, resultCount: number) => {
      const newSearch: RecentSearch = {
        id: Date.now().toString(),
        query: searchQuery,
        timestamp: new Date(),
        resultCount,
        filters: activeFilters,
      };

      setRecentSearches((prev) => {
        const filtered = prev.filter((s) => s.query !== searchQuery);
        const updated = [newSearch, ...filtered].slice(0, 10); // Keep last 10

        try {
          localStorage.setItem("infoterminal_recent_searches", JSON.stringify(updated));
        } catch (error) {
          console.warn("Failed to save recent search:", error);
        }

        return updated;
      });
    },
    [activeFilters],
  );

  const fetchSuggestions = useCallback(async (searchQuery: string) => {
    if (!searchQuery.trim()) return;

    setIsLoading(true);

    try {
      const response = await fetch("/api/search/suggestions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: searchQuery,
          includeEntities: true,
          includeQueries: true,
          limit: 8,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSuggestions(data.suggestions || []);
      }
    } catch (error) {
      console.warn("Failed to fetch suggestions:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);
    setIsOpen(true);
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleInputBlur = (e: React.FocusEvent) => {
    // Delay closing to allow clicking on suggestions
    setTimeout(() => {
      if (!suggestionsRef.current?.contains(e.relatedTarget as Node)) {
        setIsOpen(false);
      }
    }, 100);
  };

  // allSuggestions is defined below; keep handlers after it's available
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen) return;

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setSelectedIndex((prev) => (prev < allSuggestions.length - 1 ? prev + 1 : 0));
        break;
      case "ArrowUp":
        e.preventDefault();
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : allSuggestions.length - 1));
        break;
      case "Enter":
        e.preventDefault();
        if (selectedIndex >= 0) {
          const arr = allSuggestions;
          handleSuggestionClick(arr[selectedIndex]);
        } else {
          handleSearch();
        }
        break;
      case "Escape":
        setIsOpen(false);
        setSelectedIndex(-1);
        searchInputRef.current?.blur();
        break;
    }
  };

  const allSuggestions = useMemo(() => {
    const all: SearchSuggestion[] = [];

    // Add query suggestions
    all.push(...suggestions);

    // Add recent searches if query is empty or matches
    if (showHistory && query.length < 2) {
      all.push(
        ...recentSearches.slice(0, 3).map((search) => ({
          id: `recent_${search.id}`,
          text: search.query,
          type: "recent" as const,
          confidence: 1.0,
          metadata: {
            resultCount: search.resultCount,
            lastUsed: search.timestamp.toISOString(),
          },
        })),
      );
    }

    // Add saved searches that match query
    if (showHistory) {
      const matchingSaved = savedSearches
        .filter(
          (saved) =>
            saved.name.toLowerCase().includes(query.toLowerCase()) ||
            saved.query.toLowerCase().includes(query.toLowerCase()),
        )
        .slice(0, 2);

      all.push(
        ...matchingSaved.map((saved) => ({
          id: `saved_${saved.id}`,
          text: saved.name,
          type: "saved" as const,
          confidence: 1.0,
          metadata: {
            query: saved.query,
            category: saved.tags.join(", "),
          },
        })),
      );
    }

    return all;
  }, [suggestions, recentSearches, savedSearches, query, showHistory]);

  // Load saved data on mount
  useEffect(() => {
    loadRecentSearches();
    loadSavedSearches();
  }, [loadRecentSearches, loadSavedSearches]);

  // Fetch suggestions when query changes
  useEffect(() => {
    if (debouncedQuery.trim().length >= 2) {
      fetchSuggestions(debouncedQuery);
    } else {
      setSuggestions([]);
    }
  }, [debouncedQuery, fetchSuggestions]);

  const handleSuggestionClick = (suggestion: SearchSuggestion) => {
    let searchQuery = suggestion.text;

    if (suggestion.type === "saved" && suggestion.metadata?.query) {
      searchQuery = suggestion.metadata.query;
    }

    setQuery(searchQuery);
    setIsOpen(false);
    setSelectedIndex(-1);

    // Track suggestion usage
    trackClick("search-suggestion-selected", {
      suggestionType: suggestion.type,
      confidence: suggestion.confidence,
    });

    if (onSuggestionSelect) {
      onSuggestionSelect(suggestion);
    }

    // Execute search
    executeSearch(searchQuery);
  };

  const handleSearch = () => {
    if (query.trim()) {
      executeSearch(query.trim());
    }
  };

  const executeSearch = async (searchQuery: string) => {
    const startTime = Date.now();

    try {
      // Execute the search
      await onSearch(searchQuery, activeFilters);

      const responseTime = Date.now() - startTime;

      // Track search
      trackSearch(searchQuery, 0, responseTime); // Result count will be updated by parent

      // Save to recent searches
      saveRecentSearch(searchQuery, 0); // Result count will be updated

      setIsOpen(false);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  const handleFilterChange = (filterKey: string, value: any) => {
    setActiveFilters((prev) => ({
      ...prev,
      [filterKey]: value,
    }));
  };

  const removeFilter = (filterKey: string) => {
    setActiveFilters((prev) => {
      const updated = { ...prev };
      delete updated[filterKey];
      return updated;
    });
  };

  const clearAllFilters = () => {
    setActiveFilters({});
  };

  const saveCurrentSearch = async (name: string, tags: string[]) => {
    const newSavedSearch: SavedSearch = {
      id: Date.now().toString(),
      name,
      query: query.trim(),
      filters: activeFilters,
      createdAt: new Date(),
      tags,
    };

    setSavedSearches((prev) => {
      const updated = [newSavedSearch, ...prev];

      try {
        localStorage.setItem("infoterminal_saved_searches", JSON.stringify(updated));
      } catch (error) {
        console.warn("Failed to save search:", error);
      }

      return updated;
    });

    setShowSaveDialog(false);
    trackClick("search-saved", { query: query.trim() });
  };

  const getSuggestionIcon = (type: SearchSuggestion["type"]) => {
    switch (type) {
      case "entity":
        return <TrendingUp className="w-4 h-4 text-blue-500" />;
      case "recent":
        return <Clock className="w-4 h-4 text-gray-500" />;
      case "saved":
        return <Star className="w-4 h-4 text-yellow-500" />;
      case "filter":
        return <Filter className="w-4 h-4 text-purple-500" />;
      default:
        return <Search className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className={`smart-search-container ${className}`}>
      {/* Search Input */}
      <div className="search-input-wrapper">
        <div className="search-input-container">
          <Search className="search-icon w-5 h-5 text-gray-400" />

          <input
            ref={searchInputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            onFocus={handleInputFocus}
            onBlur={handleInputBlur}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className="search-input"
            autoComplete="off"
            spellCheck="false"
          />

          {query && (
            <button
              onClick={() => {
                setQuery("");
                setSuggestions([]);
                searchInputRef.current?.focus();
              }}
              className="clear-button"
            >
              <X className="w-4 h-4" />
            </button>
          )}

          {query.trim() && (
            <button
              onClick={() => setShowSaveDialog(true)}
              className="save-search-button"
              title="Save this search"
            >
              <BookmarkPlus className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Active Filters */}
        {Object.keys(activeFilters).length > 0 && (
          <div className="active-filters">
            {Object.entries(activeFilters).map(([key, value]) => (
              <span key={key} className="filter-tag">
                {key}: {String(value)}
                <button onClick={() => removeFilter(key)} className="remove-filter">
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
            <button onClick={clearAllFilters} className="clear-all-filters">
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Suggestions Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            ref={suggestionsRef}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="suggestions-dropdown"
          >
            {isLoading && (
              <div className="suggestion-item loading">
                <div className="loading-spinner" />
                <span>Searching...</span>
              </div>
            )}

      {!isLoading && allSuggestions.length === 0 && query.trim().length >= 2 && (
              <div className="no-suggestions">
                <Search className="w-4 h-4 text-gray-400" />
                <span>No suggestions found</span>
              </div>
            )}

            {!isLoading &&
              allSuggestions.map((suggestion, index) => (
                <button
                  key={suggestion.id}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className={`suggestion-item ${index === selectedIndex ? "selected" : ""}`}
                  onMouseEnter={() => setSelectedIndex(index)}
                >
                  <div className="suggestion-icon">{getSuggestionIcon(suggestion.type)}</div>

                  <div className="suggestion-content">
                    <div className="suggestion-text">{suggestion.text}</div>

                    {suggestion.metadata && (
                      <div className="suggestion-metadata">
                        {suggestion.type === "recent" && suggestion.metadata.resultCount && (
                          <span>{suggestion.metadata.resultCount} results</span>
                        )}
                        {suggestion.type === "saved" && suggestion.metadata.category && (
                          <span>{suggestion.metadata.category}</span>
                        )}
                        {suggestion.type === "entity" && suggestion.metadata.entityType && (
                          <span>{suggestion.metadata.entityType}</span>
                        )}
                      </div>
                    )}
                  </div>

                  <ArrowRight className="suggestion-arrow w-4 h-4 opacity-0 group-hover:opacity-100" />
                </button>
              ))}

            {!isLoading &&
              query.trim().length < 2 &&
              recentSearches.length === 0 &&
              savedSearches.length === 0 && (
                <div className="empty-state">
                  <Search className="w-8 h-8 text-gray-300 mb-2" />
                  <p className="text-sm text-gray-500">
                    Start typing to search entities, domains, or enter OSINT queries
                  </p>
                </div>
              )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Save Search Dialog */}
      <AnimatePresence>
        {showSaveDialog && (
          <SaveSearchDialog
            query={query}
            onSave={saveCurrentSearch}
            onCancel={() => setShowSaveDialog(false)}
          />
        )}
      </AnimatePresence>

      <style jsx>{`
        .smart-search-container {
          position: relative;
          width: 100%;
        }

        .search-input-wrapper {
          width: 100%;
        }

        .search-input-container {
          position: relative;
          display: flex;
          align-items: center;
          background: white;
          border: 2px solid #e5e7eb;
          border-radius: 12px;
          padding: 12px 16px;
          transition: all 0.2s ease;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .search-input-container:focus-within {
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .search-icon {
          margin-right: 12px;
          flex-shrink: 0;
        }

        .search-input {
          flex: 1;
          border: none;
          outline: none;
          font-size: 16px;
          background: transparent;
          color: #1f2937;
        }

        .search-input::placeholder {
          color: #9ca3af;
        }

        .clear-button,
        .save-search-button {
          margin-left: 8px;
          padding: 4px;
          border-radius: 4px;
          border: none;
          background: transparent;
          color: #6b7280;
          cursor: pointer;
          transition: all 0.2s ease;
          flex-shrink: 0;
        }

        .clear-button:hover,
        .save-search-button:hover {
          background: #f3f4f6;
          color: #374151;
        }

        .active-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-top: 8px;
          align-items: center;
        }

        .filter-tag {
          display: flex;
          align-items: center;
          gap: 4px;
          background: #eff6ff;
          color: #1e40af;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 12px;
          border: 1px solid #dbeafe;
        }

        .remove-filter {
          padding: 0;
          border: none;
          background: none;
          color: inherit;
          cursor: pointer;
          border-radius: 2px;
        }

        .remove-filter:hover {
          background: rgba(0, 0, 0, 0.1);
        }

        .clear-all-filters {
          font-size: 12px;
          color: #6b7280;
          background: none;
          border: none;
          cursor: pointer;
          text-decoration: underline;
        }

        .clear-all-filters:hover {
          color: #374151;
        }

        .suggestions-dropdown {
          position: absolute;
          top: 100%;
          left: 0;
          right: 0;
          background: white;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          margin-top: 4px;
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
          z-index: 50;
          max-height: 400px;
          overflow-y: auto;
        }

        .suggestion-item {
          display: flex;
          align-items: center;
          width: 100%;
          padding: 12px 16px;
          border: none;
          background: none;
          text-align: left;
          cursor: pointer;
          transition: background-color 0.15s ease;
          border-bottom: 1px solid #f3f4f6;
          group: true;
        }

        .suggestion-item:last-child {
          border-bottom: none;
        }

        .suggestion-item:hover,
        .suggestion-item.selected {
          background: #f8fafc;
        }

        .suggestion-item.loading {
          pointer-events: none;
          opacity: 0.7;
        }

        .suggestion-icon {
          margin-right: 12px;
          flex-shrink: 0;
        }

        .suggestion-content {
          flex: 1;
          min-width: 0;
        }

        .suggestion-text {
          font-size: 14px;
          color: #1f2937;
          font-weight: 500;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .suggestion-metadata {
          font-size: 12px;
          color: #6b7280;
          margin-top: 2px;
        }

        .suggestion-arrow {
          margin-left: 8px;
          color: #9ca3af;
          transition: opacity 0.15s ease;
        }

        .no-suggestions,
        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 24px;
          color: #6b7280;
          text-align: center;
        }

        .loading-spinner {
          width: 16px;
          height: 16px;
          border: 2px solid #e5e7eb;
          border-top: 2px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-right: 8px;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .search-input-container {
            padding: 10px 12px;
          }

          .search-input {
            font-size: 16px; /* Prevent zoom on iOS */
          }

          .suggestions-dropdown {
            max-height: 300px;
          }
        }
      `}</style>
    </div>
  );
};

// Save Search Dialog Component
interface SaveSearchDialogProps {
  query: string;
  onSave: (name: string, tags: string[]) => void;
  onCancel: () => void;
}

const SaveSearchDialog: React.FC<SaveSearchDialogProps> = ({ query, onSave, onCancel }) => {
  const [name, setName] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      onSave(name.trim(), tags);
    }
  };

  const addTag = (tag: string) => {
    if (tag.trim() && !tags.includes(tag.trim())) {
      setTags((prev) => [...prev, tag.trim()]);
      setTagInput("");
    }
  };

  const removeTag = (index: number) => {
    setTags((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="save-dialog-overlay"
      onClick={onCancel}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        className="save-dialog"
        onClick={(e) => e.stopPropagation()}
      >
        <h3>Save Search</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Query</label>
            <input type="text" value={query} disabled />
          </div>

          <div className="form-group">
            <label>Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Give this search a name"
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Tags</label>
            <div className="tags-input">
              <div className="tags-list">
                {tags.map((tag, index) => (
                  <span key={index} className="tag">
                    {tag}
                    <button type="button" onClick={() => removeTag(index)}>
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addTag(tagInput);
                  }
                }}
                placeholder="Add tags..."
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="button" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" disabled={!name.trim()}>
              Save
            </button>
          </div>
        </form>
      </motion.div>

      <style jsx>{`
        .save-dialog-overlay {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 100;
          padding: 16px;
        }

        .save-dialog {
          background: white;
          border-radius: 12px;
          padding: 24px;
          width: 100%;
          max-width: 400px;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        .save-dialog h3 {
          margin: 0 0 16px 0;
          font-size: 18px;
          font-weight: 600;
          color: #1f2937;
        }

        .form-group {
          margin-bottom: 16px;
        }

        .form-group label {
          display: block;
          margin-bottom: 4px;
          font-size: 14px;
          font-weight: 500;
          color: #374151;
        }

        .form-group input {
          width: 100%;
          padding: 8px 12px;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          font-size: 14px;
        }

        .form-group input:disabled {
          background: #f9fafb;
          color: #6b7280;
        }

        .tags-input {
          border: 1px solid #d1d5db;
          border-radius: 6px;
          padding: 8px;
          min-height: 40px;
        }

        .tags-list {
          display: flex;
          flex-wrap: wrap;
          gap: 4px;
          margin-bottom: 4px;
        }

        .tag {
          background: #eff6ff;
          color: #1e40af;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .tag button {
          background: none;
          border: none;
          color: inherit;
          cursor: pointer;
          font-size: 14px;
          line-height: 1;
        }

        .tags-input input {
          border: none;
          outline: none;
          padding: 0;
          font-size: 14px;
          flex: 1;
        }

        .form-actions {
          display: flex;
          gap: 8px;
          justify-content: flex-end;
          margin-top: 20px;
        }

        .form-actions button {
          padding: 8px 16px;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .form-actions button[type="button"] {
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          color: #374151;
        }

        .form-actions button[type="submit"] {
          background: #3b82f6;
          border: 1px solid #3b82f6;
          color: white;
        }

        .form-actions button:hover {
          opacity: 0.9;
        }

        .form-actions button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
    </motion.div>
  );
};

export default SmartSearch;
