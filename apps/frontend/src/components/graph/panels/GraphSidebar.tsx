import React from 'react';
import Panel from '@/components/layout/Panel';
import StatusPill, { Status } from '@/components/ui/StatusPill';

interface GraphData {
  nodes: Array<{ id: string; label: string; type?: string; properties?: any }>;
  edges: Array<{ id: string; source: string; target: string; type?: string; properties?: any }>;
}

interface GraphSidebarProps {
  graphData: GraphData;
  graphStatus?: Status;
  customQuery?: string;
  onQuerySelect?: (query: string) => void;
}

export default function GraphSidebar({ graphData, graphStatus, customQuery, onQuerySelect }: GraphSidebarProps) {
  return (
    <div className="space-y-6">
      
      {/* Quick Stats */}
      <Panel title="Graph Statistics">
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-gray-600 dark:text-slate-400">Loaded Nodes</span>
            <span className="font-medium text-gray-900 dark:text-slate-100">{graphData.nodes.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600 dark:text-slate-400">Loaded Edges</span>
            <span className="font-medium text-gray-900 dark:text-slate-100">{graphData.edges.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600 dark:text-slate-400">Graph Status</span>
            <StatusPill status={graphStatus || 'fail'} />
          </div>
        </div>
      </Panel>

      {/* Node Types */}
      {graphData.nodes.length > 0 && (
        <Panel title="Node Types">
          <div className="space-y-2">
            {Array.from(new Set(graphData.nodes.map(n => n.type || 'Unknown'))).map(type => {
              const count = graphData.nodes.filter(n => (n.type || 'Unknown') === type).length;
              return (
                <div key={type} className="flex items-center justify-between text-sm">
                  <span className="text-gray-700 dark:text-slate-300">{type}</span>
                  <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs">{count}</span>
                </div>
              );
            })}
          </div>
        </Panel>
      )}

      {/* Recent Queries */}
      <Panel title="Recent Queries">
        <div className="space-y-2 text-sm">
          {[customQuery].filter(Boolean).slice(0, 3).map((query, index) => (
            <button
              key={index}
              onClick={() => onQuerySelect?.(query)}
              className="w-full p-2 text-left text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded text-xs font-mono truncate"
            >
              {query}
            </button>
          ))}
          {!customQuery && (
            <div className="text-xs text-gray-500 dark:text-slate-500 italic">
              No recent queries
            </div>
          )}
        </div>
      </Panel>
    </div>
  );
}
