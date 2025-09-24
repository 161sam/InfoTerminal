import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { Settings, Download, Cube } from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import { LoadingSpinner, EmptyState } from "@/components/ui/loading";

// Dynamic imports for 3D visualization to avoid SSR issues
const DeckGLComp = dynamic(() => import("@deck.gl/react").then((m: any) => m.default || m.DeckGL), {
  ssr: false,
});

interface GraphVisualization3DProps {
  graphData?: {
    nodes: Array<{ id: string; label: string; type?: string; properties?: any }>;
    edges: Array<{ id: string; source: string; target: string; type?: string; properties?: any }>;
  };
}

export default function GraphVisualization3D({ graphData }: GraphVisualization3DProps) {
  const [ScatterplotLayer, setScatterplotLayer] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load layers on client to avoid SSR issues
    import("@deck.gl/layers").then((m: any) => {
      setScatterplotLayer(() => m.ScatterplotLayer);
      setLoading(false);
    });
  }, []);

  const layers = ScatterplotLayer
    ? [
        new ScatterplotLayer({
          id: "scatter",
          data: [
            { position: [0, 0], size: 100 },
            { position: [0.1, 0.1], size: 80 },
          ],
          getPosition: (d: any) => d.position,
          getRadius: (d: any) => d.size,
          getFillColor: [200, 0, 80],
        }),
      ]
    : [];

  if (loading) {
    return (
      <LoadingSpinner
        layout="card"
        text="Loading 3D Components"
        subText="Initializing deck.gl visualization"
      />
    );
  }

  return (
    <Panel title="3D Graph Visualization">
      <div className="space-y-4">
        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
          <h4 className="font-medium text-blue-900 dark:text-blue-300 mb-2">3D Network View</h4>
          <p className="text-sm text-blue-700 dark:text-blue-400">
            Interactive 3D visualization powered by deck.gl for spatial network analysis
          </p>
        </div>

        <div
          style={{ height: 500 }}
          className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
        >
          {ScatterplotLayer ? (
            // @ts-ignore: dynamic ESM default
            <DeckGLComp
              initialViewState={{
                longitude: 0,
                latitude: 0,
                zoom: 12,
                pitch: 45,
                bearing: 0,
              }}
              controller={true}
              layers={layers}
            />
          ) : (
            <EmptyState
              icon={Cube}
              title="3D View Loading"
              message="Preparing 3D visualization components..."
            />
          )}
        </div>

        <div className="flex gap-2">
          <Button size="sm" variant="secondary">
            <Settings size={14} className="mr-2" />
            Configure 3D View
          </Button>
          <Button size="sm" variant="secondary">
            <Download size={14} className="mr-2" />
            Export 3D Scene
          </Button>
        </div>
      </div>
    </Panel>
  );
}
