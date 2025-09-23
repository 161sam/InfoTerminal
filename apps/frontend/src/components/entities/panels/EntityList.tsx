import React from 'react';
import { User } from 'lucide-react';
import EntityCard from './EntityCard';
import { Entity, EntityFilter } from './types';

interface EntityListProps {
  entities: Entity[];
  filters: EntityFilter;
  onAction: (entity: Entity, action: string) => void;
}

export default function EntityList({ entities, filters, onAction }: EntityListProps) {
  
  const hasActiveFilters = filters.searchTerm || filters.type !== 'all' || 
                          filters.verified !== 'all' || filters.riskLevel !== 'all' || 
                          filters.minMentions > 0;

  if (entities.length === 0) {
    return (
      <div className="text-center py-12">
        <User size={48} className="mx-auto text-gray-400 dark:text-slate-500 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">No entities found</h3>
        <p className="text-gray-500 dark:text-slate-400">
          {hasActiveFilters 
            ? 'Try adjusting your search filters to find more entities' 
            : 'Upload documents or add entities manually to get started'
          }
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {entities.map((entity) => (
        <EntityCard 
          key={entity.id} 
          entity={entity} 
          onAction={onAction}
        />
      ))}
    </div>
  );
}
