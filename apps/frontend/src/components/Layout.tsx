import React from "react";
import Link from "next/link";
import ServiceHealthMatrix from "./ServiceHealthMatrix";

export interface LayoutProps {
  children: React.ReactNode;
  showHealth?: boolean;
}

/**
 * Basic layout with top navigation and centered content container.
 */
const Layout: React.FC<LayoutProps> = ({ children, showHealth }) => {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="container mx-auto flex max-w-7xl items-center justify-between p-4">
          <Link href="/" className="font-semibold">
            InfoTerminal
          </Link>
          <div className="flex items-center gap-4 text-sm">
            <nav className="flex items-center gap-4">
              <Link href="/search">Search</Link>
              <Link href="/graphx">GraphX</Link>
              <Link href="/settings">Settings</Link>
            </nav>
            {showHealth && <ServiceHealthMatrix />}
          </div>
        </div>
      </header>
      <main className="container mx-auto max-w-7xl flex-1 p-6">{children}</main>
      <footer className="border-t">
        <div className="container mx-auto max-w-7xl p-4 text-sm text-gray-500">
          © {new Date().getFullYear()} InfoTerminal
        </div>
      </footer>
    </div>
  );
};

export default Layout;
