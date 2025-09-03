// apps/frontend/src/components/charts/index.tsx
import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  ComposedChart,
  Brush,
  ReferenceLine,
} from 'recharts';
import { TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';

// Color palette for charts
export const CHART_COLORS = {
  primary: '#0ea5e9',
  secondary: '#8b5cf6',
  success: '#22c55e',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  gray: '#6b7280',
  palette: ['#0ea5e9', '#8b5cf6', '#22c55e', '#f59e0b', '#ef4444', '#3b82f6', '#ec4899', '#14b8a6']
};

// Common chart props
interface BaseChartProps {
  data: any[];
  height?: number;
  className?: string;
  showGrid?: boolean;
  showTooltip?: boolean;
  showLegend?: boolean;
  animate?: boolean;
  loading?: boolean;
}

// Custom Tooltip Component
function CustomTooltip({ active, payload, label, labelFormatter, valueFormatter }: any) {
  if (!active || !payload || !payload.length) return null;

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      <p className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
        {labelFormatter ? labelFormatter(label) : label}
      </p>
      {payload.map((entry: any, index: number) => (
        <div key={index} className="flex items-center justify-between gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-gray-700 dark:text-gray-300">{entry.name}:</span>
          </div>
          <span className="font-medium text-gray-900 dark:text-gray-100">
            {valueFormatter ? valueFormatter(entry.value) : entry.value}
          </span>
        </div>
      ))}
    </div>
  );
}

// Time Series Line Chart
interface TimeSeriesChartProps extends BaseChartProps {
  xKey: string;
  yKey: string;
  color?: string;
  strokeWidth?: number;
  dotSize?: number;
  showArea?: boolean;
  showBrush?: boolean;
  onBrushChange?: (range: [number, number]) => void;
}

