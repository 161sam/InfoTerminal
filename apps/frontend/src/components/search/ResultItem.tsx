import Link from 'next/link';
import { useRouter } from 'next/router';
import type { SearchHit } from '../../types/search';
import EntityBadge from '../entities/EntityBadge';
import { displayValue, normalizeLabel } from '../../lib/entities';
import { buildSearchUrl } from '../../lib/searchNav';

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
  const router = useRouter();
  const query = router.query;
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
      <div className="flex flex-wrap gap-1">
        {hit.entity_types?.map((t) => {
          const label = normalizeLabel(t);
          const href = buildSearchUrl(query, { addEntity: label });
          return <EntityBadge key={t} label={label} href={href} clickable />;
        })}
        {hit.meta?.entities?.map((e: any, idx: number) => {
          const label = normalizeLabel(e.label);
          const value = displayValue(e.value || e.text);
          const href = buildSearchUrl(query, { addValue: value });
          return (
            <EntityBadge key={idx} label={label} value={value} href={href} clickable />
          );
        })}
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
