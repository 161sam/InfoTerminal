import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useRouter } from "next/router";
import { Settings, Menu, X, Bell, User, ChevronRight, Home } from "lucide-react";
import { useNotifications } from "@/lib/notifications";
import { getMainNavItems, getCompactNavItems, type NavItem } from "@/components/navItems";

interface MobileNavigationProps {
  isMenuOpen: boolean;
  onMenuToggle: () => void;
  currentUser?: any;
}

export function MobileNavigation({ isMenuOpen, onMenuToggle, currentUser }: MobileNavigationProps) {
  const router = useRouter();
  const { notifications } = useNotifications();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const mainNavItems = getMainNavItems();
  const compactNavItems = getCompactNavItems();

  // Close menu when route changes
  useEffect(() => {
    onMenuToggle();
  }, [router.pathname, onMenuToggle]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isMenuOpen && !(event.target as Element).closest(".mobile-menu")) {
        onMenuToggle();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isMenuOpen, onMenuToggle]);

  const unreadNotifications = notifications.filter((n) => !n.persistent).length;

  const isActiveRoute = (href: string) => {
    if (href === "/") {
      return router.pathname === "/";
    }
    return router.pathname.startsWith(href);
  };

  const toggleExpanded = (itemKey: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(itemKey)) {
      newExpanded.delete(itemKey);
    } else {
      newExpanded.add(itemKey);
    }
    setExpandedItems(newExpanded);
  };

  const handleNavigation = (href: string) => {
    router.push(href);
    onMenuToggle();
  };

  return (
    <>
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 z-40 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <button
              onClick={onMenuToggle}
              className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100">InfoTerminal</h1>
          </div>

          <div className="flex items-center gap-2">
            <button className="relative p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <Bell size={20} />
              {unreadNotifications > 0 && (
                <span className="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {unreadNotifications > 9 ? "9+" : unreadNotifications}
                </span>
              )}
            </button>
            <div className="h-8 w-8 bg-primary-500 rounded-full flex items-center justify-center">
              {currentUser?.avatar ? (
                <Image
                  src={currentUser.avatar}
                  alt={currentUser.name}
                  width={32}
                  height={32}
                  className="h-8 w-8 rounded-full object-cover"
                  unoptimized
                />
              ) : (
                <User size={16} className="text-white" />
              )}
            </div>
          </div>
        </div>
      </header>
      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-black bg-opacity-50">
          <div className="mobile-menu fixed top-0 left-0 h-full w-80 bg-white dark:bg-gray-800 shadow-xl transform transition-transform">
            {/* Menu Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Navigation</h2>
              <button
                onClick={onMenuToggle}
                className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>

            {/* Navigation Items */}
            <nav className="flex-1 overflow-y-auto p-4 space-y-2">
              {mainNavItems.map((item) => {
                const isActive = isActiveRoute(item.href);
                const hasSubItems = item.subItems && item.subItems.length > 0;
                const isExpanded = expandedItems.has(item.key);

                return (
                  <div key={item.key} className="space-y-1">
                    {/* Main Item */}
                    <div className="flex items-center">
                      <button
                        onClick={() =>
                          hasSubItems ? toggleExpanded(item.key) : handleNavigation(item.href)
                        }
                        className={`flex-1 flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-left ${
                          isActive
                            ? "bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400"
                            : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                        }`}
                      >
                        <item.icon size={20} />
                        <div className="flex-1">
                          <span className="font-medium">{item.name}</span>
                          {item.description && (
                            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                              {item.description}
                            </div>
                          )}
                        </div>
                        {hasSubItems && (
                          <ChevronRight
                            size={16}
                            className={`transition-transform ${isExpanded ? "rotate-90" : ""}`}
                          />
                        )}
                      </button>
                    </div>

                    {/* Sub Items */}
                    {hasSubItems && isExpanded && (
                      <div className="ml-4 space-y-1 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
                        {item.subItems!.map((subItem) => {
                          const isSubActive = isActiveRoute(subItem.href);
                          return (
                            <button
                              key={subItem.key}
                              onClick={() => handleNavigation(subItem.href)}
                              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-left text-sm ${
                                isSubActive
                                  ? "bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400"
                                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50"
                              }`}
                            >
                              <subItem.icon size={16} />
                              <span>{subItem.name}</span>
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>

            {/* Settings */}
            <div className="p-4 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => handleNavigation("/settings")}
                className="w-full flex items-center gap-3 px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <Settings size={20} />
                <span className="font-medium">Settings</span>
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Bottom Tab Navigation */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 shadow-lg">
        <div className="flex items-center justify-around py-2">
          {compactNavItems.map((item) => {
            const isActive = isActiveRoute(item.href);

            return (
              <button
                key={item.key}
                onClick={() => handleNavigation(item.href)}
                className={`flex flex-col items-center gap-1 p-2 min-w-0 flex-1 transition-colors ${
                  isActive
                    ? "text-primary-600 dark:text-primary-400"
                    : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                }`}
              >
                <item.icon size={20} />
                <span className="text-xs font-medium truncate">
                  {item.name === "Graph Analysis"
                    ? "Graph"
                    : item.name === "NLP Analysis"
                      ? "NLP"
                      : item.name === "AI Agents"
                        ? "Agents"
                        : item.name}
                </span>
                {item.badge && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {item.badge > 9 ? "9+" : item.badge}
                  </span>
                )}
              </button>
            );
          })}

          {/* More Button */}
          <button
            onClick={onMenuToggle}
            className="flex flex-col items-center gap-1 p-2 min-w-0 flex-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
          >
            <Menu size={20} />
            <span className="text-xs font-medium">More</span>
          </button>
        </div>
      </nav>
      {/* Content Spacers for Mobile */}
      <div className="lg:hidden h-16" /> {/* Top spacer */}
      <div className="lg:hidden h-16" /> {/* Bottom spacer */}
    </>
  );
}

export default MobileNavigation;
