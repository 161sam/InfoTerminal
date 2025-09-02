import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import { GraphSnippet } from '../../src/components/analytics/GraphSnippet';
import { NewsTimeline } from '../../src/components/analytics/NewsTimeline';
import { EntityHeader } from '../../src/components/analytics/EntityHeader';
import { fetchAsset, fetchGraph, fetchNews } from '../../src/lib/api';

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
    <div data-testid="person-page">
      {person && <EntityHeader title={person.name || id} type="Person" />}
      <nav>
        <button onClick={() => router.push({ query: { id, tab: 'graph' } })}>Graph</button>
        <button onClick={() => router.push({ query: { id, tab: 'news' } })}>News</button>
      </nav>
      {tab === 'graph' && <GraphSnippet data={graph} />}
      {tab === 'news' && <NewsTimeline items={news} />}
    </div>
  );
}
