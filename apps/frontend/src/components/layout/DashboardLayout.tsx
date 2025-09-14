// apps/frontend/src/components/layout/DashboardLayout.tsx
import React, { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import {
  Settings,
  Bell,
  Menu,
  X,
  Activity,
  Plug,
  ChevronDown,
} from 'lucide-react';
import GlobalHealth from '../health/GlobalHealth';
import { ThemeToggle } from '@/components/layout/ThemeToggle';
import { NAV_ITEMS, isEnabled, type NavItem } from '@/components/navItems';

const navigation = NAV_ITEMS.filter(isEnabled);

interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export default function DashboardLayout({ children, title, subtitle }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const router = useRouter();
  // TODO: Layout-Spacings/Typo konsolidieren, sobald Design-Tokens definiert sind.

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-slate-100">
      {/* Accessibility: lock scroll and close on Escape when open */}
      {/** Side effects for open state */}
      {(() => {
        // run effect-like block safely in render (no hooks inside conditionals)
        return null;
      })()}
      
      {/* manage body scroll + escape */}
      { /* eslint-disable react-hooks/rules-of-hooks */ }
      { (function useSidebarA11y() {
        useEffect(() => {
          if (sidebarOpen) {
            const onKey = (e: KeyboardEvent) => {
              if (e.key === 'Escape') setSidebarOpen(false);
            };
            document.addEventListener('keydown', onKey);
            const prevOverflow = document.body.style.overflow;
            document.body.style.overflow = 'hidden';
            // focus first focusable in dialog
            setTimeout(() => {
              const el = dialogRef.current?.querySelector<HTMLElement>('a,button,[tabindex]:not([tabindex="-1"])');
              el?.focus();
            }, 0);
            return () => {
              document.removeEventListener('keydown', onKey);
              document.body.style.overflow = prevOverflow;
            };
          }
        }, [sidebarOpen]);
        return null as any;
      })() }
      { /* eslint-enable react-hooks/rules-of-hooks */ }
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`} aria-hidden={!sidebarOpen}>
        <div className="fixed inset-0 bg-gray-900/80" onClick={() => setSidebarOpen(false)} aria-hidden="true" />
        <div
          id="mobile-sidebar"
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
          aria-label="Sidebar"
          className="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-900 shadow-xl focus:outline-none"
        >
          <SidebarContent items={navigation} currentPath={router.pathname} onClose={() => setSidebarOpen(false)} />
        </div>
      </div>

      {/* Desktop sidebar */}
      <aside
        id="app-sidebar"
        role="navigation"
        aria-label="Sidebar"
        className="hidden lg:fixed lg:inset-y-0 lg:z-40 lg:flex lg:w-64 lg:flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800"
      >
        <SidebarContent items={navigation} currentPath={router.pathname} />
      </aside>

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top bar */}
        <header role="banner" className="sticky top-0 z-30 bg-white/80 dark:bg-gray-900/80 backdrop-blur border-b border-gray-200 dark:border-gray-800">
          <div className="flex h-16 items-center justify-between px-4 sm:px-6">
            <div className="flex items-center gap-4">
              <button
                type="button"
                className="lg:hidden p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 hover:text-gray-600"
                aria-label="Open sidebar"
                aria-controls="mobile-sidebar"
                aria-expanded={sidebarOpen}
                onClick={() => setSidebarOpen(true)}
              >
                <Menu size={20} />
              </button>
              <div>
                {title && <h1 className="text-xl font-semibold text-gray-900">{title}</h1>}
                {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
              </div>
            </div>

            <div className="flex items-center gap-4">
              <GlobalHealth />
              <ThemeToggle />
              <button className="relative p-2 text-gray-500 hover:text-gray-600">
                <Bell size={20} />
                <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400" />
              </button>
              <div className="h-6 w-px bg-gray-200" />
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center">
                  <span className="text-sm font-medium text-white">A</span>
                </div>
                <span className="text-sm font-medium text-gray-700">Admin User</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main role="main" className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}

interface SidebarContentProps {
  items: NavItem[];
  currentPath?: string;
  onClose?: () => void;
}

function SidebarContent({ items, currentPath, onClose }: SidebarContentProps) {
  const router = useRouter();
  const [plugins, setPlugins] = useState<{ name: string }[]>([]);
  const [open, setOpen] = useState(() => currentPath?.startsWith('/plugins'));

  useEffect(() => {
    fetch('/api/plugins/state')
      .then((r) => r.json())
      .then((d) => {
        const active = (d.items || []).filter((p: any) => p.enabled !== false);
        setPlugins(active);
      })
      .catch(() => setPlugins([]));
  }, []);

  const cp = currentPath || '';

  return (
    <div className="flex h-full flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800">
      {/* Logo */}
      <div className="flex h-16 items-center justify-between px-6 border-b border-gray-200 dark:border-gray-800">
        <Link href="/" className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-primary-600 flex items-center justify-center">
            <Activity size={20} className="text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900">InfoTerminal</span>
        </Link>
        {onClose && (
          <button onClick={onClose} className="lg:hidden p-1 text-gray-500">
            <X size={20} />
          </button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {items.map((item) => {
          const isActive = cp === item.href || (item.href !== '/' && cp.startsWith(item.href));

          const link = (
            <Link
              key={item.name}
              href={item.href}
              onClick={onClose}
              className={`
                group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors
                ${isActive
                  ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }
              `}
            >
              <item.icon
                size={20}
                className={`mr-3 ${isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-500'}`}
              />
              {item.name}
              {item.badge && (
                <span className="ml-auto bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded-full">
                  {item.badge}
                </span>
              )}
            </Link>
          );

          if (item.key === 'security') {
            return (
              <React.Fragment key={item.key}>
                {link}
                <div className="mt-1">
                  <button
                    type="button"
                    onClick={() => {
                      setOpen(!open);
                      router.push('/plugins');
                      onClose?.();
                    }}
                    className={`
                      w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors
                      ${cp.startsWith('/plugins')
                        ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }
                    `}
                  >
                    <Plug size={20} className="mr-3" />
                    <span className="flex-1 text-left">Plugins</span>
                    <ChevronDown
                      size={16}
                      className={`ml-auto transition-transform ${open ? 'rotate-180' : ''}`}
                    />
                  </button>
                  {open && (
                    <div className="mt-1 ml-6 space-y-1">
                      {plugins.map((p) => {
                        const childActive = cp === `/plugins/${p.name}`;
                        return (
                          <Link
                            key={p.name}
                            href={`/plugins/${p.name}`}
                            onClick={onClose}
                            className={`
                              block px-3 py-1.5 text-sm rounded-lg transition-colors
                              ${childActive
                                ? 'bg-primary-50 text-primary-700'
                                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                              }
                            `}
                          >
                            {p.name}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              </React.Fragment>
            );
          }

          return link;
        })}
      </nav>

      {/* Footer */}
      <div className="px-3 py-4 border-t border-gray-200 dark:border-gray-800">
        <Link
          href="/settings"
          className="group flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-lg transition-colors"
        >
          <Settings size={20} className="mr-3 text-gray-400 group-hover:text-gray-500" />
          Settings
        </Link>
      </div>
    </div>
  );
}
