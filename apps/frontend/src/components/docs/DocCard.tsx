import { useState } from 'react';
import { DocRecord } from '@/types/docs';

interface Props {
  doc: DocRecord;
}

export default function DocCard({ doc }: Props) {
  const [summary, setSummary] = useState<string>('');
  async function summarize() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_NLP_URL}/summarize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: doc.text })
    });
    const data = await res.json();
    setSummary(data.summary || '');
  }
  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
      <h2>{doc.meta?.title || 'Dokument'}</h2>
      {doc.meta?.source && <p>Quelle: {doc.meta.source}</p>}
      {doc.meta?.aleph_id && (
        <a href={`${process.env.NEXT_PUBLIC_ALEPH_URL}/#/documents/${doc.meta.aleph_id}`} target="_blank" rel="noreferrer">In Aleph öffnen</a>
      )}
      <button onClick={summarize}>Zusammenfassen</button>
      {summary && <p>{summary}</p>}
    </div>
  );
}
