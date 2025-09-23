import Link from 'next/link';
import { ENTITY_COLORS, EntityLabel } from '@/lib/entities';
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
  resolutionStatus?: string;
  resolutionScore?: number | null;
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

const RESOLUTION_STYLES: Record<string, string> = {
  resolved: 'bg-emerald-100 text-emerald-800',
  unmatched: 'bg-rose-100 text-rose-800',
  ambiguous: 'bg-amber-100 text-amber-800',
  pending: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-100',
  unknown: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-100',
};

const RESOLUTION_LABELS: Record<string, string> = {
  resolved: 'Resolved',
  unmatched: 'Unmatched',
  ambiguous: 'Ambiguous',
  pending: 'Pending',
  unknown: 'Unknown',
};

function resolutionTone(status: string): string {
  return RESOLUTION_STYLES[status.toLowerCase()] ?? RESOLUTION_STYLES.unknown;
}

function resolutionLabel(status: string): string {
  return RESOLUTION_LABELS[status.toLowerCase()] ?? status;
}

function resolutionTooltip(status: string, score?: number): string {
  const label = resolutionLabel(status);
  if (typeof score === 'number') {
    return `${label} (confidence ${(score * 100).toFixed(1)}%)`;
  }
  return label;
}

export default function EntityBadge({
  label,
  value,
  size = 'md',
  clickable = false,
  onClick,
  href,
  countBadge,
  resolutionStatus,
  resolutionScore,
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
        <span className="ml-1 rounded-full px-1 text-xs
                  bg-gray-100 text-gray-900
                  dark:bg-gray-800 dark:text-gray-100">
          {countBadge}
        </span>
      )}
      {resolutionStatus && (
        <span
          className={`ml-1 rounded-full px-2 py-0.5 text-[10px] font-semibold ${resolutionTone(resolutionStatus)}`}
          title={resolutionTooltip(resolutionStatus, resolutionScore ?? undefined)}
        >
          {resolutionLabel(resolutionStatus)}
          {typeof resolutionScore === 'number' && (
            <span className="ml-1 opacity-80">{Math.round(resolutionScore * 100)}%</span>
          )}
        </span>
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
