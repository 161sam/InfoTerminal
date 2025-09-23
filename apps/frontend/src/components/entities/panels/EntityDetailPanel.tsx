// Entity detail panel for viewing and editing entity information
import { useState } from 'react';
import { ExternalLink, X } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import { Entity } from '@/lib/entities/entity-config';

interface EntityDetailPanelProps {
  entity: Entity;
  onClose: () => void;
  onUpdate: (entity: Entity) => void;
}

export function EntityDetailPanel({ entity, onClose, onUpdate }: EntityDetailPanelProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedEntity, setEditedEntity] = useState(entity);

  const handleSave = () => {
    onUpdate(editedEntity);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedEntity(entity);
  };

  const updateField = (field: keyof Entity, value: any) => {
    setEditedEntity(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Panel>
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            Entity Details
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 p-1 rounded"
            aria-label="Close detail panel"
          >
            <X size={20} />
          </button>
        </div>
        
        <div className="space-y-4">
          {/* Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
              Name
            </label>
            {isEditing ? (
              <input
                type="text"
                value={editedEntity.name}
                onChange={(e) => updateField('name', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            ) : (
              <p className="text-gray-900 dark:text-slate-100 font-mono">
                {entity.name}
              </p>
            )}
          </div>
          
          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
              Description
            </label>
            {isEditing ? (
              <textarea
                value={editedEntity.description || ''}
                onChange={(e) => updateField('description', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                rows={3}
                placeholder="Enter entity description..."
              />
            ) : (
              <p className="text-gray-900 dark:text-slate-100">
                {entity.description || 'No description provided'}
              </p>
            )}
          </div>
          
          {/* Basic info grid */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500 dark:text-slate-400">Type</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {entity.type}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Verified</span>
              <div className={entity.verified ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'}>
                {entity.verified ? 'Verified' : 'Pending Verification'}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">First Seen</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {new Date(entity.firstSeen).toLocaleDateString()}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Last Seen</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {new Date(entity.lastSeen).toLocaleDateString()}
              </div>
            </div>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-2 gap-4 text-sm">
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

          {/* Risk Score */}
          {entity.riskScore !== undefined && (
            <div>
              <span className="text-gray-500 dark:text-slate-400">Risk Score</span>
              <div className="flex items-center gap-2 mt-1">
                <div className="font-semibold text-gray-900 dark:text-slate-100">
                  {entity.riskScore}/10
                </div>
                <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      entity.riskScore >= 7 ? 'bg-red-500' :
                      entity.riskScore >= 4 ? 'bg-yellow-500' :
                      'bg-green-500'
                    }`}
                    style={{ width: `${(entity.riskScore / 10) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          )}
          
          {/* Aliases */}
          {entity.aliases && entity.aliases.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                Aliases
              </label>
              <div className="flex flex-wrap gap-2">
                {entity.aliases.map((alias, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full dark:bg-gray-800 dark:text-slate-300"
                  >
                    {alias}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Tags */}
          {entity.tags && entity.tags.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                Tags
              </label>
              <div className="flex flex-wrap gap-2">
                {entity.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full dark:bg-blue-900/30 dark:text-blue-300"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Sources */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
              Sources ({entity.sources.length})
            </label>
            <div className="space-y-1 max-h-32 overflow-y-auto">
              {entity.sources.map((source, index) => (
                <div
                  key={index}
                  className="px-2 py-1 text-xs bg-gray-50 text-gray-700 rounded dark:bg-gray-800 dark:text-slate-300 font-mono"
                >
                  {source}
                </div>
              ))}
            </div>
          </div>
          
          {/* Action buttons */}
          <div className="flex gap-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            {isEditing ? (
              <>
                <button
                  onClick={handleSave}
                  className="flex-1 px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Save Changes
                </button>
                <button
                  onClick={handleCancel}
                  className="flex-1 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700 transition-colors"
                >
                  Cancel
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex-1 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700 transition-colors"
                >
                  Edit Entity
                </button>
                <button
                  onClick={() => window.open(`/graphx?focus=${encodeURIComponent(entity.name)}`, '_blank')}
                  className="flex-1 px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:hover:bg-blue-900/50 transition-colors inline-flex items-center justify-center gap-2"
                >
                  <ExternalLink size={14} />
                  View in Graph
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </Panel>
  );
}

export default EntityDetailPanel;
