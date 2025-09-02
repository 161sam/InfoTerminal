import React from 'react';

export interface NewsItem { id: string; title: string; date: string; url?: string }
interface Props { items: NewsItem[]; onItemClick?: (id: string) => void }

export const NewsTimeline: React.FC<Props> = ({ items, onItemClick }) => (
  <ul data-testid="news-timeline">
    {items.map((n) => (
      <li key={n.id} onClick={() => onItemClick && onItemClick(n.id)}>
        <span>{n.date}</span> - {n.title}
      </li>
    ))}
  </ul>
);
