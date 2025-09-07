// apps/frontend/src/components/ui/CommandPalette.tsx
import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { useRouter } from 'next/router';
import {
  Search,
  Command,
  ArrowRight,
  Settings,
  Home,
  FileText,
  Network,
  BarChart3,
  Users,
  Database,
  Moon,
  Sun,
  LogOut,
  Plus,
  Upload,
  Download,
  Zap,
  Hash,
  AlertTriangle,
  CheckCircle,
  Info
} from 'lucide-react';
import { useTheme } from '@/lib/theme-provider';
import { useAuth } from '../auth/AuthProvider';
import { useNotifications } from '@/lib/notifications';

// Command types
export interface Command {
  id: string;
  title: string;
  subtitle?: string;
  icon?: React.ComponentType<{ size?: number | string; className?: string }>;
  shortcut?: string[];
  keywords?: string[];
  section?: string;
  action: () => void | Promise<void>;
  condition?: () => boolean;
}

// Keyboard shortcut hook
export function useKeyboardShortcut(
  keys: string[],
  callback: (event: KeyboardEvent) => void,
  deps: React.DependencyList = []
) {
  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      const keyCombo = [];
      
      if (event.ctrlKey || event.metaKey) keyCombo.push('cmd');
      if (event.altKey) keyCombo.push('alt');
      if (event.shiftKey) keyCombo.push('shift');
      keyCombo.push(event.key.toLowerCase());
      
      const shortcut = keyCombo.join('+');
      const targetShortcut = keys.join('+').toLowerCase();
      
      if (shortcut === targetShortcut) {
        event.preventDefault();
        callback(event);
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, deps);
}

// Command Palette Provider
interface CommandPaletteContextType {
  isOpen: boolean;
  open: () => void;
  close: () => void;
  toggle: () => void;
  addCommand: (command: Command) => void;
  removeCommand: (id: string) => void;
  registerShortcut: (keys: string[], action: () => void) => void;
}

const CommandPaletteContext = React.createContext<CommandPaletteContextType | undefined>(undefined);

export function CommandPaletteProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const [customCommands, setCustomCommands] = useState<Command[]>([]);
  
  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);
  const toggle = () => setIsOpen(!isOpen);

  const addCommand = (command: Command) => {
    setCustomCommands(prev => [...prev.filter(c => c.id !== command.id), command]);
  };

  const removeCommand = (id: string) => {
    setCustomCommands(prev => prev.filter(c => c.id !== id));
  };

  const registerShortcut = (keys: string[], action: () => void) => {
    // This would be implemented with a global keyboard listener
    // For now, we'll just log it
    console.log(`Registered shortcut: ${keys.join('+')}`, action);
  };

  // Global keyboard shortcut to open palette
  useKeyboardShortcut(['cmd', 'k'], () => {
    setIsOpen(!isOpen);
  });

  useKeyboardShortcut(['cmd', 'p'], () => {
    setIsOpen(!isOpen);
  });

  // Close on Escape
  useKeyboardShortcut(['escape'], () => {
    if (isOpen) setIsOpen(false);
  });

  const value = {
    isOpen,
    open,
    close,
    toggle,
    addCommand,
    removeCommand,
    registerShortcut,
  };

  return (
    <CommandPaletteContext.Provider value={value}>
      {children}
      <CommandPalette customCommands={customCommands} />
    </CommandPaletteContext.Provider>
  );
}

export function useCommandPalette() {
  const context = React.useContext(CommandPaletteContext);
  if (!context) {
    throw new Error('useCommandPalette must be used within CommandPaletteProvider');
  }
  return context;
}

