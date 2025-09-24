import React, { useState } from "react";
import { Search, Network, ArrowRight } from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import { LoadingSpinner } from "@/components/ui/loading";
import { getEgo, getShortestPath } from "@/lib/api";
import { toast } from "@/components/ui/toast";

interface GraphData {
  nodes: Array<{ id: string; label: string; type?: string; properties?: any }>;
  edges: Array<{ id: string; source: string; target: string; type?: string; properties?: any }>;
}

interface GraphExplorerProps {
  onGraphData?: (data: GraphData) => void;
}

const ENTITY_EXAMPLES = [
  { label: "Person", key: "id", value: "alice", description: "Sample person node" },
  { label: "Organization", key: "name", value: "ACME Corp", description: "Company entity" },
  { label: "Location", key: "name", value: "London", description: "Geographic location" },
];

export default function GraphExplorer({ onGraphData }: GraphExplorerProps) {
  // Explorer state
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedEntityType, setSelectedEntityType] = useState("Person");
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
    directed: false,
  });

  const loadEntityNetwork = async (entityType: string, searchValue?: string) => {
    setIsLoadingGraph(true);
    try {
      const { data } = await getEgo({
        label: entityType,
        key: searchValue ? "name" : "id",
        value: searchValue || "alice",
        depth: 2,
        limit: 50,
      });

      const nodes = (data.nodes || []).map((n: any) => ({
        id: String(n.id),
        label: n.properties?.name || String(n.id),
        type: n.labels?.[0] || "Unknown",
      }));

      const edges = (data.relationships || []).map((r: any) => ({
        id: String(r.id),
        source: String(r.start),
        target: String(r.end),
        type: r.type,
      }));

      const graphData = { nodes, edges };
      onGraphData?.(graphData);
      toast(`Loaded ${nodes.length} nodes and ${edges.length} edges`, { variant: "success" });
    } catch (e: any) {
      toast(`Failed to load network: ${e?.message}`, { variant: "error" });
    } finally {
      setIsLoadingGraph(false);
    }
  };

  const findShortestPath = async () => {
    if (!pathConfig.srcValue || !pathConfig.dstValue) {
      toast("Please enter both source and destination values", { variant: "error" });
      return;
    }

    setIsLoadingGraph(true);
    try {
      const { data } = await getShortestPath(pathConfig);

      const nodes = (data.nodes || []).map((n: any) => ({
        id: String(n.id),
        label: n.properties?.name || String(n.id),
        type: n.labels?.[0] || "Unknown",
      }));

      const edges = (data.relationships || []).map((r: any) => ({
        id: String(r.id),
        source: String(r.start),
        target: String(r.end),
        type: r.type,
      }));

      const graphData = { nodes, edges };
      onGraphData?.(graphData);

      if (nodes.length === 0) {
        toast("No path found between the specified nodes", { variant: "error" });
      } else {
        toast(`Found path with ${nodes.length} nodes`, { variant: "success" });
      }
    } catch (e: any) {
      toast(`Path finding failed: ${e?.message}`, { variant: "error" });
    } finally {
      setIsLoadingGraph(false);
    }
  };

  return (
    <div className="space-y-6">
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
                  <LoadingSpinner size="sm" text="" />
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

      <Panel title="Find Path Between Entities">
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <h5 className="font-medium text-gray-900 dark:text-slate-100">Source Entity</h5>
              <input
                placeholder="Source Label (e.g., Person)"
                value={pathConfig.srcLabel}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, srcLabel: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
              />
              <input
                placeholder="Key (e.g., id)"
                value={pathConfig.srcKey}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, srcKey: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
              />
              <input
                placeholder="Value (e.g., alice)"
                value={pathConfig.srcValue}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, srcValue: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
              />
            </div>

            <div className="space-y-3">
              <h5 className="font-medium text-gray-900 dark:text-slate-100">Target Entity</h5>
              <input
                placeholder="Target Label (e.g., Person)"
                value={pathConfig.dstLabel}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, dstLabel: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
              />
              <input
                placeholder="Key (e.g., id)"
                value={pathConfig.dstKey}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, dstKey: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
              />
              <input
                placeholder="Value (e.g., bob)"
                value={pathConfig.dstValue}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, dstValue: e.target.value }))}
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
                onChange={(e) =>
                  setPathConfig((prev) => ({ ...prev, maxLength: parseInt(e.target.value) }))
                }
                className="w-24 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
              />
            </div>

            <div className="flex items-center gap-2 pt-6">
              <input
                type="checkbox"
                id="directed"
                checked={pathConfig.directed}
                onChange={(e) => setPathConfig((prev) => ({ ...prev, directed: e.target.checked }))}
                className="rounded"
              />
              <label htmlFor="directed" className="text-sm text-gray-700 dark:text-slate-300">
                Directed Graph
              </label>
            </div>

            <div className="pt-6">
              <Button onClick={findShortestPath} disabled={isLoadingGraph}>
                {isLoadingGraph ? (
                  <LoadingSpinner size="sm" text="" />
                ) : (
                  <ArrowRight size={16} className="mr-2" />
                )}
                Find Path
              </Button>
            </div>
          </div>
        </div>
      </Panel>
    </div>
  );
}
