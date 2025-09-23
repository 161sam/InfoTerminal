import type { LucideIcon } from "lucide-react";
import {
  Home,
  Search,
  Network,
  Brain,
  FileText,
  BarChart3,
  Users,
  Database,
  Bot,
  Sparkles,
  Settings,
  CheckCircle,
  MessageSquare,
  Plug,
  Image,
  Video,
  Music,
  ScanSearch,
} from "lucide-react";

export type NavItem = {
  key: string;
  name: string;
  href: string;
  icon: LucideIcon;
  featureFlag?: string;
  badge?: number;
  description?: string;
  category?: "core" | "analysis" | "intelligence" | "management";
  subItems?: NavItem[];
};

export const NAV_ITEMS: NavItem[] = [
  // Primary navigation (top to bottom)
  {
    key: "dashboard",
    name: "Dashboard",
    href: "/",
    icon: Home,
    description: "System overview and health status",
    category: "core",
  },
  {
    key: "search",
    name: "Search",
    href: "/search",
    icon: Search,
    description: "Search across all data sources and entities",
    category: "core",
  },
  {
    key: "graphx",
    name: "Graph Analysis",
    href: "/graphx",
    icon: Network,
    description: "Entity relationships, 3D visualization, and ML analytics",
    category: "analysis",
    subItems: [
      {
        key: "graph-view",
        name: "Graph View",
        href: "/graphx/graph",
        icon: Network,
        description: "Interactive network exploration",
      },
      {
        key: "viz3d",
        name: "3D Visualization",
        href: "/graphx/viz3d",
        icon: Sparkles,
        description: "deck.gl 3D network rendering",
      },
      {
        key: "ml-analytics",
        name: "ML Analytics",
        href: "/graphx/ml",
        icon: BarChart3,
        description: "PageRank and Node2Vec analysis",
      },
    ],
  },
  {
    key: "nlp",
    name: "NLP Analysis",
    href: "/nlp",
    icon: Brain,
    featureFlag: "NEXT_PUBLIC_FEATURE_NLP",
    description: "Entity extraction, summarization, and domain insights",
    category: "analysis",
  },
  {
    key: "agent",
    name: "AI Agents",
    href: "/agent",
    icon: Bot,
    featureFlag: "NEXT_PUBLIC_FEATURE_AGENT",
    description: "AI-powered investigation and management",
    category: "intelligence",
    subItems: [
      {
        key: "agent-interaction",
        name: "Agent Chat",
        href: "/agent/interaction",
        icon: MessageSquare,
        description: "Interactive AI assistant",
      },
      {
        key: "agent-management",
        name: "Agent Management",
        href: "/agent/management",
        icon: Settings,
        description: "Configure and monitor agents",
      },
    ],
  },
  {
    key: "verification",
    name: "Verification",
    href: "/verification",
    icon: CheckCircle,
    description: "Fact-checking and evidence analysis",
    category: "analysis",
  },
  {
    key: "media-forensics",
    name: "Media Forensics",
    href: "/media-forensics",
    icon: ScanSearch,
    description: "Image, video, and audio forensic analysis",
    category: "analysis",
  },

  {
    key: "entities",
    name: "Entities",
    href: "/entities",
    icon: Users,
    description: "Person and organization profiles",
    category: "analysis",
  },
  {
    key: "analytics",
    name: "Analytics",
    href: "/analytics",
    icon: BarChart3,
    description: "System analytics and reporting",
    category: "management",
  },
  {
    key: "data",
    name: "Data",
    href: "/data",
    icon: Database,
    description: "Import and manage all file types",
    category: "core",
  },
  {
    key: "collab",
    name: "Collaboration",
    href: "/collab",
    icon: Users,
    description: "Real-time collaboration and workspaces",
    category: "management",
  },
  {
    key: "plugins",
    name: "Plugins",
    href: "/plugins",
    icon: Plug,
    description: "Manage available extensions and integrations",
    category: "management",
  },
  {
    key: "settings",
    name: "Settings",
    href: "/settings",
    icon: Settings,
    description: "System configuration and user management",
    category: "management",
  },
];

// Legacy URL mappings for redirects
export const LEGACY_REDIRECTS = {
  "/agents": "/agent?tab=management",
  "/legal": "/nlp?domain=legal",
  "/documents": "/nlp?domain=documents",
  "/ethics": "/nlp?domain=ethics",
  "/forensics": "/nlp?domain=forensics",
  "/graph-ml": "/graphx?tab=ml",
  "/viz3d": "/graphx?tab=viz3d",
  "/verification/media-forensics": "/media-forensics",
};

export const ff = (k: string) => {
  if (typeof window === "undefined") {
    // Server-side: check process.env
    const v = process.env[k];
    if (v === undefined) return true;
    return v === "1" || v.toLowerCase() === "true";
  } else {
    // Client-side: check if feature is available (could be localStorage or other client-side check)
    const v = process.env[k];
    if (v === undefined) return true;
    return v === "1" || v.toLowerCase() === "true";
  }
};

export function isEnabled(item: NavItem) {
  return !item.featureFlag || ff(item.featureFlag);
}

export function getNavItemsByCategory(category: NavItem["category"]) {
  return NAV_ITEMS.filter((item) => item.category === category && isEnabled(item));
}

export function getEnabledNavItems() {
  return NAV_ITEMS.filter(isEnabled);
}

export function getCoreNavItems() {
  return getNavItemsByCategory("core");
}

export function getIntelligenceNavItems() {
  return getNavItemsByCategory("intelligence");
}

export function getAnalysisNavItems() {
  return getNavItemsByCategory("analysis");
}

export function getManagementNavItems() {
  return getNavItemsByCategory("management");
}

export function getMainNavItems() {
  // Return only main navigation items (no subItems) for header/mobile nav
  return NAV_ITEMS.filter((item) => isEnabled(item) && !item.key.includes("-"));
}

export function getCompactNavItems() {
  // Return most important items for mobile bottom navigation
  return [
    NAV_ITEMS.find((item) => item.key === "dashboard"),
    NAV_ITEMS.find((item) => item.key === "search"),
    NAV_ITEMS.find((item) => item.key === "graphx"),
    NAV_ITEMS.find((item) => item.key === "agent"),
    NAV_ITEMS.find((item) => item.key === "verification"),
  ].filter(Boolean) as NavItem[];
}
