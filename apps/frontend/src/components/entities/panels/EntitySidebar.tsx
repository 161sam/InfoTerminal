// Entity sidebar with type distribution and risk levels
import { User } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import { 
  Entity, 
  EntityFilter, 
  ENTITY_TYPE_ICONS, 
  RISK_LEVELS 
} from '@/lib/entities/entity-config';

interface EntitySidebarProps {
  entities: Entity[];
  filters: EntityFilter;
  onFilterChange: (key: keyof EntityFilter, value: string) => void;
}

export function EntitySidebar({ entities, filters, onFilterChange }: EntitySidebarProps) {
  // Calculate entity type distribution
  const typeDistribution = entities.reduce((acc, entity) => {
    acc[entity.type] = (acc[entity.type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Calculate risk level distribution
  const riskDistribution = RISK_LEVELS.filter(level => level.value !== 'all').map((level) => {
    const count = entities.filter(e => {
      const risk = e.riskScore || 0;
      switch (level.value) {
        case 'low': return risk <= 3;
        case 'medium': return risk >= 4 && risk <= 6;
        case 'high': return risk >= 7;
        default: return false;
      }
    }).length;
    return { ...level, count };
  });

  const getRiskBarColor = (value: string) => {
    switch (value) {
      case 'low': return 'bg-green-500';
      case 'medium': return 'bg-yellow-500';
      case 'high': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getTotalEntities = () => entities.length;

  return (
    <div className="space-y-6">
      
      {/* Entity Type Distribution */}
      <Panel title="Entity Types">
        <div className="space-y-3">
          {Object.entries(typeDistribution).map(([type, count]) => {
            const Icon = ENTITY_TYPE_ICONS[type as keyof typeof ENTITY_TYPE_ICONS] || User;
            const isActive = filters.type === type;
            
            return (
              <button
                key={type}
                onClick={() => onFilterChange('type', type === filters.type ? 'all' : type)}
                className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon size={18} />
                  <span className="font-medium">{type}</span>
                </div>
                <span className="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded-full">
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </Panel>

      {/* Risk Distribution */}
      <Panel title="Risk Levels">
        <div className="space-y-3">
          {riskDistribution.map((level) => {
            const percentage = getTotalEntities() > 0 ? (level.count / getTotalEntities()) * 100 : 0;
            const isActive = filters.riskLevel === level.value;
            
            return (
              <button
                key={level.value}
                onClick={() => onFilterChange('riskLevel', level.value === filters.riskLevel ? 'all' : level.value)}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">{level.label}</span>
                  <span className="text-sm text-gray-500 dark:text-slate-400">
                    {level.count}
                  </span>
                </div>
                
                {/* Risk level progress bar */}
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${getRiskBarColor(level.value)}`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
                
                <div className="text-xs text-gray-500 dark:text-slate-400 mt-1">
                  {percentage.toFixed(1)}% of entities
                </div>
              </button>
            );
          })}
        </div>
      </Panel>

      {/* Quick Stats */}
      <Panel title="Quick Stats">
        <div className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-slate-400">Total Entities:</span>
            <span className="font-medium">{getTotalEntities()}</span>
          </div>
          
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-slate-400">Verified:</span>
            <span className="font-medium text-green-600 dark:text-green-400">
              {entities.filter(e => e.verified).length}
            </span>
          </div>
          
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-slate-400">High Risk:</span>
            <span className="font-medium text-red-600 dark:text-red-400">
              {entities.filter(e => (e.riskScore || 0) >= 7).length}
            </span>
          </div>
          
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-slate-400">Total Connections:</span>
            <span className="font-medium">
              {entities.reduce((sum, e) => sum + (e.connections || 0), 0)}
            </span>
          </div>
        </div>
      </Panel>
    </div>
  );
}

export default EntitySidebar;
