import { useRef, useEffect } from "react";
import { Search } from "lucide-react";
import { SEARCH_SUGGESTIONS, SearchSuggestion } from "@/lib/search/search-config";

interface SearchHeaderProps {
  query: string;
  setQuery: (query: string) => void;
  onSearch: (searchQuery?: string) => void;
  onClear: () => void;
}

export default function SearchHeader({ query, setQuery, onSearch, onClear }: SearchHeaderProps) {
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Focus search input on mount
  useEffect(() => {
    searchInputRef.current?.focus();
  }, []);

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  const selectSuggestion = (suggestion: string) => {
    setQuery(suggestion);
    onSearch(suggestion);
  };

  return (
    <div className="space-y-4">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-6 w-6 text-gray-400" />
        </div>
        <input
          ref={searchInputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Search documents, entities, connections..."
          className="block w-full pl-12 pr-4 py-4 text-lg border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400"
        />
        {query && (
          <button
            onClick={onClear}
            className="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600"
          >
            ×
          </button>
        )}
      </div>

      {/* Search Suggestions */}
      {!query && (
        <div className="space-y-2">
          <p className="text-sm text-gray-600 dark:text-slate-400">Popular searches:</p>
          <div className="flex flex-wrap gap-2">
            {SEARCH_SUGGESTIONS.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => selectSuggestion(suggestion.text)}
                className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-slate-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              >
                <span>{suggestion.text}</span>
                <span className="text-xs text-gray-500 dark:text-slate-400">
                  ({suggestion.category})
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
