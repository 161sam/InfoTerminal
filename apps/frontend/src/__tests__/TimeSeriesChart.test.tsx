import { render } from '@testing-library/react';

const brushHandler = vi.fn();
vi.mock('recharts', () => {
  const React = require('react');
  return {
    Line: () => null,
    LineChart: ({ children }: any) => <div>{children}</div>,
    XAxis: () => null,
    YAxis: () => null,
    Tooltip: () => null,
    CartesianGrid: () => null,
    ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
    Brush: (props: any) => {
      brushHandler(props.onChange);
      return null;
    },
  };
});

import { TimeSeriesChart } from '../components/analytics/TimeSeriesChart';

test('renders and brush emits range', () => {
  const fn = vi.fn();
  render(
    <TimeSeriesChart
      data={[{ ts: '1', value: 1 }, { ts: '2', value: 2 }]}
      onBrush={fn}
    />
  );
  const handler = brushHandler.mock.calls[0][0];
  handler({ startIndex: 0, endIndex: 1 });
  expect(fn).toHaveBeenCalledWith([0, 1]);
});
