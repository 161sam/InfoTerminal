// apps/frontend/src/lib/theme-provider.tsx - Enhanced Theme Provider with Dark Mode

import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: 'light' | 'dark';
  isDark: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const THEME_KEY = 'ui.theme';

// Helpers to apply theme instantly to the DOM
const sysPrefersDark = () => (typeof window !== 'undefined') && !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
const applyTheme = (mode: Theme) => {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  const isDark = mode === 'dark' || (mode === 'system' && sysPrefersDark());
  root.classList.toggle('dark', isDark);
  root.setAttribute('data-theme', isDark ? 'dark' : 'light');
  root.setAttribute('data-theme-owner', 'tp');
  document.body?.classList.remove('dark');
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute('content', isDark ? '#1f2937' : '#ffffff');
};

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Load theme from localStorage
    let saved: Theme | null = null;
    try {
      saved = localStorage.getItem(THEME_KEY) as Theme;
    } catch {}
    const initialTheme: Theme = saved && ['light', 'dark', 'system'].includes(saved) ? (saved as Theme) : 'light';
    setTheme(initialTheme);
    // nachdem du initial theme bestimmt hast (light/dark/system)
    applyTheme(initialTheme);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const updateTheme = () => {
      let newResolvedTheme: 'light' | 'dark';
      
      if (theme === 'system') {
        newResolvedTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      } else {
        newResolvedTheme = theme;
      }
      
      setResolvedTheme(newResolvedTheme);
    };

    updateTheme();
    // Also ensure DOM is updated in this pass
    applyTheme(theme);

    // Listen only when user mode is system
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => updateTheme();
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme, mounted]);

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    try { localStorage.setItem(THEME_KEY, newTheme); } catch {}
    // Apply immediately to avoid any flicker
    applyTheme(newTheme);
  };

  const value = {
    theme,
    setTheme: handleSetTheme,
    resolvedTheme,
    isDark: resolvedTheme === 'dark'
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    // Fallback for tests or environments without the provider
    const isDark = typeof document !== 'undefined' && document.documentElement.classList.contains('dark');
    return {
      theme: 'system' as Theme,
      setTheme: () => {},
      resolvedTheme: isDark ? 'dark' : 'light',
      isDark,
    };
  }
  return context;
}

// Enhanced Theme Toggle Component
import { Sun, Moon, Monitor } from 'lucide-react';

interface ThemeToggleProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'button' | 'dropdown';
  showLabel?: boolean;
  className?: string;
}

export function ThemeToggle({ 
  size = 'md', 
  variant = 'button', 
  showLabel = false,
  className = '' 
}: ThemeToggleProps) {
  const { theme, setTheme, resolvedTheme, isDark } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    const sizeClasses = {
      sm: 'w-8 h-8',
      md: 'w-9 h-9', 
      lg: 'w-10 h-10'
    };
    return (
      <div className={`${sizeClasses[size]} rounded-lg bg-gray-200 dark:bg-gray-700 animate-pulse ${className}`} />
    );
  }

  const sizeClasses = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-2.5'
  };

  const iconSizes = {
    sm: 14,
    md: 16,
    lg: 18
  };

  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else if (theme === 'dark') {
      setTheme('system');
    } else {
      setTheme('light');
    }
  };

  const getIcon = () => {
    if (theme === 'system') return <Monitor size={iconSizes[size]} />;
    if (theme === 'dark') return <Moon size={iconSizes[size]} />;
    return <Sun size={iconSizes[size]} />;
  };

  const getLabel = () => {
    if (theme === 'system') return 'System';
    if (theme === 'dark') return 'Dark';
    return 'Light';
  };

  if (variant === 'dropdown') {
    return (
      <div className={`relative ${className}`}>
        <select
          value={theme}
          onChange={(e) => setTheme(e.target.value as Theme)}
          className="pr-8 pl-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 appearance-none"
        >
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="system">System</option>
        </select>
      </div>
    );
  }

  return (
    <button
      onClick={toggleTheme}
      className={`
        ${sizeClasses[size]} rounded-lg border transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
        ${isDark 
          ? 'bg-gray-800 border-gray-600 text-gray-200 hover:bg-gray-700' 
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
        }
        ${showLabel ? 'flex items-center gap-2 px-3' : 'flex items-center justify-center'}
        ${className}
      `}
      title={`Switch to ${theme === 'light' ? 'dark' : theme === 'dark' ? 'system' : 'light'} theme`}
      aria-label={`Current theme: ${getLabel()}. Click to switch theme.`}
    >
      {getIcon()}
      {showLabel && <span className="text-sm font-medium">{getLabel()}</span>}
    </button>
  );
}

// Dark Mode Styles Hook
export function useDarkModeStyles() {
  const { isDark } = useTheme();

  return {
    // Background classes
    bg: {
      primary: isDark ? 'bg-gray-900' : 'bg-white',
      secondary: isDark ? 'bg-gray-800' : 'bg-gray-50',
      tertiary: isDark ? 'bg-gray-700' : 'bg-gray-100',
    },
    // Text classes
    text: {
      primary: isDark ? 'text-gray-100' : 'text-gray-900',
      secondary: isDark ? 'text-gray-300' : 'text-gray-600',
      tertiary: isDark ? 'text-gray-400' : 'text-gray-500',
    },
    // Border classes
    border: {
      default: isDark ? 'border-gray-600' : 'border-gray-300',
      light: isDark ? 'border-gray-700' : 'border-gray-200',
    },
    // Interactive classes
    hover: {
      bg: isDark ? 'hover:bg-gray-700' : 'hover:bg-gray-50',
      text: isDark ? 'hover:text-gray-200' : 'hover:text-gray-700',
    }
  };
}