export function TimeSeriesChart({
  data,
  xKey,
  yKey,
  height = 300,
  className = '',
  color = CHART_COLORS.primary,
  strokeWidth = 2,
  dotSize = 4,
  showGrid = true,
  showTooltip = true,
  showArea = false,
  showBrush = false,
  onBrushChange,
  animate = true,
  loading = false,
}: TimeSeriesChartProps) {
  const Chart = showArea ? AreaChart : LineChart;
  const DataComponent = showArea ? Area : Line;

  if (loading) return <ChartSkeleton height={height} />;

  return (
    <div className={`w-full ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <Chart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" className="opacity-30" />}
          <XAxis dataKey={xKey} className="text-xs text-gray-600 dark:text-gray-400" />
          <YAxis className="text-xs text-gray-600 dark:text-gray-400" />
          {showTooltip && <Tooltip content={<CustomTooltip />} />}
          
          <DataComponent
            type="monotone"
            dataKey={yKey}
            stroke={color}
            strokeWidth={strokeWidth}
            dot={{ r: dotSize }}
            fill={showArea ? `${color}20` : undefined}
            animationDuration={animate ? 1000 : 0}
          />
          
          {showBrush && (
            <Brush
              dataKey={xKey}
              height={30}
              stroke={color}
              onChange={(e) => onBrushChange && onBrushChange([e.startIndex || 0, e.endIndex || data.length - 1])}
            />
          )}
        </Chart>
      </ResponsiveContainer>
    </div>
  );
}

// Multi-Series Chart
interface MultiSeriesChartProps extends BaseChartProps {
  xKey: string;
  series: Array<{
    key: string;
    name: string;
    color?: string;
    type?: 'line' | 'area' | 'bar';
  }>;
}

export function MultiSeriesChart({
  data,
  xKey,
  series,
  height = 300,
  className = '',
  showGrid = true,
  showTooltip = true,
  showLegend = true,
  animate = true,
  loading = false,
}: MultiSeriesChartProps) {
  if (loading) return <ChartSkeleton height={height} />;

  return (
    <div className={`w-full ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" className="opacity-30" />}
          <XAxis dataKey={xKey} className="text-xs text-gray-600 dark:text-gray-400" />
          <YAxis className="text-xs text-gray-600 dark:text-gray-400" />
          {showTooltip && <Tooltip content={<CustomTooltip />} />}
          {showLegend && <Legend />}
          
          {series.map((s, index) => {
            const color = s.color || CHART_COLORS.palette[index % CHART_COLORS.palette.length];
            
            if (s.type === 'area') {
              return (
                <Area
                  key={s.key}
                  type="monotone"
                  dataKey={s.key}
                  name={s.name}
                  stroke={color}
                  fill={`${color}30`}
                  animationDuration={animate ? 1000 : 0}
                />
              );
            } else if (s.type === 'bar') {
              return (
                <Bar
                  key={s.key}
                  dataKey={s.key}
                  name={s.name}
                  fill={color}
                  animationDuration={animate ? 1000 : 0}
                />
              );
            } else {
              return (
                <Line
                  key={s.key}
                  type="monotone"
                  dataKey={s.key}
                  name={s.name}
                  stroke={color}
                  strokeWidth={2}
                  dot={{ r: 3 }}
                  animationDuration={animate ? 1000 : 0}
                />
              );
            }
          })}
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

// Donut Chart with Stats
interface DonutChartProps extends BaseChartProps {
  valueKey: string;
  nameKey: string;
  centerLabel?: string;
  centerValue?: string | number;
}

export function DonutChart({
  data,
  valueKey,
  nameKey,
  height = 300,
  className = '',
  centerLabel,
  centerValue,
  showTooltip = true,
  showLegend = true,
  loading = false,
}: DonutChartProps) {
  if (loading) return <ChartSkeleton height={height} />;

  const total = data.reduce((sum, entry) => sum + entry[valueKey], 0);

  return (
    <div className={`w-full ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            dataKey={valueKey}
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={CHART_COLORS.palette[index % CHART_COLORS.palette.length]} 
              />
            ))}
          </Pie>
          {showTooltip && (
            <Tooltip
              content={({ active, payload }) => {
                if (!active || !payload || !payload.length) return null;
                const data = payload[0].payload;
                const percentage = ((data[valueKey] / total) * 100).toFixed(1);
                return (
                  <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                    <p className="font-medium text-gray-900 dark:text-gray-100">{data[nameKey]}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {data[valueKey]} ({percentage}%)
                    </p>
                  </div>
                );
              }}
            />
          )}
          {showLegend && (
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => <span className="text-sm text-gray-700 dark:text-gray-300">{value}</span>}
            />
          )}
          
          {/* Center Text */}
          {(centerLabel || centerValue) && (
            <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle">
              <tspan x="50%" dy="-0.5em" className="text-sm font-medium fill-gray-700 dark:fill-gray-300">
                {centerLabel}
              </tspan>
              <tspan x="50%" dy="1.2em" className="text-2xl font-bold fill-gray-900 dark:fill-gray-100">
                {centerValue}
              </tspan>
            </text>
          )}
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

// Metric Card with Chart
interface MetricCardProps {
  title: string;
  value: string | number;
  change?: {
    value: number;
    period: string;
  };
  chart?: {
    data: any[];
    dataKey: string;
    color?: string;
  };
  icon?: React.ComponentType<{ size?: number; className?: string }>;
  className?: string;
}

export function MetricCard({
  title,
  value,
  change,
  chart,
  icon: Icon = Activity,
  className = '',
}: MetricCardProps) {
  const isPositiveChange = change && change.value >= 0;
  const TrendIcon = isPositiveChange ? TrendingUp : TrendingDown;

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
            <Icon size={20} className="text-primary-600 dark:text-primary-400" />
          </div>
          <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
        </div>
      </div>
      
      <div className="flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          
          {change && (
            <div className={`flex items-center gap-1 text-sm ${
              isPositiveChange ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
            }`}>
              <TrendIcon size={14} />
              <span>{Math.abs(change.value)}%</span>
              <span className="text-gray-500 dark:text-gray-400">vs {change.period}</span>
            </div>
          )}
        </div>
        
        {chart && (
          <div className="w-24 h-12">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chart.data}>
                <Line
                  type="monotone"
                  dataKey={chart.dataKey}
                  stroke={chart.color || CHART_COLORS.primary}
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}

// Chart Skeleton Loader
function ChartSkeleton({ height }: { height: number }) {
  return (
    <div className="w-full animate-pulse" style={{ height }}>
      <div className="bg-gray-200 dark:bg-gray-700 rounded-lg w-full h-full flex items-center justify-center">
        <BarChart3 size={48} className="text-gray-400" />
      </div>
    </div>
  );
}

// Heatmap Component (for correlation matrices, activity patterns)
interface HeatmapProps {
  data: Array<{ x: string; y: string; value: number }>;
  width?: number;
  height?: number;
  className?: string;
}

export function Heatmap({ data, width = 800, height = 400, className = '' }: HeatmapProps) {
  const xLabels = [...new Set(data.map(d => d.x))];
  const yLabels = [...new Set(data.map(d => d.y))];
  const values = data.map(d => d.value);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  const getColor = (value: number) => {
    const intensity = (value - minValue) / (maxValue - minValue);
    return `rgba(14, 165, 233, ${intensity})`;
  };

  const cellWidth = width / xLabels.length;
  const cellHeight = height / yLabels.length;

  return (
    <div className={`w-full ${className}`}>
      <svg width={width} height={height} className="border border-gray-200 dark:border-gray-700 rounded">
        {data.map((cell, index) => {
          const xIndex = xLabels.indexOf(cell.x);
          const yIndex = yLabels.indexOf(cell.y);
          
          return (
            <g key={index}>
              <rect
                x={xIndex * cellWidth}
                y={yIndex * cellHeight}
                width={cellWidth}
                height={cellHeight}
                fill={getColor(cell.value)}
                stroke="#fff"
                strokeWidth={1}
              />
              <text
                x={xIndex * cellWidth + cellWidth / 2}
                y={yIndex * cellHeight + cellHeight / 2}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="12"
                fill={cell.value > (maxValue + minValue) / 2 ? '#fff' : '#000'}
              >
                {cell.value.toFixed(1)}
              </text>
            </g>
          );
        })}
        
        {/* X-axis labels */}
        {xLabels.map((label, index) => (
          <text
            key={label}
            x={index * cellWidth + cellWidth / 2}
            y={height + 15}
            textAnchor="middle"
            fontSize="10"
            className="fill-gray-600 dark:fill-gray-400"
          >
            {label}
          </text>
        ))}
        
        {/* Y-axis labels */}
        {yLabels.map((label, index) => (
          <text
            key={label}
            x={-10}
            y={index * cellHeight + cellHeight / 2}
            textAnchor="end"
            dominantBaseline="middle"
            fontSize="10"
            className="fill-gray-600 dark:fill-gray-400"
          >
            {label}
          </text>
        ))}
      </svg>
    </div>
  );
}

// Network Graph Component (simple node-link visualization)
interface NetworkNode {
  id: string;
  label: string;
  value?: number;
  group?: string;
}

interface NetworkLink {
  source: string;
  target: string;
  value?: number;
}

interface NetworkGraphProps {
  nodes: NetworkNode[];
  links: NetworkLink[];
  width?: number;
  height?: number;
  className?: string;
}

export function NetworkGraph({ nodes, links, width = 600, height = 400, className = '' }: NetworkGraphProps) {
  // Simple force layout simulation (simplified)
  const getNodePosition = (nodeId: string, index: number) => {
    const angle = (index / nodes.length) * 2 * Math.PI;
    const radius = Math.min(width, height) * 0.3;
    return {
      x: width / 2 + Math.cos(angle) * radius,
      y: height / 2 + Math.sin(angle) * radius,
    };
  };

  return (
    <div className={`w-full ${className}`}>
      <svg width={width} height={height} className="border border-gray-200 dark:border-gray-700 rounded">
        {/* Links */}
        {links.map((link, index) => {
          const sourceNode = nodes.find(n => n.id === link.source);
          const targetNode = nodes.find(n => n.id === link.target);
          const sourceIndex = nodes.findIndex(n => n.id === link.source);
          const targetIndex = nodes.findIndex(n => n.id === link.target);
          
          if (!sourceNode || !targetNode) return null;
          
          const sourcePos = getNodePosition(link.source, sourceIndex);
          const targetPos = getNodePosition(link.target, targetIndex);
          
          return (
            <line
              key={index}
              x1={sourcePos.x}
              y1={sourcePos.y}
              x2={targetPos.x}
              y2={targetPos.y}
              stroke="#6b7280"
              strokeWidth={link.value ? Math.max(1, link.value * 3) : 1}
              opacity={0.6}
            />
          );
        })}
        
        {/* Nodes */}
        {nodes.map((node, index) => {
          const pos = getNodePosition(node.id, index);
          const radius = node.value ? Math.max(8, Math.sqrt(node.value) * 5) : 8;
          
          return (
            <g key={node.id}>
              <circle
                cx={pos.x}
                cy={pos.y}
                r={radius}
                fill={CHART_COLORS.palette[index % CHART_COLORS.palette.length]}
                stroke="#fff"
                strokeWidth={2}
              />
              <text
                x={pos.x}
                y={pos.y + radius + 15}
                textAnchor="middle"
                fontSize="10"
                className="fill-gray-700 dark:fill-gray-300"
              >
                {node.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}