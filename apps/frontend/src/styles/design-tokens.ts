// Design tokens for consistent styling across InfoTerminal
// Centralizes commonly used style patterns to avoid inline CSS

// Navigation and Interactive States
export const navigationStyles = {
  // Sidebar navigation items
  navItem: {
    base: "group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors",
    active:
      "bg-primary-50 text-primary-700 border-r-2 border-primary-600 dark:bg-primary-900/30 dark:text-primary-300",
    inactive:
      "text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-slate-400 dark:hover:bg-gray-800 dark:hover:text-slate-100",
  },

  // Navigation icons
  navIcon: {
    base: "mr-3 transition-colors",
    active: "text-primary-600 dark:text-primary-300",
    inactive:
      "text-gray-400 group-hover:text-gray-500 dark:text-slate-500 dark:group-hover:text-slate-400",
  },

  // Expandable navigation items
  navExpander: {
    button:
      "w-full group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors",
    chevron: "ml-auto transition-transform",
    chevronExpanded: "ml-auto transition-transform rotate-180",
    submenu: "ml-6 space-y-1",
  },

  // Navigation badges
  navBadge:
    "ml-auto bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded-full dark:bg-red-900/30 dark:text-red-300",
};

// Button Variants
export const buttonStyles = {
  // Primary buttons
  primary:
    "inline-flex items-center justify-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-70",

  // Secondary buttons
  secondary:
    "inline-flex items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-900 shadow-sm transition hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100 dark:hover:bg-gray-800",

  // Ghost buttons
  ghost:
    "inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 rounded-lg transition hover:bg-gray-100 hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:text-slate-400 dark:hover:bg-gray-800 dark:hover:text-slate-100",

  // Destructive buttons
  destructive:
    "inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30",

  // Icon-only buttons
  iconOnly:
    "inline-flex h-8 w-8 items-center justify-center rounded-full text-gray-500 transition hover:bg-gray-200 hover:text-gray-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:hover:bg-gray-800",

  // Mobile menu button
  mobileMenu:
    "lg:hidden p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 hover:text-gray-600 dark:text-slate-400 dark:hover:text-slate-300",
};

// Form Input Styles
export const inputStyles = {
  base: "w-full rounded-lg border border-gray-300 bg-white py-2 px-3 text-sm text-gray-900 shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100",
  withIcon:
    "w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100",
  error: "border-red-300 focus:border-red-500 focus:ring-red-500 dark:border-red-700",
  disabled: "cursor-not-allowed opacity-50",
};

// Layout and Container Styles
export const layoutStyles = {
  // Main containers
  pageContainer: "min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-slate-100",
  contentArea: "lg:ml-64",
  sidebarOverlay: "fixed inset-0 z-50 lg:hidden",
  sidebarBackdrop: "fixed inset-0 bg-gray-900/80",

  // Sidebar containers
  mobileSidebar:
    "fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-900 shadow-xl focus:outline-none",
  desktopSidebar:
    "hidden lg:fixed lg:inset-y-0 lg:z-40 lg:flex lg:w-64 lg:flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800",

  // Header styles
  header:
    "sticky top-0 z-30 bg-white/80 dark:bg-gray-900/80 backdrop-blur border-b border-gray-200 dark:border-gray-800",
  headerContent: "flex h-16 items-center justify-between px-4 sm:px-6",
};

// Card and Panel Styles
export const cardStyles = {
  base: "bg-white rounded-lg border border-gray-200 shadow-sm dark:bg-gray-900 dark:border-gray-800",
  padding: "p-6",
  header: "border-b border-gray-200 pb-4 dark:border-gray-800",
  footer: "border-t border-gray-200 pt-4 dark:border-gray-800",
};

// Status and State Indicators
export const statusStyles = {
  // Status badges
  success: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  warning: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  error: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  info: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  neutral: "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300",

  // Loading states
  loading: "animate-pulse bg-gray-200 dark:bg-gray-700",
  skeleton: "animate-pulse bg-gray-200 rounded dark:bg-gray-700",
};

// Typography Styles
export const textStyles = {
  // Headings
  h1: "text-3xl font-bold text-gray-900 dark:text-slate-100",
  h2: "text-2xl font-semibold text-gray-900 dark:text-slate-100",
  h3: "text-lg font-semibold text-gray-900 dark:text-slate-100",
  h4: "text-base font-semibold text-gray-900 dark:text-slate-100",

  // Body text
  body: "text-sm text-gray-600 dark:text-slate-400",
  bodyLarge: "text-base text-gray-600 dark:text-slate-400",
  bodySmall: "text-xs text-gray-500 dark:text-slate-500",

  // Links
  link: "text-primary-600 hover:text-primary-700 focus:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300",
  linkSubtle:
    "text-gray-600 hover:text-gray-900 focus:text-gray-900 dark:text-slate-400 dark:hover:text-slate-100",
};

// Z-index Management
export const zIndexTokens = {
  dropdown: 1000,
  tooltip: 1010,
  overlay: 1050,
  modal: 1100,
  notification: 1200,
};

// Animation and Transition Tokens
export const animationTokens = {
  fast: "transition-colors duration-150",
  normal: "transition-all duration-200",
  slow: "transition-all duration-300",
  slideIn: "transform transition-transform duration-200 ease-in-out",
  fadeIn: "transition-opacity duration-200 ease-in-out",
};

// Spacing tokens (for consistent padding/margin)
export const spacingTokens = {
  xs: "0.25rem", // 1
  sm: "0.5rem", // 2
  md: "0.75rem", // 3
  lg: "1rem", // 4
  xl: "1.5rem", // 6
  "2xl": "2rem", // 8
  "3xl": "3rem", // 12
};

// Utility function to combine styles
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(" ");
}

// Style composition helpers
export const compose = {
  // Combine navigation styles
  navItem: (isActive: boolean, className?: string) =>
    cn(
      navigationStyles.navItem.base,
      isActive ? navigationStyles.navItem.active : navigationStyles.navItem.inactive,
      className,
    ),

  navIcon: (isActive: boolean, className?: string) =>
    cn(
      navigationStyles.navIcon.base,
      isActive ? navigationStyles.navIcon.active : navigationStyles.navIcon.inactive,
      className,
    ),

  // Combine button styles
  button: (variant: keyof typeof buttonStyles, className?: string) =>
    cn(buttonStyles[variant], className),

  // Combine status styles
  status: (status: keyof typeof statusStyles, className?: string) =>
    cn("text-xs font-medium px-2 py-1 rounded-full", statusStyles[status], className),

  // Combine card styles
  card: (className?: string) => cn(cardStyles.base, cardStyles.padding, className),
};
