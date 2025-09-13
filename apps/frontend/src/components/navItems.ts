export type NavItem = { key: string; href: string; label: string; icon?: string; featureFlag?: string };

export const baseNav: NavItem[] = [
  // existing core nav items could be added here in future
];

export const extraNav: NavItem[] = [
  { key: "agent", href: "/agent", label: "Agent", icon: "MessageSquare", featureFlag: "NEXT_PUBLIC_FEATURE_AGENT" },
  { key: "nlp", href: "/nlp", label: "NLP", icon: "Sparkles", featureFlag: "NEXT_PUBLIC_FEATURE_NLP" },
];

export function isEnabled(item: NavItem) {
  if (!item.featureFlag) return true;
  return process.env[item.featureFlag] === "1" || process.env[item.featureFlag] === "true";
}
