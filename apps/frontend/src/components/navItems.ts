import type { LucideIcon } from "lucide-react";
import {
  Home,
  Search,
  Network,
  FileText,
  BarChart3,
  Users,
  Database,
  Shield,
  Bot,
  Sparkles,
  Settings,
  Brain
} from "lucide-react";

export type NavItem = {
  key: string;
  name: string;
  href: string;
  icon: LucideIcon;
  featureFlag?: string;
  badge?: number;
  description?: string;
  category?: 'core' | 'analysis' | 'intelligence' | 'management';
};

export const NAV_ITEMS: NavItem[] = [
  // Core functionality
  { 
    key: "dashboard", 
    name: "Dashboard", 
    href: "/", 
    icon: Home,
    description: "Overview and system status",
    category: "core"
  },
  { 
    key: "search", 
    name: "Search", 
    href: "/search", 
    icon: Search,
    description: "Search across all data sources",
    category: "core"
  },
  { 
    key: "graph", 
    name: "Graph", 
    href: "/graphx", 
    icon: Network,
    description: "Entity relationships and network analysis",
    category: "analysis"
  },

  // AI and Intelligence
  { 
    key: "agent", 
    name: "Agent", 
    href: "/agent", 
    icon: Bot, 
    featureFlag: "NEXT_PUBLIC_FEATURE_AGENT",
    description: "AI-powered investigation assistant",
    category: "intelligence"
  },
  { 
    key: "agents", 
    name: "Agent Management", 
    href: "/agents", 
    icon: Brain, 
    featureFlag: "NEXT_PUBLIC_FEATURE_AGENT",
    description: "Manage AI agents and capabilities",
    category: "management"
  },
  { 
    key: "nlp", 
    name: "NLP", 
    href: "/nlp", 
    icon: Sparkles, 
    featureFlag: "NEXT_PUBLIC_FEATURE_NLP",
    description: "Natural language processing and entity extraction",
    category: "analysis"
  },

  // Content and Data
  { 
    key: "documents", 
    name: "Documents", 
    href: "/documents", 
    icon: FileText,
    description: "Document management and analysis",
    category: "core"
  },
  { 
    key: "entities", 
    name: "Entities", 
    href: "/entities", 
    icon: Users,
    description: "Person and organization profiles",
    category: "analysis"
  },
  { 
    key: "data", 
    name: "Data", 
    href: "/data", 
    icon: Database,
    description: "Data sources and integrations",
    category: "core"
  },

  // Analytics and Security
  { 
    key: "analytics", 
    name: "Analytics", 
    href: "/analytics", 
    icon: BarChart3,
    description: "Data analytics and reporting",
    category: "analysis"
  },
  { 
    key: "legal", 
    name: "Legal/Compliance", 
    href: "/legal", 
    icon: FileText,
    description: "Law retrieval and compliance context",
    category: "analysis"
  },
  { 
    key: "graphml", 
    name: "Graph ML", 
    href: "/graph-ml", 
    icon: Brain,
    description: "Run PageRank and Node2Vec",
    category: "analysis"
  },
  { 
    key: "security", 
    name: "Security", 
    href: "/security", 
    icon: Shield,
    description: "Security monitoring and compliance",
    category: "management"
  },
  { 
    key: "ethics", 
    name: "Ethical AI", 
    href: "/ethics", 
    icon: Settings,
    description: "Explainability and model cards",
    category: "analysis"
  },
  { 
    key: "forensics", 
    name: "Forensics", 
    href: "/forensics", 
    icon: FileText,
    description: "Chain-of-custody and verification",
    category: "analysis"
  },
  { 
    key: "viz3d", 
    name: "3D Viz", 
    href: "/viz3d", 
    icon: Sparkles,
    description: "deck.gl prototype",
    category: "analysis"
  },
  { 
    key: "collab", 
    name: "Collaboration", 
    href: "/collab", 
    icon: Users,
    description: "Live notes and audit stream",
    category: "management"
  },
];

export const ff = (k: string) => {
  const v = process.env[k];
  if (v === undefined) return true;
  return v === "1" || v.toLowerCase() === "true";
};

export function isEnabled(item: NavItem) {
  return !item.featureFlag || ff(item.featureFlag);
}

export function getNavItemsByCategory(category: NavItem['category']) {
  return NAV_ITEMS.filter(item => item.category === category && isEnabled(item));
}

export function getEnabledNavItems() {
  return NAV_ITEMS.filter(isEnabled);
}

export function getCoreNavItems() {
  return getNavItemsByCategory('core');
}

export function getIntelligenceNavItems() {
  return getNavItemsByCategory('intelligence');
}

export function getAnalysisNavItems() {
  return getNavItemsByCategory('analysis');
}

export function getManagementNavItems() {
  return getNavItemsByCategory('management');
}
