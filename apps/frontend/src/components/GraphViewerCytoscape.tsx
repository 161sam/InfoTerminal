import React, { useState, useEffect } from "react";
import CytoscapeComponent from "react-cytoscapejs";

type CyElement = any; // TODO: narrow type if you have a schema
type Props = {
  elements: CyElement;
  layout?: { name: string; [k: string]: any };
  style?: React.CSSProperties;
  className?: string;
  directed?: boolean; // not used
  onNodeClick?: (data: any) => void;
};

const GraphViewerCytoscape: React.FC<Props> = ({
  elements,
  layout = { name: "grid" },
  style,
  className,
  onNodeClick,
}) => {
  const [cy, setCy] = useState<any>();

  useEffect(() => {
    if (!cy || !onNodeClick) return;
    const handler = (e: any) => onNodeClick(e.target.data());
    cy.on("tap", "node", handler);
    return () => {
      cy.off("tap", "node", handler);
    };
  }, [cy, onNodeClick]);

  return (
    <div className={className} style={{ width: "100%", height: "400px", ...style }}>
      <CytoscapeComponent
        cy={setCy}
        elements={elements}
        layout={layout}
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
};

export default GraphViewerCytoscape;
