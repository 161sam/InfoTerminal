import Link from 'next/link';
import { Entity } from '../../types/docs';

interface Props {
  text: string;
  entities: Entity[];
}

export default function EntityHighlighter({ text, entities }: Props) {
  const base = process.env.NEXT_PUBLIC_GRAPH_DEEPLINK_BASE || '/graphx?focus=';
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;

  entities.sort((a, b) => a.start - b.start).forEach((ent, idx) => {
    if (ent.start > lastIndex) {
      parts.push(<span key={`t-${idx}`}>{text.slice(lastIndex, ent.start)}</span>);
    }
    const entText = text.slice(ent.start, ent.end);
    parts.push(
      <mark key={`e-${idx}`} title={ent.label} data-label={ent.label}>
        {entText}
        {ent.node_id && (
          <Link href={`${base}${encodeURIComponent(ent.node_id)}`}>Im Graph anzeigen</Link>
        )}
      </mark>
    );
    lastIndex = ent.end;
  });
  if (lastIndex < text.length) {
    parts.push(<span key="t-end">{text.slice(lastIndex)}</span>);
  }
  return <p>{parts}</p>;
}
