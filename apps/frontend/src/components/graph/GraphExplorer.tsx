// apps/frontend/src/components/graph/GraphExplorer.tsx
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { 
  Network, 
  Play, 
  Pause, 
  RotateCcw, 
  Save, 
  FolderOpen, 
  Settings, 
  Search,
  Maximize2,
  Download,
  Zap,
  Eye,
  EyeOff,
  Lock,
  Unlock
} from 'lucide-react';
import CytoscapeComponent from 'react-cytoscapejs';

interface Node {
  data: {
    id: string;
    label: string;
    type?: string;
    locked?: boolean;
  };
  position?: { x: number; y: number };
}

interface Edge {
  data: {
    id: string;
    source: string;
    target: string;
    label?: string;
    weight?: number;
  };
}

interface GraphData {
  nodes: Node[];
  edges: Edge[];
}

interface ViewConfig {
  layout: string;
  showLabels: boolean;
  nodeSize: number;
  edgeWidth: number;
  physics: boolean;
}

const GRAPH_LAYOUTS = [
  { value: 'cose', label: 'Force-Directed (COSE)' },
  { value: 'grid', label: 'Grid' },
  { value: 'circle', label: 'Circle' },
  { value: 'breadthfirst', label: 'Hierarchical' },
  { value: 'concentric', label: 'Concentric' }
];

const GRAPH_API_BASE = 'http://127.0.0.1:8002';
const VIEWS_API_BASE = 'http://127.0.0.1:8004';

