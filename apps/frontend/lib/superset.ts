// Compose Superset dashboard URL with native filters (hash fragment)
export type NativeFilter = {
  id: string;                  // stable filter id (or auto)
  column: string;              // column name in dataset
  datasetId: number;           // Superset dataset id
  values?: (string|number)[];  // for select/filter_box
  timeRange?: string;          // e.g. "Last 30 days", "No filter"
};

export function supersetDashboardUrl(base: string, slug: string, filters: NativeFilter[]) {
  // Superset accepts native_filters_key or full state via # or ?native_filters=...
  // We inline state via hash for portability.
  const filterState = {
    native_filters: filters.map((f, i) => ({
      id: f.id || `auto-${i}`,
      filterState: {
        value: f.values ?? null,
        validateMessage: null,
      },
      targets: [{
        column: f.column,
        datasetId: f.datasetId,
      }],
      type: "select",
    })),
    time_range: filters.find(f => f.timeRange)?.timeRange || "No filter",
  };
  const encoded = encodeURIComponent(JSON.stringify(filterState));
  // Example final URL:
  // http://superset.host/superset/dashboard/<slug>/?standalone=0#<encoded>
  const u = new URL(`/superset/dashboard/${slug}/`, base);
  u.searchParams.set("standalone", "0");
  return `${u.toString()}#${encoded}`;
}
