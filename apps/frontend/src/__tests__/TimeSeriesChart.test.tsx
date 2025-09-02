import { render, fireEvent } from '@testing-library/react';
import { TimeSeriesChart } from '../components/analytics/TimeSeriesChart';

test('renders and brush emits range', () => {
  const fn = vi.fn();
  const { container } = render(<TimeSeriesChart data={[{ ts: '1', value: 1 }, { ts: '2', value: 2 }]} onBrush={fn} />);
  const brush = container.querySelector('.recharts-brush');
  if (brush) {
    fireEvent.change(brush, { target: { startIndex: 0, endIndex: 1 } });
  }
  expect(fn).toHaveBeenCalled();
});
