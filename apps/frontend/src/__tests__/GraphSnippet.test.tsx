import { render } from '@testing-library/react';
import { GraphSnippet } from '@/components/analytics/GraphSnippet';

test('renders nodes and click callback', () => {
  const fn = vi.fn();
  let cy: any;
  render(
    <GraphSnippet
      data={{ nodes: [{ data: { id: 'a', label: 'A' } }], edges: [] }}
      onNodeClick={fn}
      cyRef={(c) => (cy = c)}
    />
  );
  cy.$('#a').emit('tap');
  expect(fn).toHaveBeenCalledWith('a');
});
