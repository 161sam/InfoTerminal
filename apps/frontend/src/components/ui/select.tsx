import React, { createContext, useContext, useMemo, useState } from "react";

type SelectContextType = {
  value: string | undefined;
  setValue: (v: string) => void;
  open: boolean;
  setOpen: (o: boolean) => void;
};

const SelectContext = createContext<SelectContextType | null>(null);

export interface SelectProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  children?: React.ReactNode;
}

function Select({ value, defaultValue, onValueChange, children }: SelectProps) {
  const [internal, setInternal] = useState<string | undefined>(defaultValue);
  const [open, setOpen] = useState(false);
  const isControlled = typeof value !== "undefined";
  const current = isControlled ? value : internal;
  const setValue = (v: string) => {
    if (!isControlled) setInternal(v);
    onValueChange?.(v);
    setOpen(false);
  };
  const ctx = useMemo(() => ({ value: current, setValue, open, setOpen }), [current, open]);
  return <SelectContext.Provider value={ctx}>{children}</SelectContext.Provider>;
}

export interface SelectTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}
function SelectTrigger({ className = "", children, onClick, ...props }: SelectTriggerProps) {
  const ctx = useContext(SelectContext);
  if (!ctx) throw new Error("SelectTrigger must be used within <Select>");
  const base =
    "inline-flex items-center justify-between gap-2 rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100";
  return (
    <button
      type="button"
      className={`${base} ${className}`}
      onClick={(e) => {
        onClick?.(e);
        if (!e.defaultPrevented) ctx.setOpen(!ctx.open);
      }}
      {...props}
    >
      {children}
    </button>
  );
}

export interface SelectValueProps {
  placeholder?: string;
}
function SelectValue({ placeholder }: SelectValueProps) {
  const ctx = useContext(SelectContext);
  if (!ctx) throw new Error("SelectValue must be used within <Select>");
  return <span>{ctx.value ?? placeholder ?? "Select"}</span>;
}

export interface SelectContentProps extends React.HTMLAttributes<HTMLDivElement> {}
function SelectContent({ className = "", children, ...props }: SelectContentProps) {
  const ctx = useContext(SelectContext);
  if (!ctx) throw new Error("SelectContent must be used within <Select>");
  if (!ctx.open) return null;
  return (
    <div
      className={`mt-2 w-64 rounded-md border border-gray-200 bg-white p-1 shadow-lg dark:border-gray-700 dark:bg-gray-900 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export interface SelectItemProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  value: string;
}
function SelectItem({ value, className = "", children, onClick, ...props }: SelectItemProps) {
  const ctx = useContext(SelectContext);
  if (!ctx) throw new Error("SelectItem must be used within <Select>");
  const isActive = ctx.value === value;
  const base =
    "flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-800";
  return (
    <button
      type="button"
      role="option"
      aria-selected={isActive}
      className={`${base} ${className}`}
      onClick={(e) => {
        onClick?.(e);
        if (!e.defaultPrevented) ctx.setValue(value);
      }}
      {...props}
    >
      {children}
    </button>
  );
}

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem };
