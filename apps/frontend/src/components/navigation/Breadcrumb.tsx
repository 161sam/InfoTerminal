import React from "react";
import { ChevronRight, Home } from "lucide-react";
import Link from "next/link";

interface BreadcrumbItem {
  label: string;
  href?: string;
  active?: boolean;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  showHome?: boolean;
  className?: string;
}

const Breadcrumb: React.FC<BreadcrumbProps> = ({ items, showHome = true, className = "" }) => {
  const allItems = showHome ? [{ label: "Home", href: "/" }, ...items] : items;

  return (
    <nav
      className={`flex items-center space-x-1 text-sm text-gray-600 dark:text-gray-400 ${className}`}
      aria-label="Breadcrumb"
    >
      {allItems.map((item, index) => (
        <React.Fragment key={index}>
          {/* Separator */}
          {index > 0 && (
            <ChevronRight size={16} className="text-gray-400 dark:text-gray-500 flex-shrink-0" />
          )}

          {/* Breadcrumb Item */}
          <div className="flex items-center">
            {/* Home icon for first item */}
            {index === 0 && showHome && (
              <Home size={16} className="mr-1 text-gray-500 dark:text-gray-400" />
            )}

            {/* Link or Text */}
            {item.href && !item.active ? (
              <Link
                href={item.href}
                className="hover:text-gray-900 dark:hover:text-gray-200 transition-colors duration-200 truncate"
              >
                {item.label}
              </Link>
            ) : (
              <span
                className={`truncate ${
                  item.active
                    ? "text-gray-900 dark:text-gray-100 font-medium"
                    : "text-gray-600 dark:text-gray-400"
                }`}
              >
                {item.label}
              </span>
            )}
          </div>
        </React.Fragment>
      ))}
    </nav>
  );
};

export default Breadcrumb;

// Hook for generating breadcrumbs based on current route and tab
export const useBreadcrumbs = (
  basePage: string,
  currentTab?: string,
  domain?: string,
): BreadcrumbItem[] => {
  const hasTabs = (
    c: any,
  ): c is { label: string; tabs: Record<string, string> } & Record<string, unknown> =>
    !!c && typeof c === "object" && (c as any).tabs && typeof (c as any).tabs === "object";

  const hasDomains = (
    c: any,
  ): c is { label: string; domains: Record<string, string> } & Record<string, unknown> =>
    !!c && typeof c === "object" && (c as any).domains && typeof (c as any).domains === "object";

  const pageConfig = {
    "/search": { label: "Search", tabs: {} },
    "/graphx": {
      label: "Graph Analysis",
      tabs: {
        graph: "Graph View",
        viz3d: "3D Visualization",
        ml: "ML Analytics",
      },
    },
    "/nlp": {
      label: "NLP Analysis",
      domains: {
        general: "General",
        legal: "Legal",
        documents: "Documents",
        ethics: "Ethics",
        forensics: "Forensics",
      },
    },
    "/agent": {
      label: "AI Agents",
      tabs: {
        interaction: "Agent Interaction",
        management: "Agent Management",
      },
    },
    "/verification": { label: "Verification", tabs: {} },
    "/security": { label: "Security", tabs: {} },
    "/analytics": { label: "Analytics", tabs: {} },
    "/settings": { label: "Settings", tabs: {} },
    "/collab": { label: "Collaboration", tabs: {} },
  };

  const config = pageConfig[basePage as keyof typeof pageConfig];
  if (!config) return [{ label: "Unknown Page", active: true }];

  const items: BreadcrumbItem[] = [{ label: config.label, href: basePage }];

  // Handle NLP domain-specific breadcrumbs
  if (basePage === "/nlp" && domain && hasDomains(config)) {
    const domainLabel = config.domains[domain as keyof typeof config.domains];
    if (domainLabel) {
      items.push({
        label: domainLabel,
        href: `${basePage}?domain=${domain}`,
        active: true,
      });
    }
  }

  // Handle tab-based breadcrumbs
  if (currentTab && hasTabs(config)) {
    const tabLabel = config.tabs[currentTab as keyof typeof config.tabs];
    if (tabLabel) {
      items.push({
        label: tabLabel,
        href: `${basePage}?tab=${currentTab}`,
        active: true,
      });
    }
  }

  return items;
};

export type { BreadcrumbItem, BreadcrumbProps };
