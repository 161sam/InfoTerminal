import React, { createContext, useContext, useMemo, useState, useCallback } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

type TabsContextType = {
  value: string | undefined;
  setValue: (v: string) => void;
  orientation?: "horizontal" | "vertical";
  variant?: "default" | "pills" | "underline" | "cards";
};

const TabsContext = createContext<TabsContextType | null>(null);

// Tab variants using CVA for consistent styling
const tabsListVariants = cva("inline-flex items-center justify-center", {
  variants: {
    variant: {
      default: "rounded-lg bg-gray-100 dark:bg-gray-800 p-1",
      pills:
        "rounded-full bg-gray-50 dark:bg-gray-900 p-1 border border-gray-200 dark:border-gray-700",
      underline: "border-b border-gray-200 dark:border-gray-700",
      cards: "gap-2",
    },
    orientation: {
      horizontal: "flex-row gap-1",
      vertical: "flex-col gap-2",
    },
  },
  defaultVariants: {
    variant: "default",
    orientation: "horizontal",
  },
});

const tabsTriggerVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap font-medium text-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default:
          "rounded-md px-3 py-2 data-[state=active]:bg-primary-600 data-[state=active]:text-white data-[state=active]:shadow-sm data-[state=inactive]:text-gray-600 data-[state=inactive]:hover:text-gray-900 data-[state=inactive]:hover:bg-gray-50 dark:data-[state=inactive]:text-gray-400 dark:data-[state=inactive]:hover:text-gray-100 dark:data-[state=inactive]:hover:bg-gray-700",
        pills:
          "rounded-full px-4 py-2 data-[state=active]:bg-primary-600 data-[state=active]:text-white data-[state=active]:shadow-sm data-[state=inactive]:text-gray-600 data-[state=inactive]:hover:text-gray-900 data-[state=inactive]:hover:bg-gray-100 dark:data-[state=inactive]:text-gray-400 dark:data-[state=inactive]:hover:text-gray-100 dark:data-[state=inactive]:hover:bg-gray-800",
        underline:
          "border-b-2 border-transparent px-4 py-3 data-[state=active]:border-primary-600 data-[state=active]:text-primary-600 data-[state=inactive]:text-gray-500 data-[state=inactive]:hover:text-gray-700 data-[state=inactive]:hover:border-gray-300 dark:data-[state=active]:text-primary-400 dark:data-[state=active]:border-primary-400 dark:data-[state=inactive]:text-gray-400 dark:data-[state=inactive]:hover:text-gray-300",
        cards:
          "rounded-lg border border-gray-200 dark:border-gray-700 px-4 py-3 data-[state=active]:bg-primary-50 data-[state=active]:border-primary-300 data-[state=active]:text-primary-700 data-[state=inactive]:bg-white data-[state=inactive]:text-gray-600 data-[state=inactive]:hover:bg-gray-50 data-[state=inactive]:hover:border-gray-300 dark:data-[state=active]:bg-primary-900/30 dark:data-[state=active]:border-primary-600 dark:data-[state=active]:text-primary-300 dark:data-[state=inactive]:bg-gray-800 dark:data-[state=inactive]:text-gray-400 dark:data-[state=inactive]:hover:bg-gray-700",
      },
      size: {
        sm: "px-2 py-1 text-xs",
        md: "px-3 py-2 text-sm",
        lg: "px-4 py-3 text-base",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  },
);

export interface TabsProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  orientation?: "horizontal" | "vertical";
  variant?: "default" | "pills" | "underline" | "cards";
}

/**
 * Enhanced Tabs implementation with multiple variants and design consistency.
 * - Controlled via `value`/`onValueChange`, or uncontrolled via `defaultValue`
 * - Supports multiple visual variants: default, pills, underline, cards
 * - Responsive design with horizontal/vertical orientation
 * - Consistent with InfoTerminal design system
 */
