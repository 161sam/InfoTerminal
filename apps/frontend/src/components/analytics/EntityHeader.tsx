import React from 'react';

interface Props {
  title: string;
  type: string;
  supersetUrl?: string;
}

export const EntityHeader: React.FC<Props> = ({ title, type, supersetUrl }) => (
  <header data-testid="entity-header">
    <h1>{title}</h1>
    <span>{type}</span>
    {supersetUrl && (
      <a href={supersetUrl} target="_blank" rel="noreferrer">
        Open in Superset
      </a>
    )}
  </header>
);
