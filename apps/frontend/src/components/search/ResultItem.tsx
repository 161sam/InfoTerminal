import Link from 'next/link';
import type { SearchHit } from '../../types/search';

interface Props {
  hit: SearchHit;
}

function Highlights({ hit }: { hit: SearchHit }) {
  if (hit.highlights && hit.highlights.length) {
    const text = hit.highlights.map(h => h.fragments.join(' ... ')).join(' ... ');
    const safe = text.replace(/<(?!\/?(em|mark)>)/g, '&lt;');
    return <p dangerouslySetInnerHTML={{ __html: safe }} />;
  }
  if (hit.snippet) return <p>{hit.snippet}</p>;
  return null;
}

export default function ResultItem({ hit }: Props) {
  return (
    <article>
      {hit.id ? (
        <h3>
          <Link href={`/documents/${hit.id}`}>{hit.title || hit.id}</Link>
        </h3>
      ) : (
        <h3>{hit.title || hit.id}</h3>
      )}
      <Highlights hit={hit} />
      <div>
        {hit.entity_types?.map((t) => (
          <span key={t}>{t} </span>
        ))}
        {hit.source && <span>{hit.source} </span>}
        {hit.node_id && (
          <Link href={`/graphx?focus=${hit.node_id}`}>Graph</Link>
        )}
        {hit.score !== undefined && (
          <small> score: {hit.score.toFixed(2)}</small>
        )}
      </div>
    </article>
  );
}
