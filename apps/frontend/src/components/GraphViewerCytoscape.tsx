import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

type CyElement = any; // TODO: narrow type if you have a schema
type Props = {
  elements: CyElement;
  layout?: { name: string; [k: string]: any };
  style?: React.CSSProperties;
  className?: string;
    directed?: boolean; // <- ergänzt, wird intern nicht benötigt
};

const GraphViewerCytoscape: React.FC<Props> = ({ elements, layout = { name: 'grid' }, style, className }) => {
  return (
    <div className={className} style={{ width: '100%', height: '400px', ...style }}>
      <CytoscapeComponent elements={elements} layout={layout} style={{ width: '100%', height: '100%' }} />
    </div>
  );
};

export default GraphViewerCytoscape;
