// Workflow runs table component
import React from 'react';
import { Play, CheckCircle, XCircle, Clock, AlertCircle, Download, ExternalLink } from 'lucide-react';
import { useWorkflowRuns } from '../../hooks/analytics';
import { AnalyticsFilters, WorkflowRun } from './types';

interface WorkflowRunsTableProps {
  filters: AnalyticsFilters;
  className?: string;
}

export function WorkflowRunsTable({ filters, className = '' }: WorkflowRunsTableProps) {
  const { data, loading, error, refresh } = useWorkflowRuns(filters);

  if (loading) {
    return (
      <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}>
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400 mb-4">
          <AlertCircle size={20} />
          <span className="text-sm">Workflow service unavailable. Showing empty state.</span>
        </div>
      </div>
    );
  }

  const getStatusIcon = (status: WorkflowRun['status']) => {
    switch (status) {
      case 'running': return <Play size={16} className="text-blue-500 animate-pulse" />;
      case 'completed': return <CheckCircle size={16} className="text-green-500" />;
      case 'failed': return <XCircle size={16} className="text-red-500" />;
      case 'cancelled': return <AlertCircle size={16} className="text-yellow-500" />;
      default: return <Clock size={16} className="text-gray-500" />;
    }
  };

  const getStatusColor = (status: WorkflowRun['status']) => {
    switch (status) {
      case 'running': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      case 'failed': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'cancelled': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300';
    }
  };

  const formatDuration = (milliseconds?: number) => {
    if (!milliseconds) return '-';
    
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
  };

  const exportWorkflowData = () => {
    if (data.length === 0) return;
    
    const csvData = [
      ['ID', 'Name', 'Type', 'Status', 'Start Time', 'Duration', 'Entities', 'Claims', 'Input Query'],
      ...data.map(run => [
        run.id,
        run.name,
        run.type,
        run.status,
        run.startTime,
        formatDuration(run.duration),
        run.entities.length.toString(),
        run.claims.length.toString(),
        run.input.query || ''
      ])
    ];

    const csv = csvData.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `workflow-runs-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Play size={20} className="text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Workflow Runs</h3>
        </div>
        
        <div className="flex items-center gap-2">
          {data.length > 0 && (
            <button
              onClick={exportWorkflowData}
              className="inline-flex items-center gap-1 px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
            >
              <Download size={14} />
              Export CSV
            </button>
          )}
          <button
            onClick={refresh}
            className="inline-flex items-center gap-1 px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-200 dark:hover:bg-blue-900/50 text-blue-700 dark:text-blue-300 rounded transition-colors"
          >
            <Play size={14} />
            Refresh
          </button>
        </div>
      </div>

      {data.length === 0 ? (
        <div className="text-center py-12">
          <Play size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            No workflow runs available for the selected filters.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Stats Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {['running', 'completed', 'failed', 'cancelled'].map(status => {
              const count = data.filter(run => run.status === status).length;
              return (
                <div key={status} className={`p-3 rounded-lg ${getStatusColor(status as WorkflowRun['status'])}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-lg font-bold">{count}</div>
                      <div className="text-xs capitalize">{status}</div>
                    </div>
                    {getStatusIcon(status as WorkflowRun['status'])}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Runs Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left p-3 font-medium text-gray-900 dark:text-gray-100">Workflow</th>
                  <th className="text-left p-3 font-medium text-gray-900 dark:text-gray-100">Status</th>
                  <th className="text-left p-3 font-medium text-gray-900 dark:text-gray-100">Started</th>
                  <th className="text-left p-3 font-medium text-gray-900 dark:text-gray-100">Duration</th>
                  <th className="text-right p-3 font-medium text-gray-900 dark:text-gray-100">Results</th>
                  <th className="text-center p-3 font-medium text-gray-900 dark:text-gray-100">Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.map((run) => {
                  const startDateTime = formatDateTime(run.startTime);
                  const endDateTime = run.endTime ? formatDateTime(run.endTime) : null;
                  
                  return (
                    <tr key={run.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50">
                      <td className="p-3">
                        <div>
                          <div className="font-medium text-gray-900 dark:text-gray-100">
                            {run.name}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            {run.type} • {run.id}
                          </div>
                          {run.input.query && (
                            <div className="text-xs text-gray-600 dark:text-gray-400 mt-1 max-w-xs truncate">
                              Query: {run.input.query}
                            </div>
                          )}
                        </div>
                      </td>
                      
                      <td className="p-3">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(run.status)}
                          <span className={`inline-block px-2 py-1 text-xs rounded ${getStatusColor(run.status)}`}>
                            {run.status}
                          </span>
                        </div>
                        {run.error && (
                          <div className="text-xs text-red-600 dark:text-red-400 mt-1 max-w-xs truncate">
                            {run.error}
                          </div>
                        )}
                      </td>
                      
                      <td className="p-3">
                        <div className="text-sm text-gray-900 dark:text-gray-100">
                          {startDateTime.date}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {startDateTime.time}
                        </div>
                      </td>
                      
                      <td className="p-3">
                        <div className="text-sm text-gray-900 dark:text-gray-100">
                          {formatDuration(run.duration)}
                        </div>
                        {endDateTime && (
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            Ended {endDateTime.time}
                          </div>
                        )}
                      </td>
                      
                      <td className="p-3 text-right">
                        {run.output ? (
                          <div className="space-y-1">
                            <div className="text-sm text-gray-900 dark:text-gray-100">
                              {run.entities.length} entities
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              {run.output.relationships} relations • {run.output.documents} docs
                            </div>
                            {run.output.confidence && (
                              <div className="text-xs">
                                <span className={`${
                                  run.output.confidence >= 0.8 ? 'text-green-600 dark:text-green-400' :
                                  run.output.confidence >= 0.6 ? 'text-yellow-600 dark:text-yellow-400' :
                                  'text-red-600 dark:text-red-400'
                                }`}>
                                  {Math.round(run.output.confidence * 100)}% confidence
                                </span>
                              </div>
                            )}
                          </div>
                        ) : (
                          <div className="text-xs text-gray-500 dark:text-gray-400">-</div>
                        )}
                      </td>
                      
                      <td className="p-3 text-center">
                        <div className="flex items-center justify-center gap-1">
                          {run.output?.artifacts && run.output.artifacts.length > 0 && (
                            <button className="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">
                              <Download size={14} />
                            </button>
                          )}
                          <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                            <ExternalLink size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Summary Stats */}
          {data.length > 0 && (
            <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {data.reduce((sum, run) => sum + run.entities.length, 0)}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Total Entities</div>
                </div>
                
                <div>
                  <div className="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {data.reduce((sum, run) => sum + run.claims.length, 0)}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Total Claims</div>
                </div>
                
                <div>
                  <div className="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {Math.round(data.reduce((sum, run) => sum + (run.duration || 0), 0) / data.length / 1000)}s
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Avg Duration</div>
                </div>
                
                <div>
                  <div className="text-lg font-bold text-green-600 dark:text-green-400">
                    {Math.round((data.filter(run => run.status === 'completed').length / data.length) * 100)}%
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Success Rate</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default WorkflowRunsTable;
