import { 
  User, 
  Building2, 
  MapPin, 
  Mail, 
  Globe, 
  Network, 
  ExternalLink 
} from 'lucide-react';
import { LucideIcon } from 'lucide-react';
import { EntityLabel } from '@/lib/entities';

export interface Entity {
  id: string;
  name: string;
  type: EntityLabel;
  mentions: number;
  confidence: number;
  firstSeen: string;
  lastSeen: string;
  sources: string[];
  verified: boolean;
  description?: string;
  aliases?: string[];
  connections?: number;
  riskScore?: number;
  tags?: string[];
}

export interface EntityStats {
  total: number;
  verified: number;
  pending: number;
  highRisk: number;
  newToday: number;
  totalConnections: number;
}

export interface EntityFilter {
  type: string;
  verified: string;
  riskLevel: string;
  dateRange: string;
  minMentions: number;
  searchTerm: string;
}

export interface SortConfig {
  key: string;
  direction: 'asc' | 'desc';
}

export interface RiskLevel {
  value: string;
  label: string;
  color: string;
}

export const ENTITY_TYPE_ICONS: Record<EntityLabel, LucideIcon> = {
  Person: User,
  Organization: Building2,
  Location: MapPin,
  Email: Mail,
  Domain: Globe,
  IP: Network,
  Misc: ExternalLink,
};

export const RISK_LEVELS: RiskLevel[] = [
  { value: 'all', label: 'All Levels', color: 'gray' },
  { value: 'low', label: 'Low Risk (0-3)', color: 'green' },
  { value: 'medium', label: 'Medium Risk (4-6)', color: 'yellow' },
  { value: 'high', label: 'High Risk (7-10)', color: 'red' }
];

export function calculateEntityStats(entities: Entity[]): EntityStats {
  return {
    total: entities.length,
    verified: entities.filter(e => e.verified).length,
    pending: entities.filter(e => !e.verified).length,
    highRisk: entities.filter(e => (e.riskScore || 0) >= 7).length,
    newToday: entities.filter(e => {
      const today = new Date().toDateString();
      return new Date(e.firstSeen).toDateString() === today;
    }).length,
    totalConnections: entities.reduce((sum, e) => sum + (e.connections || 0), 0)
  };
}

export function getRiskColor(score: number): string {
  if (score >= 7) return 'text-red-600 bg-red-100';
  if (score >= 4) return 'text-yellow-600 bg-yellow-100';
  return 'text-green-600 bg-green-100';
}
