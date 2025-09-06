import React from "react";

export type Status = "ok" | "fail" | "loading";

export interface StatusPillProps {
  status: Status;
  children?: React.ReactNode;
}

/**
 * Small colored pill indicating a status.
 */
const StatusPill: React.FC<StatusPillProps> = ({ status, children }) => {
  const color =
    status === "ok"
      ? "bg-green-100 text-green-800"
      : status === "fail"
      ? "bg-red-100 text-red-800"
      : "bg-yellow-100 text-yellow-800";
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${color}`}>
      {children || status}
    </span>
  );
};

export default StatusPill;
