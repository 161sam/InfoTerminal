import SearchBox from '../src/components/search/SearchBox';
import FacetPanel from '../src/components/search/FacetPanel';
import FilterChips from '../src/components/search/FilterChips';
import ResultItem from '../src/components/search/ResultItem';
import Pagination from '../src/components/search/Pagination';
import SortAndRerank from '../src/components/search/SortAndRerank';
import { useSearchParams } from '../src/hooks/useSearchParams';
import { useSearch } from '../src/hooks/useSearch';
import Header from '../src/components/layout/Header';

export default function SearchPage() {
  const { params, set, replaceAll } = useSearchParams();
  const q = (params.q as string) || '';
  const page = parseInt((params.page as string) || '1', 10);
  const pageSize = parseInt((params.pageSize as string) || '20', 10);
  const sort = (params.sort as string) || 'relevance';
  const rerank = params.rerank === '1';

  const filters: Record<string, string[]> = {};
  Object.entries(params).forEach(([k, v]) => {
    if (k.startsWith('filter.')) {
      const facet = k.replace('filter.', '');
      const arr = typeof v === 'string' ? v.split(',') : Array.isArray(v) ? v : [];
      filters[facet] = arr.filter(Boolean);
    }
  });

  const entityParam = params.entity;
  const entity = Array.isArray(entityParam)
    ? (entityParam as string[])
    : entityParam
    ? [entityParam as string]
    : undefined;

  const { data, loading, error } = useSearch({
    q,
    filters,
    entity,
    sort,
    rerank,
    page,
    pageSize,
  });

  const handleFilterToggle = (facet: string, value: string) => {
    const key = `filter.${facet}`;
    const arr = filters[facet] ? [...filters[facet]] : [];
    const idx = arr.indexOf(value);
    if (idx >= 0) arr.splice(idx, 1); else arr.push(value);
    set(key, arr.join(',') || undefined);
    set('page', 1);
  };

  const handleRemoveChip = (facet: string, value: string) => {
    const key = `filter.${facet}`;
    const arr = (filters[facet] || []).filter((v) => v !== value);
    set(key, arr.join(',') || undefined);
    set('page', 1);
  };

  const handleClearAll = () => {
    const next: Record<string, any> = {};
    if (q) next.q = q;
    replaceAll(next);
  };

  return (
    <div>
      <Header />
      <SearchBox
        value={q}
        onChange={(v) => set('q', v)}
        onSubmit={(v) => set('q', v)}
        loading={loading}
      />
      <SortAndRerank
        sort={sort}
        onSortChange={(v) => set('sort', v)}
        rerank={rerank}
        onRerankToggle={(v) => set('rerank', v ? '1' : undefined)}
      />
      <FilterChips filters={filters} onRemove={handleRemoveChip} onClearAll={handleClearAll} />
      {error && <div>Error: {String(error.message)}</div>}
      {!error && data && data.total === 0 && <div>No results</div>}
      <div style={{ display: 'flex' }}>
        <FacetPanel aggregations={data?.aggregations} selectedFilters={filters} onToggle={handleFilterToggle} />
        <div data-testid="search-results" style={{ marginLeft: '1rem' }}>
          {data?.items.map((hit) => (
            <ResultItem key={hit.id} hit={hit} />
          ))}
        </div>
      </div>
      {data && data.total > pageSize && (
        <Pagination
          page={page}
          pageSize={pageSize}
          total={data.total}
          onPageChange={(p) => set('page', p)}
        />
      )}
    </div>
  );
}
