import { useMemo } from 'react';
import EntityBadge from './EntityBadge';
import { EntityLabel } from '@/lib/entities';

export type BadgeItem = {
  label: EntityLabel;
  value?: string;
  count?: number;
  nodeId?: string;
};

type Props = {
  items: BadgeItem[];
  onBadgeClick?: (item: BadgeItem) => void;
  collapseAfter?: number;
};

export default function EntityBadgeList({ items, onBadgeClick, collapseAfter = 12 }: Props) {
  const deduped = useMemo(() => {
    const map = new Map<string, BadgeItem>();
    for (const it of items) {
      const key = `${it.label}:${(it.value || '').toLowerCase()}`;
      const existing = map.get(key);
      if (existing) existing.count = (existing.count || 1) + (it.count || 1);
      else map.set(key, { ...it, count: it.count || 1 });
    }
    return Array.from(map.values()).sort((a, b) => {
      if (a.label === b.label) return (a.value || '').localeCompare(b.value || '');
      return a.label.localeCompare(b.label);
    });
  }, [items]);

  const shown = deduped.slice(0, collapseAfter);
  const hidden = deduped.slice(collapseAfter);

  const renderBadge = (item: BadgeItem, i: number) => (
    <EntityBadge
      key={i}
      label={item.label}
      value={item.value}
      clickable={!!onBadgeClick}
      countBadge={item.count}
      onClick={() => onBadgeClick?.(item)}
    />
  );

  return (
    <div className="flex flex-wrap gap-1">
      {shown.map(renderBadge)}
      {hidden.length > 0 && (
        <details>
          <summary className="cursor-pointer">+{hidden.length} mehr</summary>
          <div className="flex flex-wrap gap-1 mt-1">{hidden.map(renderBadge)}</div>
        </details>
      )}
    </div>
  );
}

