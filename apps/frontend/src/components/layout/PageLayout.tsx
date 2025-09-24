import React, { useState } from "react";
import Head from "next/head";
import { useRouter } from "next/router";
import Header from "./Header";
import MobileNavigation from "../mobile/MobileNavigation";
import Breadcrumb, { useBreadcrumbs } from "../navigation/Breadcrumb";
import { useURLBasedState } from "../navigation/URLRouter";

interface PageLayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  showBreadcrumbs?: boolean;
  maxWidth?: "sm" | "md" | "lg" | "xl" | "2xl" | "full";
  padding?: boolean;
  className?: string;
}

const PageLayout: React.FC<PageLayoutProps> = ({
  children,
  title = "InfoTerminal",
  description = "Open Source Intelligence Platform",
  showBreadcrumbs = true,
  maxWidth = "full",
  padding = true,
  className = "",
}) => {
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Extract current page and tab/domain from URL
  const { currentPage, currentTab, currentDomain } = useURLBasedState();

  // Generate breadcrumbs based on current route
  const breadcrumbItems = useBreadcrumbs(router.pathname, currentTab, currentDomain);

  // Get current user (could be from context or props)
  const [currentUser, setCurrentUser] = useState(null);

  const maxWidthClasses = {
    sm: "max-w-sm",
    md: "max-w-md",
    lg: "max-w-lg",
    xl: "max-w-xl",
    "2xl": "max-w-2xl",
    full: "max-w-full",
  };

  const handleMobileMenuToggle = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const fullTitle = title === "InfoTerminal" ? title : `${title} - InfoTerminal`;

  return (
    <>
      <Head>
        <title>{fullTitle}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <Header onMobileMenuClick={handleMobileMenuToggle} />

        {/* Mobile Navigation */}
        <MobileNavigation
          isMenuOpen={isMobileMenuOpen}
          onMenuToggle={handleMobileMenuToggle}
          currentUser={currentUser}
        />

        {/* Main Content */}
        <main
          className={`${maxWidthClasses[maxWidth]} mx-auto ${padding ? "px-4 sm:px-6 lg:px-8" : ""} ${className}`}
        >
          {/* Breadcrumbs */}
          {showBreadcrumbs && breadcrumbItems.length > 1 && (
            <div className="py-4 border-b border-gray-200 dark:border-gray-700 mb-6">
              <Breadcrumb items={breadcrumbItems} className="text-sm" />
            </div>
          )}

          {/* Page Content */}
          <div className={padding ? "py-6" : ""}>{children}</div>
        </main>
      </div>
    </>
  );
};

export default PageLayout;

// Specialized layout for tabbed pages
interface TabbedPageLayoutProps extends PageLayoutProps {
  tabs: Array<{
    key: string;
    label: string;
    icon?: React.ComponentType<any>;
    disabled?: boolean;
  }>;
  activeTab: string;
  onTabChange: (tab: string) => void;
  tabContent?: React.ReactNode;
}

export const TabbedPageLayout: React.FC<TabbedPageLayoutProps> = ({
  tabs,
  activeTab,
  onTabChange,
  tabContent,
  children,
  ...layoutProps
}) => {
  return (
    <PageLayout {...layoutProps}>
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => !tab.disabled && onTabChange(tab.key)}
              disabled={tab.disabled}
              className={`group inline-flex items-center px-1 py-4 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.key
                  ? "border-primary-500 text-primary-600 dark:text-primary-400"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300"
              } ${tab.disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
            >
              {tab.icon && (
                <tab.icon
                  className={`mr-2 h-5 w-5 ${
                    activeTab === tab.key
                      ? "text-primary-500 dark:text-primary-400"
                      : "text-gray-400 group-hover:text-gray-500"
                  }`}
                />
              )}
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {tabContent && <div className="mb-6">{tabContent}</div>}

      {/* Main Content */}
      {children}
    </PageLayout>
  );
};

// Dashboard layout with sidebar
interface DashboardLayoutProps extends PageLayoutProps {
  sidebar?: React.ReactNode;
  sidebarWidth?: "sm" | "md" | "lg";
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  sidebar,
  sidebarWidth = "md",
  children,
  ...layoutProps
}) => {
  const sidebarWidths = {
    sm: "w-64",
    md: "w-80",
    lg: "w-96",
  };

  return (
    <PageLayout {...layoutProps} maxWidth="full" padding={false}>
      <div className="flex h-full">
        {/* Sidebar */}
        {sidebar && (
          <aside
            className={`${sidebarWidths[sidebarWidth]} flex-shrink-0 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800`}
          >
            <div className="h-full overflow-y-auto p-6">{sidebar}</div>
          </aside>
        )}

        {/* Main Content */}
        <div className="flex-1 overflow-hidden">
          <div className="h-full overflow-y-auto p-6">{children}</div>
        </div>
      </div>
    </PageLayout>
  );
};

export type { PageLayoutProps, TabbedPageLayoutProps, DashboardLayoutProps };
