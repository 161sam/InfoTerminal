import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import { GraphSnippet } from '@/components/analytics/GraphSnippet';
import { NewsTimeline } from '@/components/analytics/NewsTimeline';
import { EntityHeader } from '@/components/analytics/EntityHeader';
import { fetchAsset, fetchGraph, fetchNews } from '@/lib/api';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function PersonPage() {
  const router = useRouter();
  const { id, tab = 'graph' } = router.query as { id: string; tab?: string };
  const [person, setPerson] = useState<any>();
  const [graph, setGraph] = useState<any>({ nodes: [], edges: [] });
  const [news, setNews] = useState<any[]>([]);

  useEffect(() => {
    if (id) {
      fetchAsset(id).then(setPerson).catch(() => {});
      fetchGraph(id, 1).then(setGraph).catch(() => {});
      fetchNews(id).then(setNews).catch(() => {});
    }
  }, [id]);

  return (
    <DashboardLayout title={person?.name || id || 'Person'}>
      <div data-testid="person-page" className="space-y-4">
        {person && <EntityHeader title={person.name || id} type="Person" />}
        <nav className="flex gap-2">
          <button className="btn btn-secondary" onClick={() => router.push({ query: { id, tab: 'graph' } })}>Graph</button>
          <button className="btn btn-secondary" onClick={() => router.push({ query: { id, tab: 'news' } })}>News</button>
        </nav>
        {tab === 'graph' && <GraphSnippet data={graph} />}
        {tab === 'news' && <NewsTimeline items={news} />}
      </div>
    </DashboardLayout>
  );
}
