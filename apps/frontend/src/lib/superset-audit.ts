type NF = {
  id?: string;
  column: string;
  datasetId: number;
  values?: (string | number)[];
};
type AuditFilterArgs = {
  base: string; // http://superset.127.0.0.1.nip.io
  slug: string; // Dashboard slug, z.B. "opa-audit-clickhouse"
  datasetId: number; // logs.opa_decisions dataset id
  tenants?: string[];
  paths?: string[];
  timeRange?: string; // "Last 24 hours", "Last 7 days"
};

export function auditDashboardUrl(a: AuditFilterArgs) {
  const filters: NF[] = [];
  if (a.tenants?.length)
    filters.push({ column: "tenant", datasetId: a.datasetId, values: a.tenants });
  if (a.paths?.length) filters.push({ column: "path", datasetId: a.datasetId, values: a.paths });
  const state: any = {
    native_filters: filters.map((f, i) => ({
      id: f.id || `nf-${i}`,
      filterState: { value: f.values ?? null },
      targets: [{ column: f.column, datasetId: f.datasetId }],
      type: "select",
    })),
    time_range: a.timeRange || "Last 24 hours",
  };
  const frag = encodeURIComponent(JSON.stringify(state));
  const u = new URL(`/superset/dashboard/${a.slug}/`, a.base);
  u.searchParams.set("standalone", "0");
  return `${u.toString()}#${frag}`;
}
