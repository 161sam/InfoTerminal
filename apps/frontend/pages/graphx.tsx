import React, { useState, useEffect } from "react";
import { 
  Network, 
  RefreshCw, 
  Users, 
  Building, 
  MapPin,
  Database,
  Eye,
  Search,
  Code2,
  BarChart3,
  Cube,
  Brain,
  Settings
} from 'lucide-react';
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import { Tabs, TabsList, TabsTrigger, TabsContent, SubTabs } from "@/components/ui/tabs";
import { EmptyState } from "@/components/ui/loading";
import AnalysisPanel from "@/components/graph/AnalysisPanel";
import {
  GraphExplorer,
  GraphQueryInterface,
  GraphVisualization2D,
  GraphVisualization3D,
  GraphMLAnalytics,
  GraphTools,
  GraphSidebar
} from "@/components/graph/panels";
import config from "@/lib/config";

interface GraphData {
  nodes: Array<{ id: string; label: string; type?: string; properties?: any }>;
  edges: Array<{ id: string; source: string; target: string; type?: string; properties?: any }>;
}

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

export default function ConsolidatedGraphPage() {
  const [activeMainTab, setActiveMainTab] = useState<string>('graph');
  const [activeGraphTab, setActiveGraphTab] = useState<string>('explorer');
  const [graphStatus, setGraphStatus] = useState<Status>();
  const [viewsStatus, setViewsStatus] = useState<Status>();
  
  // Query state
  const [customQuery, setCustomQuery] = useState("MATCH (n) RETURN n LIMIT 10");
  const [queryResult, setQueryResult] = useState<any>(null);
  
  // Graph state
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], edges: [] });
  const [metrics, setMetrics] = useState<Record<string, any[]>>({});
  const [selectedNode, setSelectedNode] = useState<any | null>(null);

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

  const handleAnalysisResult = (alg: string, items: any[]) => {
    setMetrics(m => ({ ...m, [alg]: items }));
  };

  const exportGraph = async (fmt: string) => {
    if (!config?.GRAPH_API) return;
    const r = await fetch(`${config.GRAPH_API}/export/${fmt}`);
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fmt === 'json' ? 'graph.json' : 'graph.graphml';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <DashboardLayout title="Graph Analysis" subtitle="Visualize, analyze and explore your knowledge graph">
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
              variant="secondary" 
              onClick={checkServices}
              disabled={graphStatus === "loading" || viewsStatus === "loading"}
            >
              <RefreshCw size={14} className={graphStatus === "loading" ? "animate-spin" : ""} />
            </Button>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="secondary"
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

        {/* Main Tab Navigation */}
        <Tabs value={activeMainTab} onValueChange={setActiveMainTab} variant="default">
          <TabsList>
            <TabsTrigger value="graph" icon={Network}>
              Graph View
            </TabsTrigger>
            <TabsTrigger value="viz3d" icon={Cube}>
              3D Visualization
            </TabsTrigger>
            <TabsTrigger value="ml" icon={Brain}>
              ML Analytics
            </TabsTrigger>
          </TabsList>

          {/* Graph View Tab Content */}
          <TabsContent value="graph">
            <SubTabs value={activeGraphTab} onValueChange={setActiveGraphTab} variant="underline">
              <TabsList>
                <TabsTrigger value="explorer" icon={Search}>
                  Explorer
                </TabsTrigger>
                <TabsTrigger value="query" icon={Code2}>
                  Query
                </TabsTrigger>
                <TabsTrigger value="analysis" icon={BarChart3}>
                  Analysis
                </TabsTrigger>
                <TabsTrigger value="tools" icon={Settings}>
                  Tools
                </TabsTrigger>
              </TabsList>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-6">
                  
                  {/* Explorer Tab */}
                  <TabsContent value="explorer">
                    <GraphExplorer onGraphData={setGraphData} />
                  </TabsContent>

                  {/* Query Tab */}
                  <TabsContent value="query">
                    <GraphQueryInterface 
                      initialQuery={customQuery}
                      onQueryResult={setQueryResult}
                    />
                  </TabsContent>

                  {/* Analysis Tab */}
                  <TabsContent value="analysis">
                    <AnalysisPanel onResult={handleAnalysisResult} />
                  </TabsContent>

                  {/* Tools Tab */}
                  <TabsContent value="tools">
                    <GraphTools 
                      graphData={graphData}
                      customQuery={customQuery}
                    />
                  </TabsContent>

                  {/* Graph Visualization */}
                  <GraphVisualization2D
                    graphData={graphData}
                    isLoading={false}
                    selectedNode={selectedNode}
                    directed={false}
                    metrics={metrics}
                    customQuery={customQuery}
                    onNodeClick={setSelectedNode}
                    onExportGraph={exportGraph}
                  />
                </div>

                {/* Sidebar */}
                <GraphSidebar
                  graphData={graphData}
                  graphStatus={graphStatus}
                  customQuery={customQuery}
                  onQuerySelect={setCustomQuery}
                />
              </div>
            </SubTabs>
          </TabsContent>

          {/* 3D Visualization Tab Content */}
          <TabsContent value="viz3d">
            <GraphVisualization3D graphData={graphData} />
          </TabsContent>

          {/* ML Analytics Tab Content */}
          <TabsContent value="ml">
            <GraphMLAnalytics onAnalysisResult={handleAnalysisResult} />
          </TabsContent>
        </Tabs>

        {/* Map Panel (if enabled) */}
        {showMap && (
          <Panel title="Geographic View">
            <div className="h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
              <EmptyState
                icon={MapPin}
                title="Map Integration"
                message="Geographic visualization will be available in a future update"
              />
            </div>
          </Panel>
        )}
      </div>
    </DashboardLayout>
  );
}
