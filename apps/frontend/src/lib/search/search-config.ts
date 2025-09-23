// Search types and configuration
import { Star, Calendar, SortAsc, FileText, Users, MapPin } from 'lucide-react';

export interface SearchResult {
  id: string;
  title?: string;
  snippet?: string;
  score?: number;
  date?: string;
  type?: string;
  source?: string;
  entities?: string[];
  url?: string;
}

export interface SearchFilters {
  type: string;
  dateRange: string;
  source: string;
  minScore: number;
}

export interface SearchSuggestion {
  text: string;
  category: string;
}

export interface SortOption {
  value: string;
  label: string;
  icon: any;
}

export interface ResultType {
  value: string;
  label: string;
  count: number | null;
}

export const SEARCH_SUGGESTIONS: SearchSuggestion[] = [
  { text: "financial networks", category: "Analysis" },
  { text: "ACME Corporation", category: "Organizations" },
  { text: "recent documents", category: "Documents" },
  { text: "entity connections", category: "Graph" },
  { text: "risk indicators", category: "Analysis" },
  { text: "John Smith", category: "People" },
  { text: "London office", category: "Locations" }
];

export const SORT_OPTIONS: SortOption[] = [
  { value: "relevance", label: "Relevance", icon: Star },
  { value: "date_desc", label: "Newest First", icon: Calendar },
  { value: "date_asc", label: "Oldest First", icon: Calendar },
  { value: "score", label: "Score", icon: SortAsc }
];

export const RESULT_TYPES: ResultType[] = [
  { value: "all", label: "All Results", count: null },
  { value: "document", label: "Documents", count: null },
  { value: "entity", label: "Entities", count: null },
  { value: "connection", label: "Connections", count: null }
];

export const RECENT_SEARCHES = [
  'financial networks', 
  'ACME Corporation', 
  'risk analysis'
];

// Utility functions
export function formatSearchTime(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

export function getResultTypeIcon(type: string) {
  switch (type) {
    case 'document': return FileText;
    case 'entity': return Users;
    case 'location': return MapPin;
    default: return FileText;
  }
}

export function createSearchExportData(
  query: string, 
  filters: SearchFilters, 
  sort: string,
  results: SearchResult[], 
  totalResults: number, 
  searchTime: number
) {
  return {
    query,
    filters,
    sort,
    results,
    totalResults,
    searchTime,
    timestamp: new Date().toISOString()
  };
}
