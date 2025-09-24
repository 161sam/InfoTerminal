import {
  Line,
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Brush,
  ResponsiveContainer,
} from "recharts";
import React from "react";

export interface SeriesPoint {
  ts: string;
  value: number;
}
interface Props {
  data: SeriesPoint[];
  onBrush?: (range: [number, number]) => void;
}

export const TimeSeriesChart: React.FC<Props> = ({ data, onBrush }) => {
  return (
    <div data-testid="timeseries-chart" style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ts" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#8884d8" dot={false} />
          {onBrush && (
            <Brush
              dataKey="ts"
              onChange={(e) =>
                e?.startIndex != null && e?.endIndex != null && onBrush([e.startIndex, e.endIndex])
              }
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
