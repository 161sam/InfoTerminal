import React from "react";
import { Users, Network, Download, Database } from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import { loadPeople, getEgo } from "@/lib/api";
import { toast } from "@/components/ui/toast";
import config from "@/lib/config";

interface GraphToolsProps {
  graphData?: {
    nodes: Array<{ id: string; label: string; type?: string; properties?: any }>;
    edges: Array<{ id: string; source: string; target: string; type?: string; properties?: any }>;
  };
  customQuery?: string;
}

export default function GraphTools({ graphData, customQuery }: GraphToolsProps) {
  const exportGraph = async (fmt: string) => {
    if (!config?.GRAPH_API) {
      toast("Graph API not configured", { variant: "error" });
      return;
    }

    try {
      const r = await fetch(`${config.GRAPH_API}/export/${fmt}`);
      const blob = await r.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = fmt === "json" ? "graph.json" : "graph.graphml";
      a.click();
      URL.revokeObjectURL(url);
      toast(`Graph exported as ${fmt.toUpperCase()}`, { variant: "success" });
    } catch (e: any) {
      toast(`Export failed: ${e.message}`, { variant: "error" });
    }
  };

  return (
    <div className="space-y-6">
      <Panel title="Export & Import">
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button variant="secondary" onClick={() => exportGraph("json")}>
              <Download size={16} className="mr-2" />
              Export as JSON
            </Button>

            <Button variant="secondary" onClick={() => exportGraph("graphml")}>
              <Download size={16} className="mr-2" />
              Export as GraphML
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button variant="secondary" disabled>
              <Database size={16} className="mr-2" />
              Import Graph Data
            </Button>

            <Button
              variant="secondary"
              onClick={() => {
                if (graphData && customQuery) {
                  const payload = {
                    query: customQuery,
                    entities: [],
                    graphSelection: { nodes: graphData.nodes, edges: graphData.edges },
                  };
                  // This would trigger dossier export
                  console.log("Dossier payload:", payload);
                  toast("Dossier export prepared", { variant: "success" });
                }
              }}
            >
              <Download size={16} className="mr-2" />
              Export Graph Selection
            </Button>
          </div>
        </div>
      </Panel>

      {process.env.NODE_ENV !== "production" && <DeveloperTools />}
    </div>
  );
}

function DeveloperTools() {
  const seedDemo = async () => {
    const rows = [
      { id: "alice", name: "Alice", knows_id: "bob" },
      { id: "bob", name: "Bob", knows_id: "carol" },
      { id: "carol", name: "Carol", knows_id: null },
    ];

    try {
      const { inserted } = await loadPeople(rows);
      toast(`Demo data seeded: ${inserted} nodes inserted`, { variant: "success" });
    } catch (e: any) {
      toast(`Seed failed: ${e?.message || e}`, { variant: "error" });
    }
  };

  const testEgo = async () => {
    try {
      const { data } = await getEgo({
        label: "Person",
        key: "id",
        value: "alice",
        depth: 2,
        limit: 50,
      });
      const nodes = data?.nodes?.length ?? 0;
      const edges = data?.relationships?.length ?? 0;
      toast(`Ego query successful: ${nodes} nodes, ${edges} edges`, { variant: "success" });
    } catch (e: any) {
      toast(`Ego query failed: ${e?.message || e}`, { variant: "error" });
    }
  };

  return (
    <Panel
      title="Developer Tools"
      className="border-2 border-dashed border-orange-200 dark:border-orange-800"
    >
      <div className="flex flex-wrap gap-2">
        <Button size="sm" variant="secondary" onClick={seedDemo}>
          <Users size={14} className="mr-2" />
          Seed Demo Data
        </Button>
        <Button size="sm" variant="secondary" onClick={testEgo}>
          <Network size={14} className="mr-2" />
          Test Ego Query
        </Button>
      </div>
    </Panel>
  );
}
