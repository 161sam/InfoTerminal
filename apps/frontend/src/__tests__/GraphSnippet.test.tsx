import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { vi } from 'vitest';
import GraphSnippet from '@/components/analytics/GraphSnippet';

describe('GraphSnippet', () => {
  it('renders nodes and click callback', () => {
    const onNodeClick = vi.fn();

    render(
      <GraphSnippet
        data={{
          nodes: [
            { data: { id: 'a', label: 'A' } },
            { data: { id: 'b', label: 'B' } },
          ],
          edges: [{ data: { id: 'ab', source: 'a', target: 'b' } }],
        }}
        onNodeClick={onNodeClick}
      />
    );

    fireEvent.click(screen.getByTestId('fire-tap-a'));
    expect(onNodeClick).toHaveBeenCalledWith('a');
  });
});
