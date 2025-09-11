// apps/frontend/src/components/analytics/GraphSnippet.tsx
import React, { useEffect, useRef } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

type CyInstance = {
  on: (event: string, selector: string, handler: (evt: any) => void) => void;
  off?: (event: string, selector?: string) => void;
  destroy?: () => void;
  $: (selector: string) => { emit: (event: string) => void };
};

export type GraphSnippetProps = {
  data: { nodes: any[]; edges: any[] };
  onNodeClick?: (id: string) => void;
  /** For tests: exposes the Cytoscape instance once ready */
  onReady?: (cy: CyInstance) => void;
};

function GraphSnippetComponent({ data, onNodeClick, onReady }: GraphSnippetProps) {
  const cyRef = useRef<CyInstance | null>(null);

  useEffect(() => {
    return () => {
      // Im Testumfeld kann der Canvas/Renderer fehlen – daher defensiv zerstören
      try {
        const cy = cyRef.current;
        if (cy && typeof cy.destroy === 'function') cy.destroy();
      } catch {
        // noop
      } finally {
        cyRef.current = null;
      }
    };
  }, []);

  return (
    <div data-testid="graph-snippet">
      <CytoscapeComponent
        // react-cytoscapejs akzeptiert ein kombiniertes Array aus nodes+edges
        elements={[...(data?.nodes ?? []), ...(data?.edges ?? [])]}
        cy={(cy: CyInstance) => {
          cyRef.current = cy;
          if (onNodeClick) {
            cy.on('tap', 'node', (evt: any) => {
              const id = typeof evt?.target?.id === 'function' ? evt.target.id() : undefined;
              if (id) onNodeClick(id);
            });
          }
          if (onReady) onReady(cy);
        }}
        style={{ width: '100%', height: 200 }}
      />
    </div>
  );
}

// Named export (für Tests, die named import verwenden)
export const GraphSnippet = React.memo(GraphSnippetComponent);

// Default export (für Importe ohne geschweifte Klammern)
export default GraphSnippet;
