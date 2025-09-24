import React from "react";

export type ServiceState = "ok" | "degraded" | "down" | "unreachable";

const colorMap: Record<ServiceState, string> = {
  ok: "bg-green-500",
  degraded: "bg-yellow-500",
  down: "bg-red-500",
  unreachable: "bg-gray-400",
};

export const StatusDot: React.FC<{ state: ServiceState; label?: string }> = ({ state, label }) => (
  <span className="inline-flex items-center">
    <span className={`w-3 h-3 rounded-full ${colorMap[state]}`}></span>
    {label && <span className="ml-1">{label}</span>}
  </span>
);

export default StatusDot;
