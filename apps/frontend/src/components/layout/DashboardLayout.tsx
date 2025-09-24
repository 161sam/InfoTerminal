// apps/frontend/src/components/layout/DashboardLayout.tsx
import React, { useEffect, useRef, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Settings, Bell, Menu, X, Activity, ChevronDown } from "lucide-react";
import GlobalHealth from "../health/GlobalHealth";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import { NAV_ITEMS, isEnabled, type NavItem } from "@/components/navItems";
import HeaderUserButton from "@/components/UserLogin/HeaderUserButton";
import { layoutStyles, buttonStyles, navigationStyles, compose } from "@/styles/design-tokens";

const navigation = NAV_ITEMS.filter((item) => isEnabled(item) && item.key !== "settings");

interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export default function DashboardLayout({ children, title, subtitle }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const router = useRouter();

  return (
    <div className={layoutStyles.pageContainer}>
      {/* Sidebar state management effects */}
      {(() => {
        // eslint-disable-next-line react-hooks/rules-of-hooks
        useEffect(() => {
          if (sidebarOpen) {
            const onKey = (e: KeyboardEvent) => {
              if (e.key === "Escape") setSidebarOpen(false);
            };
            document.addEventListener("keydown", onKey);
            const prevOverflow = document.body.style.overflow;
            document.body.style.overflow = "hidden";
            // focus first focusable in dialog
            setTimeout(() => {
              const el = dialogRef.current?.querySelector<HTMLElement>(
                'a,button,[tabindex]:not([tabindex="-1"])',
              );
              el?.focus();
            }, 0);
            return () => {
              document.removeEventListener("keydown", onKey);
              document.body.style.overflow = prevOverflow;
            };
          }
        }, [sidebarOpen]);
        return null;
      })()}

      {/* Mobile sidebar */}
      <div
        className={`${layoutStyles.sidebarOverlay} ${sidebarOpen ? "block" : "hidden"}`}
        aria-hidden={!sidebarOpen}
      >
        <div
          className={layoutStyles.sidebarBackdrop}
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
        <div
          id="mobile-sidebar"
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
          aria-label="Sidebar"
          className={layoutStyles.mobileSidebar}
        >
          <SidebarContent
            items={navigation}
            currentPath={router.pathname}
            onClose={() => setSidebarOpen(false)}
          />
        </div>
      </div>

      {/* Desktop sidebar */}
      <aside
        id="app-sidebar"
        role="navigation"
        aria-label="Sidebar"
        className={layoutStyles.desktopSidebar}
      >
        <SidebarContent items={navigation} currentPath={router.pathname} />
      </aside>

      {/* Main content */}
      <div className={layoutStyles.contentArea}>
        {/* Top bar */}
        <header role="banner" className={layoutStyles.header}>
          <div className={layoutStyles.headerContent}>
            <div className="flex items-center gap-4">
              <button
                type="button"
                className={buttonStyles.mobileMenu}
                aria-label="Open sidebar"
                aria-controls="mobile-sidebar"
                aria-expanded={sidebarOpen}
                onClick={() => setSidebarOpen(true)}
              >
                <Menu size={20} />
              </button>

              {title && (
                <div>
                  <h1 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
                    {title}
                  </h1>
                  {subtitle && (
                    <p className="text-sm text-gray-500 dark:text-slate-400">{subtitle}</p>
                  )}
                </div>
              )}
            </div>

            <div className="flex items-center gap-3">
              <GlobalHealth />

              <button
                type="button"
                className={buttonStyles.iconOnly}
                aria-label="View notifications"
              >
                <Bell size={20} />
              </button>

              <ThemeToggle />
              <HeaderUserButton />
            </div>
          </div>
        </header>

        {/* Page content */}
        <main role="main" className="flex-1 px-4 py-6 sm:px-6">
          {children}
        </main>
      </div>
    </div>
  );
}

interface SidebarContentProps {
  items: NavItem[];
  currentPath: string;
  onClose?: () => void;
}

function SidebarContent({ items, currentPath, onClose }: SidebarContentProps) {
  const [pluginsOpen, setPluginsOpen] = useState(false);
  const [plugins] = useState([
    { name: "osint-toolkit", displayName: "OSINT Toolkit" },
    { name: "sentiment-analysis", displayName: "Sentiment Analysis" },
    { name: "threat-intelligence", displayName: "Threat Intelligence" },
  ]);

  const resolvedPath = typeof currentPath === "string" ? currentPath : "";

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center gap-3">
          <Activity size={24} className="text-primary-600 dark:text-primary-400" />
          <span className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            InfoTerminal
          </span>
        </div>
        {onClose && (
          <button
            type="button"
            className={buttonStyles.iconOnly}
            aria-label="Close sidebar"
            onClick={onClose}
          >
            <X size={20} />
          </button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {items.map((item) => {
          const isActive =
            resolvedPath === item.href ||
            (item.subItems && item.subItems.some((sub) => resolvedPath.startsWith(sub.href ?? "")));
          const cp = resolvedPath;

          // Special handling for plugins
          if (item.key === "plugins") {
            const isPluginsActive = isActive || cp.startsWith("/plugins");
            return (
              <div key={item.key} className="mt-1 space-y-1">
                <button
                  type="button"
                  aria-expanded={pluginsOpen}
                  onClick={() => {
                    const nextOpen = !pluginsOpen;
                    setPluginsOpen(nextOpen);
                    // Also navigate to plugins page
                    window.location.href = item.href;
                    onClose?.();
                  }}
                  className={compose.navItem(isPluginsActive, navigationStyles.navExpander.button)}
                >
                  <item.icon size={20} className={compose.navIcon(isPluginsActive)} />
                  <span className="flex-1 text-left">{item.name}</span>
                  <ChevronDown
                    size={16}
                    className={
                      pluginsOpen
                        ? navigationStyles.navExpander.chevronExpanded
                        : navigationStyles.navExpander.chevron
                    }
                  />
                </button>
                {pluginsOpen && (
                  <div className={navigationStyles.navExpander.submenu}>
                    {plugins.map((p) => {
                      const childActive = cp === `/plugins/${p.name}`;
                      return (
                        <Link
                          key={p.name}
                          href={`/plugins/${p.name}`}
                          onClick={onClose}
                          className={compose.navItem(childActive, "block px-3 py-1.5 text-sm")}
                        >
                          {p.displayName}
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          }

          return (
            <Link
              key={item.name}
              href={item.href}
              onClick={onClose}
              className={compose.navItem(isActive)}
            >
              <item.icon size={20} className={compose.navIcon(isActive)} />
              {item.name}
              {item.badge && <span className={navigationStyles.navBadge}>{item.badge}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-3 py-4 border-t border-gray-200 dark:border-gray-800">
        <Link href="/settings" className={compose.navItem(false)}>
          <Settings size={20} className={compose.navIcon(false)} />
          Settings
        </Link>
      </div>
    </div>
  );
}
