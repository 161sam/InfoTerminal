interface Props {
  filters: Record<string, string[]>;
  entity?: string[];
  value?: string[];
  onRemove: (facet: string, value: string) => void;
  onRemoveEntity?: (label: string) => void;
  onRemoveValue?: (v: string) => void;
  onClearAll: () => void;
}

export default function FilterChips({
  filters,
  entity,
  value,
  onRemove,
  onRemoveEntity,
  onRemoveValue,
  onClearAll,
}: Props) {
  const entries: { type: 'facet' | 'entity' | 'value'; facet?: string; value: string }[] = [
    ...Object.entries(filters).flatMap(([facet, values]) =>
      values.map((v) => ({ type: 'facet' as const, facet, value: v })),
    ),
    ...(entity || []).map((v) => ({ type: 'entity' as const, value: v })),
    ...(value || []).map((v) => ({ type: 'value' as const, value: v })),
  ];
  if (entries.length === 0) return null;

  return (
    <div>
      {entries.map((e) => {
        if (e.type === 'entity') {
          return (
            <span key={`entity:${e.value}`}>
              entity: {e.value}{' '}
              <button onClick={() => onRemoveEntity?.(e.value)}>x</button>
            </span>
          );
        }
        if (e.type === 'value') {
          return (
            <span key={`value:${e.value}`}>
              value: {e.value}{' '}
              <button onClick={() => onRemoveValue?.(e.value)}>x</button>
            </span>
          );
        }
        return (
          <span key={`${e.facet}:${e.value}`}>
            {e.facet}: {e.value}{' '}
            <button onClick={() => onRemove(e.facet!, e.value)}>x</button>
          </span>
        );
      })}
      <button onClick={onClearAll}>Clear all</button>
    </div>
  );
}
