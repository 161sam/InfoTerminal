import React from "react";
import {
  Server, 
  CheckCircle, 
  Monitor, 
  Globe,
  Palette,
} from 'lucide-react';

interface OverviewMetrics {
  services: {
    configured: number;
    total: number;
  };
  healthy: number;
  operationsStatus: 'Active' | 'Inactive' | 'Maintenance';
  theme: string;
  runtime: 'Server' | 'Client';
}

interface SettingsOverviewProps {
  metrics: OverviewMetrics;
}

const OverviewCard = ({ 
  icon: Icon, 
  label, 
  value, 
  bgColor, 
  textColor, 
  borderColor 
}: {
  icon: React.ComponentType<{ size: number; className: string }>;
  label: string;
  value: string | number;
  bgColor: string;
  textColor: string;
  borderColor: string;
}) => (
  <div className={`p-4 ${bgColor} rounded-lg border ${borderColor}`}>
    <div className="flex items-center gap-3">
      <Icon size={20} className={textColor} />
      <div>
        <div className={`text-sm ${textColor} font-medium`}>{label}</div>
        <div className={`text-lg font-bold ${textColor.replace('text-', 'text-').replace('-400', '-300').replace('-600', '-800')}`}>
          {value}
        </div>
      </div>
    </div>
  </div>
);

export default function SettingsOverview({ metrics }: SettingsOverviewProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
      <OverviewCard
        icon={Server}
        label="Services"
        value={`${metrics.services.configured}/${metrics.services.total}`}
        bgColor="bg-blue-50 dark:bg-blue-900/20"
        textColor="text-blue-600 dark:text-blue-400"
        borderColor="border-blue-200 dark:border-blue-900/30"
      />
      
      <OverviewCard
        icon={CheckCircle}
        label="Healthy"
        value={metrics.healthy}
        bgColor="bg-green-50 dark:bg-green-900/20"
        textColor="text-green-600 dark:text-green-400"
        borderColor="border-green-200 dark:border-green-900/30"
      />
      
      <OverviewCard
        icon={Monitor}
        label="Operations"
        value={metrics.operationsStatus}
        bgColor="bg-amber-50 dark:bg-amber-900/20"
        textColor="text-amber-600 dark:text-amber-400"
        borderColor="border-amber-200 dark:border-amber-900/30"
      />
      
      <OverviewCard
        icon={Palette}
        label="Theme"
        value={metrics.theme}
        bgColor="bg-purple-50 dark:bg-purple-900/20"
        textColor="text-purple-600 dark:text-purple-400"
        borderColor="border-purple-200 dark:border-purple-900/30"
      />
      
      <OverviewCard
        icon={Globe}
        label="Runtime"
        value={metrics.runtime}
        bgColor="bg-orange-50 dark:bg-orange-900/20"
        textColor="text-orange-600 dark:text-orange-400"
        borderColor="border-orange-200 dark:border-orange-900/30"
      />
    </div>
  );
}
