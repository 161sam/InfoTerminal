import React from 'react';
import { EntityResult, ENTITY_COLORS } from './types';

interface NLPEntityHighlighterProps {
  text: string;
  entities: EntityResult[];
}

export function highlightEntities(text: string, entities: EntityResult[]) {
  if (!entities?.length) return text;

  const sortedEntities = [...entities].sort((a, b) => a.start - b.start);
  let result = [];
  let lastEnd = 0;

  sortedEntities.forEach((entity, index) => {
    if (entity.start > lastEnd) {
      result.push(text.slice(lastEnd, entity.start));
    }

    const colorClass = ENTITY_COLORS[entity.label] || ENTITY_COLORS.DEFAULT;
    result.push(
      <span
        key={index}
        className={`px-2 py-1 rounded-md border ${colorClass} font-medium`}
        title={`${entity.label} (${Math.round(entity.confidence * 100)}%)`}
      >
        {entity.text}
      </span>
    );

    lastEnd = entity.end;
  });

  if (lastEnd < text.length) {
    result.push(text.slice(lastEnd));
  }

  return result;
}

export default function NLPEntityHighlighter({ text, entities }: NLPEntityHighlighterProps) {
  return (
    <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border text-sm leading-relaxed">
      {highlightEntities(text, entities)}
    </div>
  );
}