export default function GraphExplorer() {
  const cyRef = useRef<any>(null);
  const [elements, setElements] = useState<(Node | Edge)[]>([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [seedNode, setSeedNode] = useState('P:alice');
  const [loading, setLoading] = useState(false);
  const [views, setViews] = useState<any[]>([]);
  const [viewName, setViewName] = useState('My Graph View');
  const [showSettings, setShowSettings] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [config, setConfig] = useState<ViewConfig>({
    layout: 'cose',
    showLabels: true,
    nodeSize: 30,
    edgeWidth: 2,
    physics: true
  });

  const [stats, setStats] = useState({
    nodes: 0,
    edges: 0,
    components: 0,
    density: 0
  });

  // Calculate graph statistics
  useEffect(() => {
    const nodes = elements.filter(el => !('source' in el.data));
    const edges = elements.filter(el => 'source' in el.data);
    
    setStats({
      nodes: nodes.length,
      edges: edges.length,
      components: 1, // Simplified calculation
      density: nodes.length > 1 ? (2 * edges.length) / (nodes.length * (nodes.length - 1)) : 0
    });
  }, [elements]);

  const expandGraph = async (nodeId: string, limit: number = 50) => {
    setLoading(true);
    try {
      const response = await fetch(`${GRAPH_API_BASE}/neighbors?node_id=${encodeURIComponent(nodeId)}&limit=${limit}`);
      if (!response.ok) throw new Error('Failed to fetch neighbors');
      
      const neighbors = await response.json();
      
      const newNodes = new Map<string, Node>();
      const newEdges: Edge[] = [];
      
      // Add existing elements to maps
      elements.forEach(el => {
        if (!('source' in el.data)) {
          newNodes.set(el.data.id, el as Node);
        }
      });
      
      // Process new data
      neighbors.forEach((edge: any) => {
        const sourceId = edge.from.id || edge.from.name;
        const targetId = edge.to.id || edge.to.name;
        
        if (!newNodes.has(sourceId)) {
          newNodes.set(sourceId, {
            data: { 
              id: sourceId, 
              label: edge.from.name || sourceId,
              type: edge.from.type || 'unknown'
            }
          });
        }
        
        if (!newNodes.has(targetId)) {
          newNodes.set(targetId, {
            data: { 
              id: targetId, 
              label: edge.to.name || targetId,
              type: edge.to.type || 'unknown'
            }
          });
        }
        
        newEdges.push({
          data: {
            id: `${sourceId}-${edge.rel}-${targetId}`,
            source: sourceId,
            target: targetId,
            label: edge.rel,
            weight: edge.weight || 1
          }
        });
      });
      
      setElements([...Array.from(newNodes.values()), ...newEdges]);
      
      // Apply layout after data loads
      setTimeout(() => applyLayout(), 100);
    } catch (error) {
      console.error('Failed to expand graph:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyLayout = () => {
    const cy = cyRef.current;
    if (!cy) return;
    
    cy.layout({
      name: config.layout,
      fit: true,
      padding: 50,
      animate: config.physics,
      animationDuration: 1000,
      randomize: false,
      // COSE-specific options
      nodeRepulsion: 10000,
      edgeElasticity: 100,
      nestingFactor: 5,
    }).run();
  };

  const toggleNodeLock = (nodeId: string) => {
    const cy = cyRef.current;
    if (!cy) return;
    
    const node = cy.getElementById(nodeId);
    if (node.locked()) {
      node.unlock();
    } else {
      node.lock();
    }
    
    // Update elements state
    setElements(prev => prev.map(el => {
      if (el.data.id === nodeId && !('source' in el.data)) {
        return { ...el, data: { ...el.data, locked: node.locked() } };
      }
      return el;
    }));
  };

  const saveView = async () => {
    const positions = getNodePositions();
    try {
      const response = await fetch(`${VIEWS_API_BASE}/views`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User': 'dev'
        },
        body: JSON.stringify({
          name: viewName,
          nodes: elements.filter(el => !('source' in el.data)).map(el => el.data),
          edges: elements.filter(el => 'source' in el.data).map(el => el.data),
          positions
        })
      });
      
      if (!response.ok) throw new Error('Failed to save view');
      
      const result = await response.json();
      alert(`View saved with ID: ${result.id}`);
      loadViewsList();
    } catch (error) {
      console.error('Failed to save view:', error);
      alert('Failed to save view');
    }
  };

  const loadViewsList = async () => {
    try {
      const response = await fetch(`${VIEWS_API_BASE}/views`, {
        headers: { 'X-User': 'dev' }
      });
      if (response.ok) {
        const viewsList = await response.json();
        setViews(viewsList);
      }
    } catch (error) {
      console.error('Failed to load views:', error);
    }
  };

  const loadView = async (viewId: number) => {
    try {
      const response = await fetch(`${VIEWS_API_BASE}/views/${viewId}`, {
        headers: { 'X-User': 'dev' }
      });
      
      if (!response.ok) throw new Error('Failed to load view');
      
      const view = await response.json();
      
      const nodes: Node[] = view.nodes.map((n: any) => ({ data: n }));
      const edges: Edge[] = view.edges.map((e: any) => ({ data: e }));
      
      setElements([...nodes, ...edges]);
      
      setTimeout(() => {
        applyPositions(view.positions || {});
      }, 100);
    } catch (error) {
      console.error('Failed to load view:', error);
      alert('Failed to load view');
    }
  };

  const getNodePositions = () => {
    const cy = cyRef.current;
    if (!cy) return {};
    
    const positions: Record<string, { x: number; y: number }> = {};
    cy.nodes().forEach((node: any) => {
      positions[node.id()] = node.position();
    });
    return positions;
  };

  const applyPositions = (positions: Record<string, { x: number; y: number }>) => {
    const cy = cyRef.current;
    if (!cy) return;
    
    Object.entries(positions).forEach(([id, pos]) => {
      const node = cy.getElementById(id);
      if (node.length > 0) {
        node.position(pos);
        node.lock();
      }
    });
  };

  const resetGraph = () => {
    setElements([]);
    setSelectedNode(null);
    expandGraph(seedNode);
  };

  const filteredElements = useMemo(() => {
    if (!searchQuery) return elements;
    
    return elements.filter(el => {
      if ('source' in el.data) return true; // Always show edges
      return el.data.label?.toLowerCase().includes(searchQuery.toLowerCase()) ||
             el.data.id.toLowerCase().includes(searchQuery.toLowerCase());
    });
  }, [elements, searchQuery]);

  const cytoscapeStylesheet = [
    {
      selector: 'node',
      style: {
        'background-color': '#0ea5e9',
        'label': config.showLabels ? 'data(label)' : '',
        'font-size': '12px',
        'font-weight': 'bold',
        'color': '#374151',
        'text-outline-width': '2px',
        'text-outline-color': '#ffffff',
        'width': config.nodeSize,
        'height': config.nodeSize,
        'border-width': '2px',
        'border-color': '#0284c7'
      }
    },
    {
      selector: 'node[type="Person"]',
      style: {
        'background-color': '#8b5cf6',
        'border-color': '#7c3aed'
      }
    },
    {
      selector: 'node[type="Organization"]',
      style: {
        'background-color': '#10b981',
        'border-color': '#059669'
      }
    },
    {
      selector: 'node:selected',
      style: {
        'background-color': '#f59e0b',
        'border-color': '#d97706',
        'border-width': '3px'
      }
    },
    {
      selector: 'node:locked',
      style: {
        'border-style': 'dashed',
        'border-width': '3px'
      }
    },
    {
      selector: 'edge',
      style: {
        'curve-style': 'bezier',
        'target-arrow-shape': 'triangle',
        'target-arrow-color': '#6b7280',
        'line-color': '#6b7280',
        'width': config.edgeWidth,
        'label': config.showLabels ? 'data(label)' : '',
        'font-size': '10px',
        'color': '#4b5563',
        'text-outline-width': '1px',
        'text-outline-color': '#ffffff'
      }
    },
    {
      selector: 'edge:selected',
      style: {
        'line-color': '#f59e0b',
        'target-arrow-color': '#f59e0b',
        'width': config.edgeWidth + 1
      }
    }
  ];

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      
      {/* Toolbar */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          
          {/* Left Controls */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={seedNode}
                onChange={(e) => setSeedNode(e.target.value)}
                placeholder="Start node (e.g., P:alice)"
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
              <button
                onClick={() => expandGraph(seedNode)}
                disabled={loading}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center gap-2"
              >
                {loading ? <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" /> : <Play size={16} />}
                {loading ? 'Loading...' : 'Expand'}
              </button>
            </div>
            
            <div className="h-6 w-px bg-gray-200" />
            
            <div className="flex items-center gap-2">
              <button
                onClick={applyLayout}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                title="Apply Layout"
              >
                <Zap size={16} />
              </button>
              <button
                onClick={resetGraph}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                title="Reset Graph"
              >
                <RotateCcw size={16} />
              </button>
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                title="Settings"
              >
                <Settings size={16} />
              </button>
            </div>
          </div>

          {/* Center Search */}
          <div className="flex-1 max-w-md mx-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search nodes..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>

          {/* Right Controls */}
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={viewName}
              onChange={(e) => setViewName(e.target.value)}
              placeholder="View name"
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm w-32"
            />
            <button
              onClick={saveView}
              className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
            >
              <Save size={16} />
              Save
            </button>
            <button
              onClick={loadViewsList}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
              title="Load Views"
            >
              <FolderOpen size={16} />
            </button>
          </div>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        
        {/* Settings Panel */}
        {showSettings && (
          <div className="w-80 bg-white border-r border-gray-200 p-6 overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Graph Settings</h3>
            
            {/* Layout */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Layout</label>
              <select
                value={config.layout}
                onChange={(e) => setConfig(prev => ({ ...prev, layout: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                {GRAPH_LAYOUTS.map(layout => (
                  <option key={layout.value} value={layout.value}>{layout.label}</option>
                ))}
              </select>
            </div>
            
            {/* Visual Settings */}
            <div className="space-y-4">
              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={config.showLabels}
                    onChange={(e) => setConfig(prev => ({ ...prev, showLabels: e.target.checked }))}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Show Labels</span>
                </label>
              </div>
              
              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={config.physics}
                    onChange={(e) => setConfig(prev => ({ ...prev, physics: e.target.checked }))}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Animation</span>
                </label>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Node Size ({config.nodeSize}px)
                </label>
                <input
                  type="range"
                  min="10"
                  max="80"
                  value={config.nodeSize}
                  onChange={(e) => setConfig(prev => ({ ...prev, nodeSize: parseInt(e.target.value) }))}
                  className="w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Edge Width ({config.edgeWidth}px)
                </label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={config.edgeWidth}
                  onChange={(e) => setConfig(prev => ({ ...prev, edgeWidth: parseInt(e.target.value) }))}
                  className="w-full"
                />
              </div>
            </div>
            
            {/* Statistics */}
            <div className="mt-8 p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Graph Statistics</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Nodes:</span>
                  <span className="font-medium">{stats.nodes}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Edges:</span>
                  <span className="font-medium">{stats.edges}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Density:</span>
                  <span className="font-medium">{(stats.density * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>

            {/* Views */}
            <div className="mt-8">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Saved Views</h4>
              <div className="space-y-2">
                {views.map(view => (
                  <button
                    key={view.id}
                    onClick={() => loadView(view.id)}
                    className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded border"
                  >
                    {view.name} #{view.id}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Main Graph Area */}
        <div className="flex-1 relative bg-white">
          <CytoscapeComponent
            cy={(cy: any) => {
              cyRef.current = cy;
              cy.on('tap', 'node', (evt: any) => {
                const nodeId = evt.target.id();
                setSelectedNode(nodeId);
              });
              cy.on('dblclick', 'node', (evt: any) => {
                toggleNodeLock(evt.target.id());
              });
            }}
            elements={filteredElements}
            style={{ width: '100%', height: '100%' }}
            stylesheet={cytoscapeStylesheet}
            layout={{ name: 'preset' }} // Use preset to maintain positions
          />
          
          {/* Graph Controls Overlay */}
          <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 p-2 flex flex-col gap-2">
            <button
              onClick={() => cyRef.current?.fit()}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
              title="Fit to View"
            >
              <Maximize2 size={16} />
            </button>
            <button
              onClick={() => {
                const png = cyRef.current?.png({ scale: 2 });
                if (png) {
                  const link = document.createElement('a');
                  link.download = 'graph.png';
                  link.href = png;
                  link.click();
                }
              }}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
              title="Export PNG"
            >
              <Download size={16} />
            </button>
          </div>

          {/* Node Info Panel */}
          {selectedNode && (
            <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg border border-gray-200 p-4 min-w-64">
              <h4 className="font-medium text-gray-900 mb-2">Node Information</h4>
              <div className="text-sm space-y-1">
                <div><span className="text-gray-600">ID:</span> <span className="font-mono">{selectedNode}</span></div>
                <div><span className="text-gray-600">Type:</span> <span>Entity</span></div>
                <div className="pt-2 flex gap-2">
                  <button
                    onClick={() => expandGraph(selectedNode)}
                    className="text-xs bg-primary-50 text-primary-700 px-2 py-1 rounded hover:bg-primary-100"
                  >
                    Expand
                  </button>
                  <button
                    onClick={() => toggleNodeLock(selectedNode)}
                    className="text-xs bg-gray-50 text-gray-700 px-2 py-1 rounded hover:bg-gray-100 flex items-center gap-1"
                  >
                    {elements.find(el => el.data.id === selectedNode && 'locked' in el.data)?.data.locked ? (
                      <>
                        <Unlock size={12} />
                        Unlock
                      </>
                    ) : (
                      <>
                        <Lock size={12} />
                        Lock
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
