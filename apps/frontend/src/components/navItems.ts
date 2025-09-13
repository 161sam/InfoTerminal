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
} from "lucide-react";

export type NavItem = {
  key: string;
  name: string;
  href: string;
  icon: LucideIcon;
  featureFlag?: string;
  badge?: number;
};

export const NAV_ITEMS: NavItem[] = [
  { key: "dashboard", name: "Dashboard", href: "/", icon: Home },
  { key: "search", name: "Search", href: "/search", icon: Search },
  { key: "graph", name: "Graph", href: "/graphx", icon: Network },
  { key: "agent", name: "Agent", href: "/agent", icon: Bot, featureFlag: "NEXT_PUBLIC_FEATURE_AGENT" },
  { key: "documents", name: "Documents", href: "/documents", icon: FileText },
  { key: "nlp", name: "NLP", href: "/nlp", icon: Sparkles, featureFlag: "NEXT_PUBLIC_FEATURE_NLP" },
  { key: "analytics", name: "Analytics", href: "/analytics", icon: BarChart3 },
  { key: "entities", name: "Entities", href: "/entities", icon: Users },
  { key: "data", name: "Data", href: "/data", icon: Database },
  { key: "security", name: "Security", href: "/security", icon: Shield },
];

export const ff = (k: string) => {
  const v = process.env[k];
  if (v === undefined) return true;
  return v === "1" || v.toLowerCase() === "true";
};

export function isEnabled(item: NavItem) {
  return !item.featureFlag || ff(item.featureFlag);
}
