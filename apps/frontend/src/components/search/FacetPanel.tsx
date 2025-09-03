import type { Aggregations } from '../../types/search';

interface Props {
  aggregations?: Aggregations;
  selectedFilters: Record<string, string[]>;
  onToggle: (facet: string, value: string) => void;
}

export default function FacetPanel({ aggregations, selectedFilters, onToggle }: Props) {
  if (!aggregations) return null;
  return (
    <aside>
      {Object.entries(aggregations).map(([facet, buckets]) => (
        <div key={facet}>
          <strong>{facet}</strong>
          <ul>
            {buckets.map((b) => {
              const selected = selectedFilters[facet]?.includes(b.key) ?? false;
              return (
                <li key={b.key}>
                  <label>
                    <input
                      type="checkbox"
                      disabled={b.doc_count === 0}
                      checked={selected}
                      onChange={() => onToggle(facet, b.key)}
                    />
                    {b.key} ({b.doc_count})
                  </label>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </aside>
  );
}
