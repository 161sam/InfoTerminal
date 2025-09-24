import React from "react";
import { Target, CheckCircle2, Clock, AlertCircle, TrendingUp, Network } from "lucide-react";
import { EntityStats } from "./types";

interface EntityStatsOverviewProps {
  stats: EntityStats;
}

export default function EntityStatsOverview({ stats }: EntityStatsOverviewProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">Total</p>
            <p className="text-2xl font-bold text-blue-800 dark:text-blue-300">{stats.total}</p>
          </div>
          <Target size={20} className="text-blue-500" />
        </div>
      </div>

      <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-600 dark:text-green-400 font-medium">Verified</p>
            <p className="text-2xl font-bold text-green-800 dark:text-green-300">
              {stats.verified}
            </p>
          </div>
          <CheckCircle2 size={20} className="text-green-500" />
        </div>
      </div>

      <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-900/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-yellow-600 dark:text-yellow-400 font-medium">Pending</p>
            <p className="text-2xl font-bold text-yellow-800 dark:text-yellow-300">
              {stats.pending}
            </p>
          </div>
          <Clock size={20} className="text-yellow-500" />
        </div>
      </div>

      <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-900/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-red-600 dark:text-red-400 font-medium">High Risk</p>
            <p className="text-2xl font-bold text-red-800 dark:text-red-300">{stats.highRisk}</p>
          </div>
          <AlertCircle size={20} className="text-red-500" />
        </div>
      </div>

      <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-900/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-purple-600 dark:text-purple-400 font-medium">New Today</p>
            <p className="text-2xl font-bold text-purple-800 dark:text-purple-300">
              {stats.newToday}
            </p>
          </div>
          <TrendingUp size={20} className="text-purple-500" />
        </div>
      </div>

      <div className="p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-900/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-indigo-600 dark:text-indigo-400 font-medium">Connections</p>
            <p className="text-2xl font-bold text-indigo-800 dark:text-indigo-300">
              {stats.totalConnections}
            </p>
          </div>
          <Network size={20} className="text-indigo-500" />
        </div>
      </div>
    </div>
  );
}
