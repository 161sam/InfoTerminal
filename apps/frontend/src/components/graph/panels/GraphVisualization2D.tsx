import React from "react";
import { Network, MapPin } from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import StatusPill, { Status } from "@/components/ui/StatusPill";
import { GraphLoadingSkeleton, EmptyState } from "@/components/ui/loading";
import GraphViewerCytoscape from "@/components/GraphViewerCytoscape";
import DossierButton from "@/components/DossierButton";

interface GraphData {
  nodes: Array<{ id: string; label: string; type?: string; properties?: any }>;
  edges: Array<{ id: string; source: string; target: string; type?: string; properties?: any }>;
}

interface GraphVisualization2DProps {
  graphData: GraphData;
  isLoading: boolean;
  selectedNode: any | null;
  directed?: boolean;
  metrics?: Record<string, any[]>;
  customQuery?: string;
  onNodeClick?: (node: any) => void;
  onExportGraph?: (format: string) => void;
}

export default function GraphVisualization2D({
  graphData,
  isLoading,
  selectedNode,
  directed = false,
  metrics = {},
  customQuery = "",
  onNodeClick,
  onExportGraph,
}: GraphVisualization2DProps) {
  if (isLoading) {
    return <GraphLoadingSkeleton />;
  }

  if (graphData.nodes.length === 0) {
    return (
      <EmptyState
        icon={Network}
        title="No Graph Data"
        message="Use the explorer to load network data or run a custom query."
        action={{
          label: "Load Sample Data",
          onClick: () => {
            // This would trigger sample data loading
            console.log("Load sample data requested");
          },
        }}
      />
    );
  }

  return (
    <Panel title="Graph Visualization">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600 dark:text-slate-400">
            {graphData.nodes.length} nodes, {graphData.edges.length} edges
          </div>
          <div className="flex gap-2">
            <Button size="sm" variant="secondary" onClick={() => onExportGraph?.("json")}>
              JSON
            </Button>
            <Button size="sm" variant="secondary" onClick={() => onExportGraph?.("graphml")}>
              GraphML
            </Button>
            <DossierButton
              getPayload={() => ({
                query: customQuery,
                entities: [],
                graphSelection: { nodes: graphData.nodes, edges: graphData.edges },
              })}
            />
          </div>
        </div>

        <div className="relative border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
          <GraphViewerCytoscape
            elements={[
              ...graphData.nodes.map((node) => ({ data: node })),
              ...graphData.edges.map((edge) => ({ data: edge })),
            ]}
            directed={directed}
            onNodeClick={(d) => {
              const nodeData = {
                id: d.id,
                degree: metrics.degree?.find((i) => String(i.id) === String(d.id))?.degree,
                betweenness: metrics.betweenness?.find((i) => String(i.id) === String(d.id))?.score,
                community: metrics.louvain?.find((i) => String(i.id) === String(d.id))?.communityId,
              };
              onNodeClick?.(nodeData);
            }}
          />
          {selectedNode && (
            <div className="absolute top-2 right-2 bg-white dark:bg-gray-800 p-2 text-xs border rounded shadow">
              <div>ID: {selectedNode.id}</div>
              {selectedNode.degree !== undefined && <div>Degree: {selectedNode.degree}</div>}
              {selectedNode.betweenness !== undefined && (
                <div>Betweenness: {selectedNode.betweenness}</div>
              )}
              {selectedNode.community !== undefined && (
                <div>Community: {selectedNode.community}</div>
              )}
            </div>
          )}
        </div>
      </div>
    </Panel>
  );
}
