// Entity table/grid component for displaying filtered entities
import { User } from "lucide-react";
import { Entity } from "@/lib/entities/entity-config";
import { EntityCard } from "./EntityCard";

interface EntityTableProps {
  entities: Entity[];
  onEntityAction: (entity: Entity, action: string) => void;
  isLoading?: boolean;
}

export function EntityTable({ entities, onEntityAction, isLoading = false }: EntityTableProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4">
        {[...Array(6)].map((_, index) => (
          <div
            key={index}
            className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 animate-pulse"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3 flex-1">
                <div className="w-5 h-5 bg-gray-300 dark:bg-gray-600 rounded"></div>
                <div>
                  <div className="h-5 bg-gray-300 dark:bg-gray-600 rounded w-32 mb-2"></div>
                  <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-20"></div>
                </div>
              </div>
              <div className="flex gap-1">
                <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded"></div>
                <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded"></div>
                <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded"></div>
              </div>
            </div>

            <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-full mb-4"></div>

            <div className="grid grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i}>
                  <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded w-16 mb-1"></div>
                  <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-12"></div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (entities.length === 0) {
    return (
      <div className="text-center py-12">
        <User size={48} className="mx-auto text-gray-400 dark:text-slate-500 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">
          No entities found
        </h3>
        <p className="text-gray-500 dark:text-slate-400 mb-4">
          No entities match your current search and filter criteria.
        </p>
        <div className="text-sm text-gray-400 dark:text-slate-500">
          Try adjusting your filters or upload new documents to detect entities.
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4">
        {entities.map((entity) => (
          <EntityCard key={entity.id} entity={entity} onAction={onEntityAction} />
        ))}
      </div>

      {/* Results summary */}
      <div className="text-center text-sm text-gray-500 dark:text-slate-400 pt-4 border-t border-gray-200 dark:border-gray-700">
        Showing {entities.length} entities
      </div>
    </div>
  );
}

export default EntityTable;
