import { ComposedChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Line, ResponsiveContainer } from 'recharts';
import React from 'react';

export interface OHLCPoint { ts: string; open: number; high: number; low: number; close: number }
interface Props { data: OHLCPoint[] }

export const OHLCChart: React.FC<Props> = ({ data }) => (
  <div data-testid="ohlc-chart" style={{ width: '100%', height: 300 }}>
    <ResponsiveContainer>
      <ComposedChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="ts" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="high" fill="#82ca9d" />
        <Bar dataKey="low" fill="#8884d8" />
        <Line type="monotone" dataKey="close" stroke="#000" dot={false} />
      </ComposedChart>
    </ResponsiveContainer>
  </div>
);
