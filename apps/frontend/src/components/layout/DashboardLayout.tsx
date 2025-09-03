// apps/frontend/src/components/layout/DashboardLayout.tsx
import React, { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { 
  Search, 
  BarChart3, 
  Network, 
  FileText, 
  Settings, 
  Bell,
  Menu,
  X,
  Home,
  Users,
  Database,
  Shield,
  Activity
} from 'lucide-react';
import GlobalHealth from '../health/GlobalHealth';

interface NavigationItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  badge?: number;
}

const navigation: NavigationItem[] = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Search', href: '/search', icon: Search },
  { name: 'Graph', href: '/graphx', icon: Network },
  { name: 'Documents', href: '/documents', icon: FileText },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Entities', href: '/entities', icon: Users },
  { name: 'Data', href: '/data', icon: Database },
  { name: 'Security', href: '/security', icon: Shield }
];

interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export default function DashboardLayout({ children, title, subtitle }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const router = useRouter();
  // TODO: Layout-Spacings/Typo konsolidieren, sobald Design-Tokens definiert sind.

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-900/80" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-xl">
          <SidebarContent currentPath={router.pathname} onClose={() => setSidebarOpen(false)} />
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-40 lg:flex lg:w-64 lg:flex-col">
        <SidebarContent currentPath={router.pathname} />
      </div>

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top bar */}
        <header className="sticky top-0 z-30 bg-white border-b border-gray-200 shadow-sm">
          <div className="flex h-16 items-center justify-between px-4 sm:px-6">
            <div className="flex items-center gap-4">
              <button
                type="button"
                className="lg:hidden p-2 text-gray-500 hover:text-gray-600"
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
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}

interface SidebarContentProps {
  currentPath: string;
  onClose?: () => void;
}

function SidebarContent({ currentPath, onClose }: SidebarContentProps) {
  return (
    <div className="flex h-full flex-col bg-white border-r border-gray-200">
      {/* Logo */}
      <div className="flex h-16 items-center justify-between px-6 border-b border-gray-200">
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
        {navigation.map((item) => {
          const isActive = currentPath === item.href || 
            (item.href !== '/' && currentPath.startsWith(item.href));
          
          return (
            <Link
              key={item.name}
              href={item.href}
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
        })}
      </nav>

      {/* Footer */}
      <div className="px-3 py-4 border-t border-gray-200">
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
