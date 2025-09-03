interface Props {
  filters: Record<string, string[]>;
  onRemove: (facet: string, value: string) => void;
  onClearAll: () => void;
}

export default function FilterChips({ filters, onRemove, onClearAll }: Props) {
  const entries = Object.entries(filters).flatMap(([facet, values]) =>
    values.map((v) => ({ facet, value: v })),
  );
  if (entries.length === 0) return null;

  return (
    <div>
      {entries.map(({ facet, value }) => (
        <span key={`${facet}:${value}`}>
          {facet}: {value}{' '}
          <button onClick={() => onRemove(facet, value)}>x</button>
        </span>
      ))}
      <button onClick={onClearAll}>Clear all</button>
    </div>
  );
}
