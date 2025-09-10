// appRoutes.ts
export type AppRoute = {
  key: string;
  label: string;
  path: string;        // react-router path
  icon?: React.ReactNode;
  kind: "internal" | "external";
  // for external apps
  urlEnvVar?: string;  // e.g. VITE_APP_ALEPH_URL
  // optional feature flag
  enabled?: boolean;
  // for access control hooks later
  requiredRole?: string;
};

export const appRoutes: AppRoute[] = [
  { key: "home", label: "Home", path: "/", kind: "internal", enabled: true },

  // External apps — URLs kommen aus .env.* (siehe Abschnitt 4)
  { key: "aleph",      label: "Aleph",      path: "/apps/aleph",      kind: "external", urlEnvVar: "VITE_APP_ALEPH_URL",      enabled: true },
  { key: "nifi",       label: "NiFi",       path: "/apps/nifi",       kind: "external", urlEnvVar: "VITE_APP_NIFI_URL",       enabled: true },
  { key: "superset",   label: "Superset",   path: "/apps/superset",   kind: "external", urlEnvVar: "VITE_APP_SUPERSET_URL",   enabled: true },
  { key: "grafana",    label: "Grafana",    path: "/apps/grafana",    kind: "external", urlEnvVar: "VITE_APP_GRAFANA_URL",    enabled: true },
  { key: "prometheus", label: "Prometheus", path: "/apps/prometheus", kind: "external", urlEnvVar: "VITE_APP_PROMETHEUS_URL", enabled: true },

  // …wenn du mehr GUIs integrieren willst: einfach hier ergänzen
];

// kleine Helfer:
export const getExternalUrl = (r: AppRoute): string | null => {
  if (r.kind !== "external" || !r.urlEnvVar) return null;
  const url = import.meta.env[r.urlEnvVar as keyof ImportMetaEnv] as string | undefined;
  return url && url.trim().length > 0 ? url : null;
};
