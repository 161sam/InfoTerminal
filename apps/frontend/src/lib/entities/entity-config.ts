// Entity configuration and types for entity management
import { LucideIcon } from 'lucide-react';
import { 
  User, 
  Building2, 
  MapPin, 
  Mail, 
  Globe, 
  Network,
  ExternalLink
} from 'lucide-react';
import { EntityLabel } from '@/lib/entities';

// Entity panel types and interfaces
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

// Utility functions
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

// Mock data for development
export const MOCK_ENTITIES: Entity[] = [
  {
    id: '1',
    name: 'John Smith',
    type: 'Person',
    mentions: 156,
    confidence: 0.95,
    firstSeen: '2024-01-15',
    lastSeen: '2024-03-01',
    sources: ['document-1', 'document-5', 'document-12'],
    verified: true,
    description: 'Senior executive at ACME Corporation',
    aliases: ['J. Smith', 'John S.'],
    connections: 23,
    riskScore: 2,
    tags: ['executive', 'finance']
  },
  {
    id: '2',
    name: 'ACME Corporation',
    type: 'Organization',
    mentions: 243,
    confidence: 0.98,
    firstSeen: '2024-01-10',
    lastSeen: '2024-03-02',
    sources: ['document-2', 'document-3', 'document-8', 'document-15'],
    verified: true,
    description: 'Global technology company',
    connections: 45,
    riskScore: 1,
    tags: ['technology', 'public-company']
  },
  {
    id: '3',
    name: 'London',
    type: 'Location',
    mentions: 89,
    confidence: 0.92,
    firstSeen: '2024-01-20',
    lastSeen: '2024-02-28',
    sources: ['document-4', 'document-9'],
    verified: false,
    description: 'Capital city of the United Kingdom',
    connections: 12,
    riskScore: 0,
    tags: ['city', 'europe']
  },
  {
    id: '4',
    name: 'john.smith@acme.com',
    type: 'Email',
    mentions: 67,
    confidence: 0.99,
    firstSeen: '2024-02-01',
    lastSeen: '2024-03-01',
    sources: ['document-1', 'document-6', 'document-11'],
    verified: false,
    connections: 8,
    riskScore: 1,
    tags: ['contact']
  },
  {
    id: '5',
    name: 'acme.com',
    type: 'Domain',
    mentions: 45,
    confidence: 0.87,
    firstSeen: '2024-01-25',
    lastSeen: '2024-02-29',
    sources: ['document-2', 'document-7'],
    verified: true,
    connections: 15,
    riskScore: 0,
    tags: ['website', 'corporate']
  },
  {
    id: '6',
    name: 'suspicious.example.com',
    type: 'Domain',
    mentions: 12,
    confidence: 0.75,
    firstSeen: '2024-02-28',
    lastSeen: '2024-03-01',
    sources: ['document-20'],
    verified: false,
    description: 'Domain flagged for suspicious activity',
    connections: 3,
    riskScore: 8,
    tags: ['suspicious', 'flagged']
  }
];
