import { useEffect, useState } from "react";
import { sanitizeUrl } from "@/lib/endpoints";
import { safeLog, isBrowser } from "@/lib/safe";
import { toast } from "@/components/ui/toast";
import useEndpoints from "./useEndpoints";

export type ServiceStatus = "ok" | "degraded" | "fail" | "unknown";
export interface ServiceEntry {
  status: ServiceStatus;
  latency?: number;
}

export function useServiceHealthMatrix(pollMs = 10000) {
  const [matrix, setMatrix] = useState<Record<string, ServiceEntry>>({});
  const endpoints = useEndpoints();

  useEffect(() => {
    if (!isBrowser()) return;
    let cancelled = false;

    const run = async () => {
      const entries = await Promise.all(
        Object.entries(endpoints).map(async ([key, base]) => {
          if (!base) return [key, { status: "unknown" }] as [string, ServiceEntry];
          const url = sanitizeUrl(base) + "/readyz";
          const start = performance.now();
          try {
            const res = await fetch(url, { cache: "no-store" });
            const latency = Math.round(performance.now() - start);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return [key, { status: "ok", latency }] as [string, ServiceEntry];
          } catch (e) {
            safeLog("health check failed", key, e);
            toast(`${key} unreachable`);
            return [key, { status: "fail" }] as [string, ServiceEntry];
          }
        }),
      );
      if (!cancelled) setMatrix(Object.fromEntries(entries));
    };

    run();
    const id = setInterval(run, pollMs);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [pollMs, endpoints]);

  return matrix;
}

export default useServiceHealthMatrix;
