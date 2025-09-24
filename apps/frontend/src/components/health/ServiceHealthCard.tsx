import React from "react";
import StatusDot, { ServiceState } from "./StatusDot";

export interface Props {
  name: string;
  state: ServiceState;
  latencyMs: number | null;
  onClick?: () => void;
}

const badgeColor: Record<ServiceState, string> = {
  ok: "bg-green-500",
  degraded: "bg-yellow-500",
  down: "bg-red-500",
  unreachable: "bg-gray-400",
};

export const ServiceHealthCard: React.FC<Props> = ({ name, state, latencyMs, onClick }) => (
  <div
    onClick={onClick}
    className="p-3 rounded shadow-md cursor-pointer flex items-center justify-between"
  >
    <div className="flex items-center gap-2">
      <StatusDot state={state} />
      <span className="font-medium">{name}</span>
    </div>
    <div className="flex items-center gap-2 text-sm">
      <span>{latencyMs !== null ? `${latencyMs} ms` : "–"}</span>
      <span className={`text-white px-2 py-0.5 rounded ${badgeColor[state]}`}>{state}</span>
    </div>
  </div>
);

export default ServiceHealthCard;