// Main Command Palette Component
function CommandPalette({ customCommands }: { customCommands: Command[] }) {
  const { isOpen, close } = useCommandPalette();
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const router = useRouter();
  const { setTheme, theme } = useTheme();
  const { user, logout } = useAuth();
  const notifications = useNotifications();

  // Built-in commands
  const builtInCommands: Command[] = useMemo(() => [
    // Navigation
    {
      id: 'nav-home',
      title: 'Go to Dashboard',
      subtitle: 'Navigate to the main dashboard',
      icon: Home,
      shortcut: ['cmd', 'shift', 'h'],
      section: 'Navigation',
      keywords: ['dashboard', 'home', 'main'],
      action: () => {
        router.push('/');
        close();
      }
    },
    {
      id: 'nav-search',
      title: 'Go to Search',
      subtitle: 'Navigate to advanced search',
      icon: Search,
      shortcut: ['cmd', 'shift', 's'],
      section: 'Navigation',
      keywords: ['search', 'find', 'query'],
      action: () => {
        router.push('/search');
        close();
      }
    },
    {
      id: 'nav-graph',
      title: 'Go to Graph Explorer',
      subtitle: 'Navigate to graph visualization',
      icon: Network,
      shortcut: ['cmd', 'shift', 'g'],
      section: 'Navigation',
      keywords: ['graph', 'network', 'visualization', 'nodes'],
      action: () => {
        router.push('/graphx');
        close();
      }
    },
    {
      id: 'nav-documents',
      title: 'Go to Documents',
      subtitle: 'Navigate to document management',
      icon: FileText,
      shortcut: ['cmd', 'shift', 'd'],
      section: 'Navigation',
      keywords: ['documents', 'files', 'upload'],
      action: () => {
        router.push('/documents');
        close();
      }
    },
    {
      id: 'nav-analytics',
      title: 'Go to Analytics',
      subtitle: 'Navigate to analytics dashboard',
      icon: BarChart3,
      section: 'Navigation',
      keywords: ['analytics', 'charts', 'data', 'insights'],
      action: () => {
        router.push('/analytics');
        close();
      }
    },

    // Actions
    {
      id: 'action-upload',
      title: 'Upload Document',
      subtitle: 'Upload a new document',
      icon: Upload,
      shortcut: ['cmd', 'u'],
      section: 'Actions',
      keywords: ['upload', 'document', 'file', 'new'],
      action: () => {
        router.push('/documents#upload');
        close();
      }
    },
    {
      id: 'action-new-search',
      title: 'New Search',
      subtitle: 'Start a new search query',
      icon: Plus,
      shortcut: ['cmd', 'n'],
      section: 'Actions',
      keywords: ['new', 'search', 'query', 'find'],
      action: () => {
        router.push('/search');
        close();
        // Focus search input after navigation
        setTimeout(() => {
          const searchInput = document.querySelector('[data-search-input]') as HTMLInputElement;
          if (searchInput) searchInput.focus();
        }, 100);
      }
    },

    // Settings
    {
      id: 'settings-theme-light',
      title: 'Switch to Light Theme',
      subtitle: 'Change appearance to light mode',
      icon: Sun,
      section: 'Settings',
      keywords: ['theme', 'light', 'appearance'],
      condition: () => theme !== 'light',
      action: () => {
        setTheme('light');
        notifications.success('Theme changed', 'Switched to light mode');
        close();
      }
    },
    {
      id: 'settings-theme-dark',
      title: 'Switch to Dark Theme',
      subtitle: 'Change appearance to dark mode',
      icon: Moon,
      section: 'Settings',
      keywords: ['theme', 'dark', 'appearance'],
      condition: () => theme !== 'dark',
      action: () => {
        setTheme('dark');
        notifications.success('Theme changed', 'Switched to dark mode');
        close();
      }
    },
    {
      id: 'settings-theme-system',
      title: 'Use System Theme',
      subtitle: 'Follow system appearance setting',
      icon: Settings,
      section: 'Settings',
      keywords: ['theme', 'system', 'auto', 'appearance'],
      condition: () => theme !== 'system',
      action: () => {
        setTheme('system');
        notifications.success('Theme changed', 'Following system preference');
        close();
      }
    },
    {
      id: 'settings-open',
      title: 'Open Settings',
      subtitle: 'Open application settings',
      icon: Settings,
      shortcut: ['cmd', ','],
      section: 'Settings',
      keywords: ['settings', 'preferences', 'config'],
      action: () => {
        router.push('/settings');
        close();
      }
    },

    // User Actions
    {
      id: 'user-logout',
      title: 'Sign Out',
      subtitle: 'Sign out of your account',
      icon: LogOut,
      section: 'Account',
      keywords: ['logout', 'sign out', 'exit'],
      condition: () => !!user,
      action: () => {
        logout();
        close();
      }
    },

    // System
    {
      id: 'system-shortcuts',
      title: 'Show Keyboard Shortcuts',
      subtitle: 'View all available shortcuts',
      icon: Command,
      shortcut: ['cmd', '/'],
      section: 'System',
      keywords: ['shortcuts', 'keyboard', 'help', 'commands'],
      action: () => {
        // This would open a shortcuts modal
        notifications.info('Keyboard Shortcuts', 'Cmd+K: Command Palette, Cmd+/: This help');
        close();
      }
    }
  ].filter((cmd) => !cmd.condition || cmd.condition()), [
    router,
    close,
    theme,
    user,
    setTheme,
    logout,
    notifications,
  ]);

  // Combine all commands
  const allCommands = [...builtInCommands, ...customCommands];

  // Filter and search commands
  const filteredCommands = useMemo(() => {
    if (!query.trim()) return allCommands;
    
    const searchTerm = query.toLowerCase();
    return allCommands.filter(command => {
      return (
        command.title.toLowerCase().includes(searchTerm) ||
        command.subtitle?.toLowerCase().includes(searchTerm) ||
        command.keywords?.some(keyword => keyword.toLowerCase().includes(searchTerm)) ||
        command.section?.toLowerCase().includes(searchTerm)
      );
    });
  }, [query, allCommands]);

  // Group commands by section
  const groupedCommands = useMemo(() => {
    const groups: Record<string, Command[]> = {};
    filteredCommands.forEach(command => {
      const section = command.section || 'Other';
      if (!groups[section]) groups[section] = [];
      groups[section].push(command);
    });
    return groups;
  }, [filteredCommands]);

  // Keyboard navigation
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setSelectedIndex(prev => (prev + 1) % filteredCommands.length);
          break;
        case 'ArrowUp':
          e.preventDefault();
          setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % filteredCommands.length);
          break;
        case 'Enter':
          e.preventDefault();
          if (filteredCommands[selectedIndex]) {
            filteredCommands[selectedIndex].action();
          }
          break;
        case 'Tab':
          e.preventDefault();
          setSelectedIndex(prev => (prev + 1) % filteredCommands.length);
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, filteredCommands, selectedIndex]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
      setQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  // Scroll selected item into view
  useEffect(() => {
    if (listRef.current) {
      const selectedElement = listRef.current.children[selectedIndex] as HTMLElement;
      if (selectedElement) {
        selectedElement.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [selectedIndex]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-start justify-center pt-[10vh]">
      <div className="w-full max-w-2xl mx-4 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        
        {/* Search Input */}
        <div className="flex items-center gap-3 p-4 border-b border-gray-200 dark:border-gray-700">
          <Search size={20} className="text-gray-400" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command or search..."
            className="flex-1 bg-transparent text-gray-900 dark:text-gray-100 placeholder-gray-500 outline-none text-lg"
          />
          <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
            <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">↑↓</kbd>
            <span>to navigate</span>
          </div>
        </div>

        {/* Results */}
        <div ref={listRef} className="max-h-96 overflow-y-auto">
          {filteredCommands.length === 0 ? (
            <div className="p-8 text-center text-gray-500 dark:text-gray-400">
              <Search size={48} className="mx-auto mb-4 opacity-50" />
              <p>No commands found</p>
              <p className="text-sm mt-1">Try a different search term</p>
            </div>
          ) : (
            Object.entries(groupedCommands).map(([section, commands]) => (
              <div key={section}>
                <div className="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide bg-gray-50 dark:bg-gray-700/50 sticky top-0">
                  {section}
                </div>
                {commands.map((command, index) => {
                  const globalIndex = filteredCommands.indexOf(command);
                  return (
                    <CommandItem
                      key={command.id}
                      command={command}
                      selected={globalIndex === selectedIndex}
                      onClick={() => command.action()}
                    />
                  );
                })}
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <kbd className="px-2 py-1 bg-white dark:bg-gray-600 rounded border">↵</kbd>
              <span>to select</span>
            </div>
            <div className="flex items-center gap-1">
              <kbd className="px-2 py-1 bg-white dark:bg-gray-600 rounded border">esc</kbd>
              <span>to close</span>
            </div>
          </div>
          <span>{filteredCommands.length} commands</span>
        </div>
      </div>
    </div>
  );
}

// Individual Command Item
function CommandItem({ 
  command, 
  selected, 
  onClick 
}: { 
  command: Command; 
  selected: boolean; 
  onClick: () => void; 
}) {
  const Icon = command.icon || Hash;

  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 text-left transition-colors ${
        selected 
          ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' 
          : 'hover:bg-gray-50 dark:hover:bg-gray-700/50 text-gray-900 dark:text-gray-100'
      }`}
    >
      <div className={`p-2 rounded-lg ${
        selected 
          ? 'bg-primary-100 dark:bg-primary-800/50 text-primary-600 dark:text-primary-400' 
          : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
      }`}>
        <Icon size={16} />
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <p className="font-medium truncate">{command.title}</p>
          {command.shortcut && (
            <div className="flex items-center gap-1 ml-4">
              {command.shortcut.map((key, i) => (
                <React.Fragment key={key}>
                  {i > 0 && <span className="text-gray-400">+</span>}
                  <kbd className="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded text-xs font-mono">
                    {key === 'cmd' ? '⌘' : key === 'shift' ? '⇧' : key === 'alt' ? '⌥' : key.toUpperCase()}
                  </kbd>
                </React.Fragment>
              ))}
            </div>
          )}
        </div>
        {command.subtitle && (
          <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
            {command.subtitle}
          </p>
        )}
      </div>
      
      {selected && <ArrowRight size={16} className="text-gray-400" />}
    </button>
  );
}

// Hook to register commands dynamically
export function useCommand(command: Command, deps: React.DependencyList = []) {
  const { addCommand, removeCommand } = useCommandPalette();

  useEffect(() => {
    addCommand(command);
    return () => removeCommand(command.id);
  }, deps);
}

// Quick Actions Helper
export function useQuickActions() {
  const { addCommand } = useCommandPalette();
  const notifications = useNotifications();

  const addQuickAction = useCallback((
    id: string,
    title: string,
    action: () => void,
    options?: Partial<Command>
  ) => {
    addCommand({
      id: `quick-${id}`,
      title,
      section: 'Quick Actions',
      action,
      ...options
    });
  }, [addCommand]);

  const showSuccess = useCallback((title: string, message?: string) => {
    notifications.success(title, message);
  }, [notifications]);

  const showError = useCallback((title: string, message?: string) => {
    notifications.error(title, message);
  }, [notifications]);

  const showWarning = useCallback((title: string, message?: string) => {
    notifications.warning(title, message);
  }, [notifications]);

  const showInfo = useCallback((title: string, message?: string) => {
    notifications.info(title, message);
  }, [notifications]);

  return {
    addQuickAction,
    showSuccess,
    showError,
    showWarning,
    showInfo
  };
}