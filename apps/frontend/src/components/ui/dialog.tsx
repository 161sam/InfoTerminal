import React, { createContext, useContext, useState } from "react";

type DialogContextType = {
  open: boolean;
  setOpen: (o: boolean) => void;
};

const DialogContext = createContext<DialogContextType | null>(null);

export interface DialogProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  children?: React.ReactNode;
}

function Dialog({ open, defaultOpen, onOpenChange, children }: DialogProps) {
  const [internal, setInternal] = useState<boolean>(!!defaultOpen);
  const isControlled = typeof open !== "undefined";
  const current = isControlled ? !!open : internal;
  const setOpen = (o: boolean) => {
    if (!isControlled) setInternal(o);
    onOpenChange?.(o);
  };

  return (
    <DialogContext.Provider value={{ open: current, setOpen }}>
      {children}
    </DialogContext.Provider>
  );
}

export interface DialogContentProps extends React.HTMLAttributes<HTMLDivElement> {}
function DialogContent({ className = "", children, ...props }: DialogContentProps) {
  const ctx = useContext(DialogContext);
  if (!ctx) throw new Error("DialogContent must be used within <Dialog>");
  if (!ctx.open) return null;
  return (
    <div
      role="dialog"
      aria-modal="true"
      className={`fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40`}
      onClick={() => ctx.setOpen(false)}
    >
      <div
        className={`w-full max-w-lg rounded-md bg-white p-4 shadow-xl dark:bg-gray-900 ${className}`}
        onClick={(e) => e.stopPropagation()}
        {...props}
      >
        {children}
      </div>
    </div>
  );
}

export interface DialogHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}
function DialogHeader({ className = "", ...props }: DialogHeaderProps) {
  return <div className={`mb-2 ${className}`} {...props} />;
}

export interface DialogTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}
function DialogTitle({ className = "", ...props }: DialogTitleProps) {
  return <h2 className={`text-lg font-semibold ${className}`} {...props} />;
}

export interface DialogTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}
function DialogTrigger({ className = "", children, onClick, ...props }: DialogTriggerProps) {
  const ctx = useContext(DialogContext);
  if (!ctx) throw new Error("DialogTrigger must be used within <Dialog>");
  const base =
    "inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100";
  return (
    <button
      type="button"
      className={`${base} ${className}`}
      onClick={(e) => {
        onClick?.(e);
        if (!e.defaultPrevented) ctx.setOpen(true);
      }}
      {...props}
    >
      {children}
    </button>
  );
}

export { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger };
