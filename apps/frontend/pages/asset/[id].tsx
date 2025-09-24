import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import { TimeSeriesChart } from "@/components/analytics/TimeSeriesChart";
import { OHLCChart } from "@/components/analytics/OHLCChart";
import { GraphSnippet } from "@/components/analytics/GraphSnippet";
import { NewsTimeline } from "@/components/analytics/NewsTimeline";
import { EntityHeader } from "@/components/analytics/EntityHeader";
import { fetchAsset, fetchAssetPrices, fetchGraph, fetchNews } from "@/lib/api";
import DashboardLayout from "@/components/layout/DashboardLayout";

export default function AssetPage() {
  const router = useRouter();
  const {
    id,
    tab = "chart",
    from,
    to,
  } = router.query as { id: string; tab?: string; from?: string; to?: string };

  const [asset, setAsset] = useState<any>();
  const [prices, setPrices] = useState<any[]>([]);
  const [graph, setGraph] = useState<any>({ nodes: [], edges: [] });
  const [news, setNews] = useState<any[]>([]);

  useEffect(() => {
    if (id) {
      fetchAsset(id)
        .then(setAsset)
        .catch(() => {});
      fetchAssetPrices(id, from, to)
        .then(setPrices)
        .catch(() => {});
      fetchGraph(id, 1)
        .then(setGraph)
        .catch(() => {});
      fetchNews(id)
        .then(setNews)
        .catch(() => {});
    }
  }, [id, from, to]);

  return (
    <DashboardLayout title={asset?.name || id || "Asset"}>
      <div data-testid="asset-page" className="space-y-4">
        {asset && <EntityHeader title={asset.name || id} type="Asset" />}
        <nav className="flex gap-2">
          <button
            className="btn btn-secondary"
            onClick={() => router.push({ query: { id, tab: "chart", from, to } })}
          >
            Kurs
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => router.push({ query: { id, tab: "graph", from, to } })}
          >
            Graph
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => router.push({ query: { id, tab: "news", from, to } })}
          >
            News
          </button>
        </nav>
        {tab === "chart" && (
          <>
            <TimeSeriesChart data={prices.map((p) => ({ ts: p.ts, value: p.close }))} />
            <OHLCChart
              data={prices.map((p) => ({
                ts: p.ts,
                open: p.open,
                high: p.high,
                low: p.low,
                close: p.close,
              }))}
            />
          </>
        )}
        {tab === "graph" && <GraphSnippet data={graph} />}
        {tab === "news" && <NewsTimeline items={news} />}
      </div>
    </DashboardLayout>
  );
}
