import { Search } from "lucide-react";
import { LoadingSpinner, EmptyState, ErrorState } from "@/components/ui/loading";
import DossierButton from "@/components/DossierButton";
import { SearchResult, formatSearchTime } from "@/lib/search/search-config";
import SearchResultCard from "./SearchResultCard";

interface SearchResultsProps {
  query: string;
  results: SearchResult[];
  totalResults: number;
  searchTime: number;
  isLoading: boolean;
  error: string | null;
  onRetry: () => void;
}

export default function SearchResults({
  query,
  results,
  totalResults,
  searchTime,
  isLoading,
  error,
  onRetry,
}: SearchResultsProps) {
  // Error state
  if (error) {
    return (
      <ErrorState
        variant="error"
        title="Search Error"
        message={error}
        action={{
          label: "Try Again",
          onClick: onRetry,
        }}
      />
    );
  }

  // Loading state
  if (isLoading) {
    return (
      <LoadingSpinner
        layout="block"
        variant="primary"
        size="lg"
        text="Searching..."
        subText="Finding relevant results"
      />
    );
  }

  // Empty state
  if (!isLoading && query && results.length === 0 && !error) {
    return (
      <EmptyState
        icon={Search}
        title="No results found"
        message="Try adjusting your search terms or filters"
      />
    );
  }

  // Results state
  if (results.length > 0) {
    return (
      <>
        {/* Results Header */}
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600 dark:text-slate-400">
            {totalResults.toLocaleString()} results found in {formatSearchTime(searchTime)}
          </p>
          <DossierButton
            getPayload={() => ({
              query,
              entities: [],
              graphSelection: { nodes: [], edges: [] },
              searchResults: results,
            })}
          />
        </div>

        {/* Results List */}
        <div className="space-y-4">
          {results.map((result) => (
            <SearchResultCard key={result.id} result={result} />
          ))}
        </div>
      </>
    );
  }

  return null;
}
