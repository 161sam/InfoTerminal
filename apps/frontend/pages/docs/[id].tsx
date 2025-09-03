import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import EntityHighlighter from '../../src/components/docs/EntityHighlighter';
import DocCard from '../../src/components/docs/DocCard';
import { DocRecord } from '../../src/types/docs';

export default function DocPage() {
  const { query } = useRouter();
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
  return (
    <main style={{ maxWidth: 800, margin: '1rem auto' }}>
      <DocCard doc={doc} />
      <EntityHighlighter text={doc.text} entities={doc.entities} />
    </main>
  );
}
