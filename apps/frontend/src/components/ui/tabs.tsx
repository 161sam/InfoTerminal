import React, { createContext, useContext, useMemo, useState } from "react";

type TabsContextType = {
  value: string | undefined;
  setValue: (v: string) => void;
};

const TabsContext = createContext<TabsContextType | null>(null);

export interface TabsProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
}

/**
 * Lightweight Tabs implementation (no external deps) compatible with our usage.
 * - Controlled via `value`/`onValueChange`, or uncontrolled via `defaultValue`.
 * - Structure: <Tabs><TabsList><TabsTrigger/></TabsList><TabsContent/></Tabs>
 */
function Tabs({ value, defaultValue, onValueChange, className = "", children, ...props }: TabsProps) {
  const [internal, setInternal] = useState<string | undefined>(defaultValue);
  const isControlled = typeof value !== "undefined";
  const current = isControlled ? value : internal;

  const setValue = (v: string) => {
    if (!isControlled) setInternal(v);
    onValueChange?.(v);
  };

  const ctx = useMemo(() => ({ value: current, setValue }), [current]);

  return (
    <TabsContext.Provider value={ctx}>
      <div className={`w-full ${className}`} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

export interface TabsListProps extends React.HTMLAttributes<HTMLDivElement> {}
function TabsList({ className = "", children, ...props }: TabsListProps) {
  return (
    <div className={`inline-flex items-center gap-2 ${className}`} {...props}>
      {children}
    </div>
  );
}

export interface TabsTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  value: string;
}
function TabsTrigger({ value, className = "", children, onClick, ...props }: TabsTriggerProps) {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error("TabsTrigger must be used within <Tabs>");
  }
  const isActive = ctx.value === value;

  const base = "px-3 py-1.5 rounded-md text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary-500";
  const active = "bg-primary-600 text-white hover:bg-primary-700";
  const inactive = "bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-800 dark:text-slate-200 dark:hover:bg-gray-700";

  return (
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      onClick={(e) => {
        onClick?.(e);
        if (!e.defaultPrevented) ctx.setValue(value);
      }}
      className={`${base} ${isActive ? active : inactive} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export interface TabsContentProps extends React.HTMLAttributes<HTMLDivElement> {
  value: string;
}
function TabsContent({ value, className = "", children, ...props }: TabsContentProps) {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error("TabsContent must be used within <Tabs>");
  }

  if (ctx.value !== value) return null;

  return (
    <div role="tabpanel" className={className} {...props}>
      {children}
    </div>
  );
}

export { Tabs, TabsList, TabsTrigger, TabsContent };

