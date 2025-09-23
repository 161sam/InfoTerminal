// Individual entity card component
import { useState } from 'react';
import { Eye, Edit, Trash2, CheckCircle2, Clock, ExternalLink } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import EntityBadge from '@/components/entities/EntityBadge';
import { Entity, ENTITY_TYPE_ICONS, getRiskColor } from '@/lib/entities/entity-config';

interface EntityCardProps {
  entity: Entity;
  onAction: (entity: Entity, action: string) => void;
}

export function EntityCard({ entity, onAction }: EntityCardProps) {
  const Icon = ENTITY_TYPE_ICONS[entity.type];

  return (
    <Panel className="hover:shadow-md transition-shadow">
      <div className="space-y-3">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <div className="flex-shrink-0">
              <Icon size={20} className="text-gray-600 dark:text-slate-400" />
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="font-semibold text-gray-900 dark:text-slate-100 truncate">
                  {entity.name}
                </h4>
                <EntityBadge label={entity.type} />
                {entity.verified ? (
                  <CheckCircle2 size={14} className="text-green-500 flex-shrink-0" />
                ) : (
                  <Clock size={14} className="text-yellow-500 flex-shrink-0" />
                )}
              </div>
              
              {entity.riskScore !== undefined && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500 dark:text-slate-400">Risk Score:</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${getRiskColor(entity.riskScore)}`}>
                    {entity.riskScore}/10
                  </span>
                </div>
              )}
            </div>
          </div>
          
          {/* Action buttons */}
          <div className="flex items-center gap-1 flex-shrink-0">
            <button
              onClick={() => onAction(entity, 'view')}
              className="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 rounded"
              title="View details"
            >
              <Eye size={16} />
            </button>
            <button
              onClick={() => onAction(entity, 'graph')}
              className="p-1 text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 rounded"
              title="View in graph"
            >
              <ExternalLink size={16} />
            </button>
            <button
              onClick={() => onAction(entity, 'edit')}
              className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
              title="Edit entity"
            >
              <Edit size={16} />
            </button>
          </div>
        </div>
        
        {/* Description */}
        {entity.description && (
          <p className="text-sm text-gray-600 dark:text-slate-400 line-clamp-2">
            {entity.description}
          </p>
        )}
        
        {/* Stats grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-gray-500 dark:text-slate-400">Mentions</span>
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {entity.mentions}
            </div>
          </div>
          <div>
            <span className="text-gray-500 dark:text-slate-400">Confidence</span>
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {Math.round(entity.confidence * 100)}%
            </div>
          </div>
          <div>
            <span className="text-gray-500 dark:text-slate-400">Sources</span>
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {entity.sources.length}
            </div>
          </div>
          <div>
            <span className="text-gray-500 dark:text-slate-400">Connections</span>
            <div className="font-semibold text-gray-900 dark:text-slate-100">
              {entity.connections || 0}
            </div>
          </div>
        </div>
        
        {/* Tags */}
        {entity.tags && entity.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {entity.tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full dark:bg-blue-900/30 dark:text-blue-300"
              >
                {tag}
              </span>
            ))}
            {entity.tags.length > 3 && (
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full dark:bg-gray-800 dark:text-slate-400">
                +{entity.tags.length - 3} more
              </span>
            )}
          </div>
        )}
      </div>
    </Panel>
  );
}

export default EntityCard;
