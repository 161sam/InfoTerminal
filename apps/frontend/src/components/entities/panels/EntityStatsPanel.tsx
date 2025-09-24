// Entity statistics dashboard panel
import { Target, CheckCircle2, Clock, AlertCircle, TrendingUp, Network } from "lucide-react";
import { EntityStats } from "@/lib/entities/entity-config";

interface EntityStatsPanelProps {
  stats: EntityStats;
}

export function EntityStatsPanel({ stats }: EntityStatsPanelProps) {
  const statCards = [
    {
      label: "Total",
      value: stats.total,
      icon: Target,
      color: "blue",
    },
    {
      label: "Verified",
      value: stats.verified,
      icon: CheckCircle2,
      color: "green",
    },
    {
      label: "Pending",
      value: stats.pending,
      icon: Clock,
      color: "yellow",
    },
    {
      label: "High Risk",
      value: stats.highRisk,
      icon: AlertCircle,
      color: "red",
    },
    {
      label: "New Today",
      value: stats.newToday,
      icon: TrendingUp,
      color: "purple",
    },
    {
      label: "Connections",
      value: stats.totalConnections,
      icon: Network,
      color: "indigo",
    },
  ];

  const getCardClasses = (color: string) => {
    const baseClasses = "p-4 rounded-lg border";
    const colorClasses = {
      blue: "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-900/30",
      green: "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-900/30",
      yellow: "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-900/30",
      red: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-900/30",
      purple: "bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-900/30",
      indigo: "bg-indigo-50 dark:bg-indigo-900/20 border-indigo-200 dark:border-indigo-900/30",
    };
    return `${baseClasses} ${colorClasses[color as keyof typeof colorClasses]}`;
  };

  const getTextClasses = (color: string) => {
    const colorClasses = {
      blue: "text-blue-600 dark:text-blue-400",
      green: "text-green-600 dark:text-green-400",
      yellow: "text-yellow-600 dark:text-yellow-400",
      red: "text-red-600 dark:text-red-400",
      purple: "text-purple-600 dark:text-purple-400",
      indigo: "text-indigo-600 dark:text-indigo-400",
    };
    return colorClasses[color as keyof typeof colorClasses];
  };

  const getValueClasses = (color: string) => {
    const colorClasses = {
      blue: "text-blue-800 dark:text-blue-300",
      green: "text-green-800 dark:text-green-300",
      yellow: "text-yellow-800 dark:text-yellow-300",
      red: "text-red-800 dark:text-red-300",
      purple: "text-purple-800 dark:text-purple-300",
      indigo: "text-indigo-800 dark:text-indigo-300",
    };
    return colorClasses[color as keyof typeof colorClasses];
  };

  const getIconClasses = (color: string) => {
    const colorClasses = {
      blue: "text-blue-500",
      green: "text-green-500",
      yellow: "text-yellow-500",
      red: "text-red-500",
      purple: "text-purple-500",
      indigo: "text-indigo-500",
    };
    return colorClasses[color as keyof typeof colorClasses];
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {statCards.map((stat) => {
        const Icon = stat.icon;
        return (
          <div key={stat.label} className={getCardClasses(stat.color)}>
            <div className="flex items-center justify-between">
              <div>
                <p className={`text-sm font-medium ${getTextClasses(stat.color)}`}>{stat.label}</p>
                <p className={`text-2xl font-bold ${getValueClasses(stat.color)}`}>{stat.value}</p>
              </div>
              <Icon size={20} className={getIconClasses(stat.color)} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default EntityStatsPanel;
