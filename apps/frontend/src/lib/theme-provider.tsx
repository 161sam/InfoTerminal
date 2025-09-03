// apps/frontend/src/lib/theme-provider.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: 'light' | 'dark';
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme') as Theme;
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  useEffect(() => {
    const root = window.document.documentElement;
    
    const updateTheme = () => {
      let newResolvedTheme: 'light' | 'dark';
      
      if (theme === 'system') {
        newResolvedTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      } else {
        newResolvedTheme = theme;
      }
      
      setResolvedTheme(newResolvedTheme);
      
      root.classList.remove('light', 'dark');
      root.classList.add(newResolvedTheme);
      
      // Update meta theme-color
      const metaThemeColor = document.querySelector('meta[name="theme-color"]');
      if (metaThemeColor) {
        metaThemeColor.setAttribute('content', newResolvedTheme === 'dark' ? '#1f2937' : '#ffffff');
      }
    };

    updateTheme();
    
    // Listen for system theme changes
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addEventListener('change', updateTheme);
      return () => mediaQuery.removeEventListener('change', updateTheme);
    }
  }, [theme]);

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme: handleSetTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// Theme Toggle Component
import { Sun, Moon, Monitor } from 'lucide-react';

export function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="w-9 h-9 rounded-lg bg-gray-200 dark:bg-gray-700 animate-pulse" />
    );
  }

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
    if (theme === 'system') return <Monitor size={16} />;
    if (theme === 'dark') return <Moon size={16} />;
    return <Sun size={16} />;
  };

  return (
    <button
      onClick={toggleTheme}
      className={`
        p-2 rounded-lg border transition-all duration-200 hover:scale-105
        ${resolvedTheme === 'dark' 
          ? 'bg-gray-800 border-gray-700 text-gray-200 hover:bg-gray-700' 
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
        }
      `}
      title={`Switch to ${theme === 'light' ? 'dark' : theme === 'dark' ? 'system' : 'light'} theme`}
    >
      {getIcon()}
    </button>
  );
}

// Extended Tailwind Config for Dark Mode
export const darkModeConfig = `
// tailwind.config.js additions for dark mode
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        // Dark mode specific colors
        dark: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
          950: '#030712',
        }
      }
    }
  }
}`;

// Dark Mode Styles Component
export function DarkModeStyles() {
  return (
    <style jsx global>{`
      /* Dark mode variables */
      :root {
        --color-bg-primary: #ffffff;
        --color-bg-secondary: #f8fafc;
        --color-text-primary: #1f2937;
        --color-text-secondary: #6b7280;
        --color-border: #e5e7eb;
      }

      .dark {
        --color-bg-primary: #1f2937;
        --color-bg-secondary: #111827;
        --color-text-primary: #f9fafb;
        --color-text-secondary: #d1d5db;
        --color-border: #374151;
      }

      /* Smooth transitions for theme changes */
      * {
        transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
      }

      /* Dark mode scrollbars */
      .dark ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
      }

      .dark ::-webkit-scrollbar-track {
        background: #374151;
        border-radius: 4px;
      }

      .dark ::-webkit-scrollbar-thumb {
        background: #6b7280;
        border-radius: 4px;
      }

      .dark ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
      }

      /* Dark mode selection */
      .dark ::selection {
        background: #3b82f6;
        color: white;
      }

      /* Dark mode focus rings */
      .dark *:focus {
        ring-color: #3b82f6;
      }
    `}</style>
  );
}

// Usage in _app.tsx
export function AppWithDarkMode({ Component, pageProps }: any) {
  return (
    <ThemeProvider>
      <DarkModeStyles />
      <Component {...pageProps} />
    </ThemeProvider>
  );
}