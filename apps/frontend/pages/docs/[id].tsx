import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import EntityHighlighter from '@/components/docs/EntityHighlighter';
import DocCard from '@/components/docs/DocCard';
import { DocRecord } from '@/types/docs';
import EntityBadgeList, { BadgeItem } from '@/components/entities/EntityBadgeList';
import { uniqueEntities } from '@/lib/entities';

export default function DocPage() {
  const router = useRouter();
  const { query } = router;
  const id = (query.id as string) || '';
  const [doc, setDoc] = useState<DocRecord | null>(null);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (!id) return;
    fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/docs/${encodeURIComponent(id)}`)
      .then(async (r) => {
        if (!r.ok) throw new Error('not found');
        return r.json();
      })
      .then(setDoc)
      .catch(() => setError('Dokument nicht gefunden'));
  }, [id]);

  if (error) return <main>{error}</main>;
  if (!doc) return <main>Lade...</main>;

  const badges: BadgeItem[] = uniqueEntities(
    doc.entities.map((e) => ({ label: e.label, value: e.text || '' })),
  );

  const handleBadgeClick = (item: BadgeItem) => {
    if (item.value) router.push(`/search?value=${encodeURIComponent(item.value)}`);
    else router.push(`/search?entity=${encodeURIComponent(item.label)}`);
  };

  return (
    <main style={{ maxWidth: 800, margin: '1rem auto', display: 'flex', gap: '1rem' }}>
      <div style={{ flex: 1 }}>
        <DocCard doc={doc} />
        <EntityHighlighter text={doc.text} entities={doc.entities} />
      </div>
      <aside style={{ width: 200 }}>
        <h4>Entitäten</h4>
        <EntityBadgeList items={badges} onBadgeClick={handleBadgeClick} />
      </aside>
    </main>
  );
}
