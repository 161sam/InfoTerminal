import Link from 'next/link';
import { ENTITY_COLORS, EntityLabel } from '../../lib/entities';
import {
  User,
  Building2,
  MapPin,
  AtSign,
  Globe,
  Network,
  Tag,
} from 'lucide-react';

type Props = {
  label: EntityLabel;
  value?: string;
  size?: 'sm' | 'md';
  clickable?: boolean;
  onClick?: () => void;
  href?: string;
  countBadge?: number;
};

const ICONS: Record<EntityLabel, any> = {
  Person: User,
  Organization: Building2,
  Location: MapPin,
  Email: AtSign,
  Domain: Globe,
  IP: Network,
  Misc: Tag,
};

export default function EntityBadge({
  label,
  value,
  size = 'md',
  clickable = false,
  onClick,
  href,
  countBadge,
}: Props) {
  const className = `inline-flex items-center gap-1 px-2 py-1 rounded-2xl font-medium ${ENTITY_COLORS[label]} ${
    clickable ? 'cursor-pointer focus:ring-2 ring-offset-2' : ''
  } ${size === 'sm' ? 'text-xs' : 'text-sm'}`;
  const content = (
    <span className={className} aria-label={value ? `Filter Suche nach Wert ${value}` : `Filter Suche nach ${label}`}> 
      {(() => {
        const Icon = ICONS[label];
        return <Icon size={14} />;
      })()}
      {value ? `${label}: ${value}` : label}
      {countBadge !== undefined && (
        <span className="ml-1 rounded-full bg-white px-1 text-xs text-black">{countBadge}</span>
      )}
    </span>
  );
  if (href) {
    return (
      <Link href={href} passHref legacyBehavior>
        <a>{content}</a>
      </Link>
    );
  }
  return (
    <button type="button" role="button" aria-pressed="false" onClick={onClick} className="bg-transparent">
      {content}
    </button>
  );
}

