import React, { useState, useEffect, useRef } from 'react';
import { User, LogOut, Settings, Users, ChevronDown, Shield, Clock } from 'lucide-react';
import { useAuth } from '@/components/auth/AuthProvider';
import { cn } from '@/lib/utils';
import Link from 'next/link';
import LoginModal from './LoginModal';

interface HeaderUserButtonProps {
  className?: string;
}

export const HeaderUserButton: React.FC<HeaderUserButtonProps> = ({ className }) => {
  const { user, logout, loading, isAuthenticated } = useAuth();
  const [showMenu, setShowMenu] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowMenu(false);
      }
    };

    if (showMenu) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showMenu]);

  // Close menu on route change
  useEffect(() => {
    setShowMenu(false);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 p-2 rounded-lg bg-gray-100 dark:bg-gray-800 animate-pulse">
        <div className="w-8 h-8 bg-gray-300 dark:bg-gray-600 rounded-full" />
        <div className="hidden sm:block w-20 h-4 bg-gray-300 dark:bg-gray-600 rounded" />
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return (
      <>
        <button
          onClick={() => setShowLoginModal(true)}
          className={cn(
            "inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors",
            className
          )}
        >
          <User size={16} />
          <span className="hidden sm:inline">Login</span>
        </button>
        
        <LoginModal
          isOpen={showLoginModal}
          onClose={() => setShowLoginModal(false)}
        />
      </>
    );
  }

  const displayName = user.name || user.email?.split('@')[0] || 'User';
  const userInitials = displayName
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  const handleLogout = async () => {
    setShowMenu(false);
    await logout();
  };

  return (
    <div ref={menuRef} className={cn("relative", className)}>
      <button
        onClick={() => setShowMenu(!showMenu)}
        className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
        aria-expanded={showMenu}
        aria-haspopup="true"
      >
        {/* User Avatar */}
        <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          {user.avatar ? (
            <img 
              src={user.avatar} 
              alt={displayName}
              className="w-8 h-8 rounded-full object-cover"
            />
          ) : (
            <span className="text-primary-600 dark:text-primary-400 text-sm font-medium">
              {userInitials}
            </span>
          )}
        </div>
        
        {/* User Info - Desktop */}
        <div className="hidden sm:block text-left min-w-0">
          <div className="text-sm font-medium text-gray-900 dark:text-white truncate">
            {displayName}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
            {user.roles?.[0] || 'User'}
          </div>
        </div>
        
        <ChevronDown 
          size={16} 
          className={cn(
            "text-gray-400 transition-transform duration-200",
            showMenu && "rotate-180"
          )} 
        />
      </button>

      {/* User Dropdown Menu */}
      {showMenu && (
        <div className="absolute right-0 top-full mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 py-2">
          {/* User Profile Header */}
          <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                {user.avatar ? (
                  <img 
                    src={user.avatar} 
                    alt={displayName}
                    className="w-10 h-10 rounded-full object-cover"
                  />
                ) : (
                  <span className="text-primary-600 dark:text-primary-400 font-medium">
                    {userInitials}
                  </span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-medium text-gray-900 dark:text-white truncate">
                  {displayName}
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400 truncate">
                  {user.email}
                </div>
                {user.roles && user.roles.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {user.roles.map(role => (
                      <span
                        key={role}
                        className="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 text-xs rounded-full"
                      >
                        <Shield size={10} />
                        {role}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-1">
            <Link
              href="/settings"
              className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              onClick={() => setShowMenu(false)}
            >
              <Settings size={16} />
              Profile Settings
            </Link>
            
            <Link
              href="/settings?tab=user-management"
              className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              onClick={() => setShowMenu(false)}
            >
              <Users size={16} />
              User Management
            </Link>

            <div className="border-t border-gray-200 dark:border-gray-700 my-1" />

            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              <LogOut size={16} />
              Sign Out
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default HeaderUserButton;
