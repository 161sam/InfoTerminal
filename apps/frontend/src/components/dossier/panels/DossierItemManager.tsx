// Dossier item manager panel
import { useState } from 'react';
import { Plus, Trash2, Tag, Upload, FileText } from 'lucide-react';
import { 
  DossierItem, 
  getItemTypeColor, 
  getItemTypeLabel,
  getConfidenceColor,
  formatConfidence,
  validateDossierItems
} from '@/lib/dossier/dossier-config';

interface DossierItemManagerProps {
  items: DossierItem[];
  onAddItem: (item: Omit<DossierItem, 'id'>) => void;
  onRemoveItem: (id: string) => void;
  onUpdateItem: (id: string, updates: Partial<DossierItem>) => void;
}

export function DossierItemManager({
  items,
  onAddItem,
  onRemoveItem,
  onUpdateItem
}: DossierItemManagerProps) {
  const [newItemValue, setNewItemValue] = useState('');
  const [newItemType, setNewItemType] = useState<DossierItem['type']>('document');
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');

  const validation = validateDossierItems(items);
  
  const filteredItems = items.filter(item => {
    const matchesSearch = item.value.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.metadata?.title?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === 'all' || item.type === typeFilter;
    return matchesSearch && matchesType;
  });

  const handleAddItem = () => {
    if (!newItemValue.trim()) return;
    
    const newItem: Omit<DossierItem, 'id'> = {
      type: newItemType,
      value: newItemValue.trim(),
      metadata: {
        title: newItemValue.trim(),
        lastSeen: new Date().toISOString().split('T')[0]
      }
    };
    
    onAddItem(newItem);
    setNewItemValue('');
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    Array.from(files).forEach(file => {
      const item: Omit<DossierItem, 'id'> = {
        type: 'document',
        value: file.name,
        metadata: {
          title: file.name,
          description: `Uploaded file (${(file.size / 1024).toFixed(1)} KB)`,
          lastSeen: new Date().toISOString().split('T')[0]
        }
      };
      onAddItem(item);
    });

    // Reset file input
    e.target.value = '';
  };

  const getItemsByType = () => {
    const types = ['document', 'entity', 'node', 'edge'] as const;
    return types.map(type => ({
      type,
      count: items.filter(item => item.type === type).length,
      label: getItemTypeLabel(type)
    }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Dossier Items
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {items.length} items • {filteredItems.length} shown
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <label className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 cursor-pointer">
            <Upload size={16} />
            Upload Files
            <input
              type="file"
              multiple
              onChange={handleFileUpload}
              className="hidden"
              accept="*/*"
            />
          </label>
        </div>
      </div>

      {/* Type distribution */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {getItemsByType().map(({ type, count, label }) => (
          <div
            key={type}
            className={`p-3 rounded-lg border text-center ${getItemTypeColor(type)}`}
          >
            <div className="font-semibold text-lg">{count}</div>
            <div className="text-sm">{label}</div>
          </div>
        ))}
      </div>

      {/* Add new item */}
      <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800">
        <h4 className="font-medium text-gray-900 dark:text-white mb-3">
          Add New Item
        </h4>
        <div className="flex gap-3">
          <select
            value={newItemType}
            onChange={(e) => setNewItemType(e.target.value as DossierItem['type'])}
            className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
          >
            <option value="document">Document</option>
            <option value="entity">Entity</option>
            <option value="node">Node</option>
            <option value="edge">Relationship</option>
          </select>
          
          <input
            type="text"
            value={newItemValue}
            onChange={(e) => setNewItemValue(e.target.value)}
            placeholder={`Enter ${getItemTypeLabel(newItemType).toLowerCase()} name...`}
            className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleAddItem();
              }
            }}
          />
          
          <button
            onClick={handleAddItem}
            disabled={!newItemValue.trim()}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>

      {/* Search and filters */}
      <div className="flex gap-3">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search items..."
          className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
        />
        
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
        >
          <option value="all">All Types</option>
          <option value="document">Documents</option>
          <option value="entity">Entities</option>
          <option value="node">Nodes</option>
          <option value="edge">Relationships</option>
        </select>
      </div>

      {/* Validation messages */}
      {!validation.isValid && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900/30 rounded-lg">
          <div className="text-sm text-red-800 dark:text-red-300">
            <strong>Validation errors:</strong>
            <ul className="mt-1 ml-4 list-disc">
              {validation.errors.map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Items list */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {filteredItems.length === 0 ? (
          <div className="text-center py-8">
            <FileText size={32} className="mx-auto text-gray-400 mb-2" />
            <p className="text-gray-500 dark:text-gray-400">
              {searchTerm || typeFilter !== 'all' ? 'No items match your search' : 'No items added yet'}
            </p>
          </div>
        ) : (
          filteredItems.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              onRemove={() => onRemoveItem(item.id)}
              onUpdate={(updates) => onUpdateItem(item.id, updates)}
            />
          ))
        )}
      </div>
    </div>
  );
}

interface ItemCardProps {
  item: DossierItem;
  onRemove: () => void;
  onUpdate: (updates: Partial<DossierItem>) => void;
}

function ItemCard({ item, onRemove, onUpdate }: ItemCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(item.value);

  const handleSave = () => {
    if (editValue.trim() !== item.value) {
      onUpdate({ 
        value: editValue.trim(),
        metadata: {
          ...item.metadata,
          title: editValue.trim()
        }
      });
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditValue(item.value);
    setIsEditing(false);
  };

  return (
    <div className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800">
      <span className={`px-2 py-1 text-xs rounded-full ${getItemTypeColor(item.type)}`}>
        {getItemTypeLabel(item.type)}
      </span>
      
      <div className="flex-1 min-w-0">
        {isEditing ? (
          <div className="flex gap-2">
            <input
              type="text"
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              className="flex-1 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded focus:ring-1 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleSave();
                if (e.key === 'Escape') handleCancel();
              }}
              autoFocus
            />
            <button
              onClick={handleSave}
              className="px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="px-2 py-1 text-xs bg-gray-400 text-white rounded hover:bg-gray-500"
            >
              Cancel
            </button>
          </div>
        ) : (
          <div>
            <div 
              className="font-medium text-gray-900 dark:text-white text-sm cursor-pointer hover:text-primary-600 dark:hover:text-primary-400"
              onClick={() => setIsEditing(true)}
            >
              {item.value}
            </div>
            {item.metadata?.description && (
              <div className="text-xs text-gray-500 dark:text-gray-400">
                {item.metadata.description}
              </div>
            )}
            <div className="flex items-center gap-3 text-xs text-gray-400 dark:text-gray-500 mt-1">
              {item.metadata?.lastSeen && (
                <span>Last seen: {item.metadata.lastSeen}</span>
              )}
              {item.metadata?.confidence && (
                <span className={getConfidenceColor(item.metadata.confidence)}>
                  Confidence: {formatConfidence(item.metadata.confidence)}
                </span>
              )}
            </div>
          </div>
        )}
      </div>
      
      <button
        onClick={onRemove}
        className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 rounded"
        title="Remove item"
      >
        <Trash2 size={16} />
      </button>
    </div>
  );
}

export default DossierItemManager;
