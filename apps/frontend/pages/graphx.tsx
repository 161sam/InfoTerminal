import React, { useState, useEffect } from "react";
import { 
  Network, 
  Search, 
  Play, 
  Download, 
  Settings, 
  RefreshCw, 
  Users, 
  Building, 
  MapPin,
  AlertTriangle,
  CheckCircle,
  Loader,
  ArrowRight,
  Database,
  Eye,
  Code2,
  BarChart3
} from 'lucide-react';
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/Button";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import GraphViewerCytoscape from "@/components/GraphViewerCytoscape";
import config from "@/lib/config";
import { getEgo, loadPeople, getShortestPath, exportDossier } from "@/lib/api";
import { toast } from "@/components/ui/toast";
import DossierButton from "@/components/DossierButton";
import AnalysisPanel from "@/components/graph/AnalysisPanel";
import dynamic from "next/dynamic";
const MapPanel = dynamic(() => import("@/components/MapPanel"), { ssr: false });

type GraphTab = 'explorer' | 'query' | 'analysis' | 'tools';

interface NodeData {
  id: string;
  label: string;
  type?: string;
  properties?: any;
}

interface EdgeData {
  id: string;
  source: string;
  target: string;
  type?: string;
  properties?: any;
}

interface GraphData {
  nodes: NodeData[];
  edges: EdgeData[];
}

const ENTITY_EXAMPLES = [
  { label: "Person", key: "id", value: "alice", description: "Sample person node" },
  { label: "Organization", key: "name", value: "ACME Corp", description: "Company entity" },
  { label: "Location", key: "name", value: "London", description: "Geographic location" }
];

const SAMPLE_QUERIES = [
  { 
    name: "All Nodes Overview", 
    query: "MATCH (n) RETURN n LIMIT 25",
    description: "Get a general overview of your graph"
  },
  { 
    name: "Person Connections", 
    query: "MATCH (p:Person)-[r]-(n) RETURN p, r, n LIMIT 20",
    description: "Find connections between people"
  },
  { 
    name: "Organizations Network", 
    query: "MATCH (o:Organization)-[r]-(n) RETURN o, r, n LIMIT 15",
    description: "Explore organizational relationships"
  },
  { 
    name: "Central Nodes", 
    query: "MATCH (n)-[r]-() RETURN n, COUNT(r) as degree ORDER BY degree DESC LIMIT 10",
    description: "Find the most connected nodes"
  }
];

async function pingService(url?: string): Promise<Status> {
  if (!url) return "fail";
  try {
    const response = await fetch(url + "/healthz", { 
      signal: AbortSignal.timeout(5000) 
    });
    return response.ok ? "ok" : "fail";
  } catch {
    return "fail";
  }
}

function DevToolsPanel() {
  if (process.env.NODE_ENV === "production") return null;

  const seedDemo = async () => {
    const rows = [
      { id: "alice", name: "Alice", knows_id: "bob" },
      { id: "bob", name: "Bob", knows_id: "carol" },
      { id: "carol", name: "Carol", knows_id: null },
    ];
    
    try {
      const { inserted } = await loadPeople(rows);
      toast(`Demo data seeded: ${inserted} nodes inserted`, { variant: 'success' });
    } catch (e: any) {
      toast(`Seed failed: ${e?.message || e}`, { variant: 'error' });
    }
  };

  const testEgo = async () => {
    try {
      const { data } = await getEgo({ 
        label: "Person", 
        key: "id", 
        value: "alice", 
        depth: 2, 
        limit: 50 
      });
      const nodes = data?.nodes?.length ?? 0;
      const edges = data?.relationships?.length ?? 0;
      toast(`Ego query successful: ${nodes} nodes, ${edges} edges`, { variant: 'success' });
    } catch (e: any) {
      toast(`Ego query failed: ${e?.message || e}`, { variant: 'error' });
    }
  };

  return (
    <Panel title="Developer Tools" className="border-2 border-dashed border-orange-200 dark:border-orange-800">
      <div className="flex flex-wrap gap-2">
        <Button size="sm" variant="outline" onClick={seedDemo}>
          <Users size={14} className="mr-2" />
          Seed Demo Data
        </Button>
        <Button size="sm" variant="outline" onClick={testEgo}>
          <Network size={14} className="mr-2" />
          Test Ego Query
        </Button>
      </div>
    </Panel>
  );
}

