export type ExternalAppKey = "aleph" | "nifi" | "superset" | "grafana" | "prometheus";

export const externalApps: Record<
  ExternalAppKey,
  {
    label: string;
    env: string;
    path: string;
  }
> = {
  aleph: { label: "Aleph", env: "NEXT_PUBLIC_APP_ALEPH_URL", path: "/apps/aleph" },
  nifi: { label: "NiFi", env: "NEXT_PUBLIC_APP_NIFI_URL", path: "/apps/nifi" },
  superset: { label: "Superset", env: "NEXT_PUBLIC_APP_SUPERSET_URL", path: "/apps/superset" },
  grafana: { label: "Grafana", env: "NEXT_PUBLIC_APP_GRAFANA_URL", path: "/apps/grafana" },
  prometheus: {
    label: "Prometheus",
    env: "NEXT_PUBLIC_APP_PROMETHEUS_URL",
    path: "/apps/prometheus",
  },
};

export const getExternalUrl = (k: ExternalAppKey): string | null => {
  const key = externalApps[k].env as keyof typeof process.env;
  const v = process.env[key] ?? "";
  return v.trim() ? v : null;
};

export interface SidebarItem {
  label: string;
  href: string;
  externalKey?: string;
}

export const sidebar: SidebarItem[] = [
  { label: "Dashboard", href: "/" },
  { label: "Search", href: "/search" },
  { label: "Graph", href: "/graphx" },
  { label: "Documents", href: "/documents" },
  { label: "Analytics", href: "/analytics" },
  { label: "Entities", href: "/entities" },
  { label: "Data", href: "/data" },
  { label: "Security", href: "/security" },
  { label: "Settings", href: "/settings" },
  { label: "—", href: "" }, // Divider
  ...Object.values(externalApps).map((a) => ({ label: a.label, href: a.path, externalKey: a.env })),
];
