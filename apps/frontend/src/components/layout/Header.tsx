import React from "react";
import { Menu, ChevronDown } from "lucide-react";
import { useRouter } from "next/router";
import GlobalHealth from "../health/GlobalHealth";
import { getMainNavItems } from "@/components/navItems";
import HeaderUserButton from "@/components/UserLogin/HeaderUserButton";
import { ThemeToggle } from "@/lib/theme-provider";

interface HeaderProps {
  onMobileMenuClick?: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMobileMenuClick }) => {
  const router = useRouter();

  // Get consolidated main navigation items
  const mainNavItems = getMainNavItems();

  const isActiveRoute = (href: string) => {
    if (href === "/") {
      return router.pathname === "/";
    }
    return router.pathname.startsWith(href);
  };

  return (
    <header className="flex items-center justify-between px-6 py-3 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm">
      {/* Logo and Mobile Menu */}
      <div className="flex items-center">
        {/* Mobile Menu Button */}
        <button
          onClick={onMobileMenuClick}
          className="md:hidden mr-3 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <Menu size={20} />
        </button>

        {/* Logo */}
        <a
          href="/"
          className="text-xl font-bold text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
        >
          InfoTerminal
        </a>
        <div className="ml-4 text-sm text-gray-500 dark:text-gray-400">v1.0.0</div>
      </div>

      {/* Main Navigation - Desktop */}
      <nav className="hidden md:flex items-center gap-6">
        {mainNavItems.slice(0, 5).map((item) => (
          <a
            key={item.key}
            href={item.href}
            className={`text-sm font-medium transition-colors ${
              isActiveRoute(item.href)
                ? "text-primary-600 dark:text-primary-400 border-b-2 border-primary-600 dark:border-primary-400 pb-1"
                : "text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
            }`}
            title={item.description}
          >
            {item.name}
          </a>
        ))}

        {/* More dropdown for additional items */}
        {mainNavItems.length > 5 && (
          <div className="relative group">
            <button className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors flex items-center gap-1">
              More
              <ChevronDown size={16} />
            </button>

            {/* Dropdown Menu */}
            <div className="absolute top-full right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div className="py-2">
                {mainNavItems.slice(5).map((item) => (
                  <a
                    key={item.key}
                    href={item.href}
                    className={`flex items-center gap-3 px-4 py-2 text-sm transition-colors ${
                      isActiveRoute(item.href)
                        ? "bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400"
                        : "text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                    }`}
                  >
                    <item.icon size={16} />
                    <div>
                      <div className="font-medium">{item.name}</div>
                      {item.description && (
                        <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                          {item.description}
                        </div>
                      )}
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Right Side - Theme, Health Status and User */}
      <div className="flex items-center gap-4">
        {/* Global Health Status */}
        <GlobalHealth />

        {/* Theme Toggle */}
        <ThemeToggle size="md" />

        {/* User Authentication */}
        <HeaderUserButton />
      </div>
    </header>
  );
};

export default Header;