function Tabs({
  value,
  defaultValue,
  onValueChange,
  orientation = "horizontal",
  variant = "default",
  className = "",
  children,
  ...props
}: TabsProps) {
  const [internal, setInternal] = useState<string | undefined>(defaultValue);
  const isControlled = typeof value !== "undefined";
  const current = isControlled ? value : internal;

  const setValue = useCallback((v: string) => {
    if (!isControlled) setInternal(v);
    onValueChange?.(v);
  }, [isControlled, onValueChange]);

  const ctx = useMemo(
    () => ({
      value: current,
      setValue,
      orientation,
      variant,
    }),
    [current, orientation, variant, setValue],
  );

  return (
    <TabsContext.Provider value={ctx}>
      <div className={cn("w-full", className)} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

export interface TabsListProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof tabsListVariants> {}

function TabsList({ variant, orientation, className = "", children, ...props }: TabsListProps) {
  const ctx = useContext(TabsContext);
  const actualVariant = variant ?? ctx?.variant ?? "default";
  const actualOrientation = orientation ?? ctx?.orientation ?? "horizontal";

  return (
    <div
      className={cn(
        tabsListVariants({ variant: actualVariant, orientation: actualOrientation }),
        className,
      )}
      role="tablist"
      {...props}
    >
      {children}
    </div>
  );
}

export interface TabsTriggerProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof tabsTriggerVariants> {
  value: string;
  icon?: React.ElementType;
  badge?: string | number;
  description?: string;
}

function TabsTrigger({
  value,
  variant,
  size,
  icon: Icon,
  badge,
  description,
  className = "",
  children,
  onClick,
  ...props
}: TabsTriggerProps) {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error("TabsTrigger must be used within <Tabs>");
  }

  const isActive = ctx.value === value;
  const actualVariant = variant ?? ctx.variant ?? "default";
  const dataState = isActive ? "active" : "inactive";

  return (
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      data-state={dataState}
      onClick={(e) => {
        onClick?.(e);
        if (!e.defaultPrevented) ctx.setValue(value);
      }}
      className={cn(tabsTriggerVariants({ variant: actualVariant, size }), className)}
      {...props}
    >
      <div className="flex items-center gap-2">
        {Icon && <Icon size={size === "sm" ? 14 : size === "lg" ? 20 : 16} />}

        <div className="flex flex-col items-start">
          <span>{children}</span>
          {description && (
            <span className="text-xs opacity-70 font-normal mt-0.5">{description}</span>
          )}
        </div>

        {badge && (
          <span
            className={cn(
              "inline-flex items-center justify-center rounded-full text-xs font-medium min-w-[1.25rem] h-5 px-1",
              isActive
                ? "bg-white/20 text-white"
                : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
            )}
          >
            {badge}
          </span>
        )}
      </div>
    </button>
  );
}

export interface TabsContentProps extends React.HTMLAttributes<HTMLDivElement> {
  value: string;
  forceMount?: boolean;
}

function TabsContent({
  value,
  forceMount = false,
  className = "",
  children,
  ...props
}: TabsContentProps) {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error("TabsContent must be used within <Tabs>");
  }

  const isActive = ctx.value === value;

  if (!isActive && !forceMount) return null;

  return (
    <div
      role="tabpanel"
      data-state={isActive ? "active" : "inactive"}
      className={cn(
        "mt-6 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        !isActive && "hidden",
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

// Helper component for nested tabs
export interface NestedTabsProps extends TabsProps {
  level?: number;
}

function NestedTabs({ level = 1, className, ...props }: NestedTabsProps) {
  return (
    <Tabs
      className={cn(
        level === 1 && "space-y-6",
        level === 2 && "space-y-4",
        level >= 3 && "space-y-2",
        className,
      )}
      {...props}
    />
  );
}

// Pre-configured tab variants for common use cases
export const MainTabs = (props: TabsProps) => <Tabs variant="default" {...props} />;

export const SubTabs = (props: TabsProps) => <Tabs variant="underline" {...props} />;

export const NavigationTabs = (props: TabsProps) => <Tabs variant="pills" {...props} />;

export const CardTabs = (props: TabsProps) => <Tabs variant="cards" {...props} />;

// Export types
export type { TabsContextType };

export {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  NestedTabs,
  tabsListVariants,
  tabsTriggerVariants,
};
