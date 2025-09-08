import dynamic from "next/dynamic";
import React from "react";

const CytoscapeComponent = dynamic(() => import("react-cytoscapejs"), {
  ssr: false,
});

export interface CytoscapeElement {
  data: any;
}

export default function GraphViewerCytoscape({
  elements,
  directed = false,
}: {
  elements: CytoscapeElement[];
  directed?: boolean;
}) {
  if (!elements || elements.length === 0) return null;
  return (
    <CytoscapeComponent
      elements={elements as any}
      layout={{ name: "breadthfirst" }}
      style={{ width: "100%", height: 400, border: "1px solid #ccc", borderRadius: 8 }}
      stylesheet={[
        {
          selector: "node",
          style: {
            label: "data(label)",
          },
        },
        {
          selector: "edge",
          style: {
            label: "data(label)",
            "curve-style": "bezier",
            "target-arrow-shape": directed ? "triangle" : "none",
          },
        },
      ]}
    />
  );
}