export default function GraphExplorerPage() {
  const [activeTab, setActiveTab] = useState<GraphTab>('explorer');
  const [graphStatus, setGraphStatus] = useState<Status>();
  const [viewsStatus, setViewsStatus] = useState<Status>();
  
  // Query tab state
  const [customQuery, setCustomQuery] = useState("MATCH (n) RETURN n LIMIT 10");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryStatus, setQueryStatus] = useState<Status>();
  
  // Explorer tab state
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedEntityType, setSelectedEntityType] = useState("Person");
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], edges: [] });
  const [isLoadingGraph, setIsLoadingGraph] = useState(false);
  
  // Path finding state
  const [pathConfig, setPathConfig] = useState({
    srcLabel: "Person",
    srcKey: "id", 
    srcValue: "",
    dstLabel: "Person",
    dstKey: "id",
    dstValue: "",
    maxLength: 4,
    directed: false
  });

  // UI state
  const [showMap, setShowMap] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(false);

  useEffect(() => {
    checkServices();
  }, []);

  const checkServices = async () => {
    setGraphStatus("loading");
    setViewsStatus("loading");
    
    const [graphHealth, viewsHealth] = await Promise.all([
      pingService(config?.GRAPH_API),
      pingService(config?.VIEWS_API)
    ]);
    
    setGraphStatus(graphHealth);
    setViewsStatus(viewsHealth);
  };

  const runCustomQuery = async () => {
    setQueryStatus("loading");
    const base = config?.GRAPH_API;
    if (!base) {
      setQueryStatus("fail");
      setQueryResult({ error: "Graph API not configured" });
      return;
    }

    try {
      let response = await fetch(`${base}/query`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query: customQuery }),
      });

      if (response.status === 404) {
        response = await fetch(`${base}/nodes?limit=25`);
      }

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const result = await response.json();
      setQueryResult(result);
      setQueryStatus("ok");
    } catch (e: any) {
      setQueryStatus("fail");
      setQueryResult({ error: e.message || "Query failed" });
    }
  };

  const loadEntityNetwork = async (entityType: string, searchValue?: string) => {
    setIsLoadingGraph(true);
    try {
      const { data } = await getEgo({ 
        label: entityType, 
        key: searchValue ? "name" : "id", 
        value: searchValue || "alice", 
        depth: 2, 
        limit: 50 
      });

      const nodes = (data.nodes || []).map((n: any) => ({
        id: String(n.id),
        label: n.properties?.name || String(n.id),
        type: n.labels?.[0] || 'Unknown'
      }));

      const edges = (data.relationships || []).map((r: any) => ({
        id: String(r.id),
        source: String(r.start),
        target: String(r.end),
        type: r.type
      }));

      setGraphData({ nodes, edges });
      toast(`Loaded ${nodes.length} nodes and ${edges.length} edges`, { variant: 'success' });
    } catch (e: any) {
      toast(`Failed to load network: ${e?.message}`, { variant: 'error' });
    } finally {
      setIsLoadingGraph(false);
    }
  };

  const findShortestPath = async () => {
    if (!pathConfig.srcValue || !pathConfig.dstValue) {
      toast("Please enter both source and destination values", { variant: 'error' });
      return;
    }

    setIsLoadingGraph(true);
    try {
      const { data } = await getShortestPath(pathConfig);
      
      const nodes = (data.nodes || []).map((n: any) => ({
        id: String(n.id),
        label: n.properties?.name || String(n.id),
        type: n.labels?.[0] || 'Unknown'
      }));

      const edges = (data.relationships || []).map((r: any) => ({
        id: String(r.id),
        source: String(r.start),
        target: String(r.end),
        type: r.type
      }));

      setGraphData({ nodes, edges });
      
      if (nodes.length === 0) {
        toast("No path found between the specified nodes", { variant: 'error' });
      } else {
        toast(`Found path with ${nodes.length} nodes`, { variant: 'success' });
      }
    } catch (e: any) {
      toast(`Path finding failed: ${e?.message}`, { variant: 'error' });
    } finally {
      setIsLoadingGraph(false);
    }
  };

  const TabButton = ({ id, label, icon: Icon }: { id: GraphTab; label: string; icon: React.ComponentType<any> }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`inline-flex items-center gap-2 px-4 py-2 text-sm rounded-lg transition-colors ${
        activeTab === id
          ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
          : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200 hover:bg-gray-100 dark:hover:bg-gray-800'
      }`}
    >
      <Icon size={16} />
      {label}
    </button>
  );

  return (
    <DashboardLayout title="Graph Explorer" subtitle="Visualize and analyze your knowledge graph">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Service Status Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Database size={20} className="text-gray-500" />
              <span className="text-sm font-medium">Graph Database</span>
              {graphStatus && <StatusPill status={graphStatus} />}
            </div>
            
            <div className="flex items-center gap-2">
              <Eye size={20} className="text-gray-500" />
              <span className="text-sm font-medium">Views API</span>
              {viewsStatus && <StatusPill status={viewsStatus} />}
            </div>
            
            <Button 
              size="sm" 
              variant="outline" 
              onClick={checkServices}
              disabled={graphStatus === "loading" || viewsStatus === "loading"}
            >
              <RefreshCw size={14} className={graphStatus === "loading" ? "animate-spin" : ""} />
            </Button>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowMap(!showMap)}
            >
              <MapPin size={14} className="mr-2" />
              {showMap ? 'Hide Map' : 'Show Map'}
            </Button>
            
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowAnalysis(!showAnalysis)}
            >
              <BarChart3 size={14} className="mr-2" />
              Analysis
            </Button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 bg-gray-50 dark:bg-gray-800 p-1 rounded-lg">
          <TabButton id="explorer" label="Explorer" icon={Search} />
          <TabButton id="query" label="Query" icon={Code2} />
          <TabButton id="analysis" label="Analysis" icon={BarChart3} />
          <TabButton id="tools" label="Tools" icon={Settings} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Explorer Tab */}
            {activeTab === 'explorer' && (
              <>
                <Panel title="Network Explorer">
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                          Entity Type
                        </label>
                        <select
                          value={selectedEntityType}
                          onChange={(e) => setSelectedEntityType(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                        >
                          <option value="Person">Person</option>
                          <option value="Organization">Organization</option>
                          <option value="Location">Location</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                          Search Value
                        </label>
                        <input
                          type="text"
                          value={searchTerm}
                          onChange={(e) => setSearchTerm(e.target.value)}
                          placeholder="Enter entity name or ID..."
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                        />
                      </div>
                      
                      <div className="flex items-end">
                        <Button
                          onClick={() => loadEntityNetwork(selectedEntityType, searchTerm)}
                          disabled={isLoadingGraph}
                          className="w-full"
                        >
                          {isLoadingGraph ? (
                            <Loader size={16} className="animate-spin mr-2" />
                          ) : (
                            <Search size={16} className="mr-2" />
                          )}
                          Explore
                        </Button>
                      </div>
                    </div>

                    <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                      <h4 className="font-medium text-gray-900 dark:text-slate-100 mb-2">Quick Examples</h4>
                      <div className="flex flex-wrap gap-2">
                        {ENTITY_EXAMPLES.map((example, index) => (
                          <button
                            key={index}
                            onClick={() => {
                              setSelectedEntityType(example.label);
                              setSearchTerm(example.value);
                              loadEntityNetwork(example.label, example.value);
                            }}
                            className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:hover:bg-blue-900/50"
                          >
                            <Network size={14} />
                            {example.description}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </Panel>

                {/* Path Finding */}
                <Panel title="Find Path Between Entities">
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-3">
                        <h5 className="font-medium text-gray-900 dark:text-slate-100">Source Entity</h5>
                        <input
                          placeholder="Source Label (e.g., Person)"
                          value={pathConfig.srcLabel}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, srcLabel: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                        <input
                          placeholder="Key (e.g., id)"
                          value={pathConfig.srcKey}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, srcKey: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                        <input
                          placeholder="Value (e.g., alice)"
                          value={pathConfig.srcValue}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, srcValue: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                      </div>
                      
                      <div className="space-y-3">
                        <h5 className="font-medium text-gray-900 dark:text-slate-100">Target Entity</h5>
                        <input
                          placeholder="Target Label (e.g., Person)"
                          value={pathConfig.dstLabel}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, dstLabel: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                        <input
                          placeholder="Key (e.g., id)"
                          value={pathConfig.dstKey}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, dstKey: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                        <input
                          placeholder="Value (e.g., bob)"
                          value={pathConfig.dstValue}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, dstValue: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                          Max Length
                        </label>
                        <input
                          type="number"
                          min="1"
                          max="10"
                          value={pathConfig.maxLength}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, maxLength: parseInt(e.target.value) }))}
                          className="w-24 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
                        />
                      </div>
                      
                      <div className="flex items-center gap-2 pt-6">
                        <input
                          type="checkbox"
                          id="directed"
                          checked={pathConfig.directed}
                          onChange={(e) => setPathConfig(prev => ({ ...prev, directed: e.target.checked }))}
                          className="rounded"
                        />
                        <label htmlFor="directed" className="text-sm text-gray-700 dark:text-slate-300">
                          Directed Graph
                        </label>
                      </div>
                      
                      <div className="pt-6">
                        <Button onClick={findShortestPath} disabled={isLoadingGraph}>
                          <ArrowRight size={16} className="mr-2" />
                          Find Path
                        </Button>
                      </div>
                    </div>
                  </div>
                </Panel>
              </>
            )}

            {/* Query Tab */}
            {activeTab === 'query' && (
              <>
                <Panel title="Custom Graph Queries">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                        Cypher Query
                      </label>
                      <textarea
                        value={customQuery}
                        onChange={(e) => setCustomQuery(e.target.value)}
                        className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-mono text-sm"
                        rows={4}
                      />
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Button onClick={runCustomQuery} disabled={queryStatus === "loading"}>
                        {queryStatus === "loading" ? (
                          <Loader size={16} className="animate-spin mr-2" />
                        ) : (
                          <Play size={16} className="mr-2" />
                        )}
                        Execute Query
                      </Button>
                      
                      {queryStatus && queryStatus !== "loading" && (
                        <StatusPill status={queryStatus} />
                      )}
                    </div>
                  </div>
                </Panel>

                <Panel title="Query Examples">
                  <div className="space-y-3">
                    {SAMPLE_QUERIES.map((sample, index) => (
                      <div key={index} className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-medium text-gray-900 dark:text-slate-100">{sample.name}</h4>
                            <p className="text-sm text-gray-600 dark:text-slate-400 mt-1">{sample.description}</p>
                            <code className="text-xs bg-gray-100 dark:bg-gray-800 p-2 rounded mt-2 block">
                              {sample.query}
                            </code>
                          </div>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => setCustomQuery(sample.query)}
                          >
                            Use
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </Panel>

                {queryResult && (
                  <Panel title="Query Results">
                    <pre className="text-sm bg-gray-50 dark:bg-gray-800 p-4 rounded-lg overflow-auto max-h-96">
                      {JSON.stringify(queryResult, null, 2)}
                    </pre>
                  </Panel>
                )}
              </>
            )}

            {/* Analysis Tab */}
            {activeTab === 'analysis' && (
              <div className="space-y-6">
                <AnalysisPanel />
              </div>
            )}

            {/* Tools Tab */}
            {activeTab === 'tools' && (
              <div className="space-y-6">
                <Panel title="Export & Import">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Button
                      variant="outline"
                      onClick={() => {
                        const payload = { 
                          query: customQuery, 
                          entities: [], 
                          graphSelection: { nodes: graphData.nodes, edges: graphData.edges } 
                        };
                        // Trigger dossier export
                      }}
                    >
                      <Download size={16} className="mr-2" />
                      Export Graph Data
                    </Button>
                    
                    <Button variant="outline">
                      <Database size={16} className="mr-2" />
                      Import Graph Data
                    </Button>
                  </div>
                </Panel>

                <DevToolsPanel />
              </div>
            )}

            {/* Graph Visualization */}
            {graphData.nodes.length > 0 && (
              <Panel title="Graph Visualization">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-600 dark:text-slate-400">
                      {graphData.nodes.length} nodes, {graphData.edges.length} edges
                    </div>
                    <DossierButton 
                      getPayload={() => ({ 
                        query: customQuery, 
                        entities: [], 
                        graphSelection: { nodes: graphData.nodes, edges: graphData.edges } 
                      })} 
                    />
                  </div>
                  
                  <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                    <GraphViewerCytoscape 
                      elements={[
                        ...graphData.nodes.map(node => ({ data: node })),
                        ...graphData.edges.map(edge => ({ data: edge }))
                      ]} 
                      directed={pathConfig.directed}
                    />
                  </div>
                </div>
              </Panel>
            )}
          </div>

          {/* Sidebar */}
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
                {[customQuery].slice(0, 3).map((query, index) => (
                  <button
                    key={index}
                    onClick={() => setCustomQuery(query)}
                    className="w-full p-2 text-left text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded text-xs font-mono truncate"
                  >
                    {query}
                  </button>
                ))}
              </div>
            </Panel>
          </div>
        </div>

        {/* Map Panel */}
        {showMap && (
          <Panel title="Geographic View">
            <MapPanel />
          </Panel>
        )}
      </div>
    </DashboardLayout>
  );
}
