// Enhanced Dialog component with viewport guards and responsive positioning
"use client";

import React, { createContext, useContext, useState, useEffect, useRef } from "react";
import { createPortal } from "react-dom";

// Z-index tokens for consistent layering
const Z_INDEX = {
  overlay: 1050,
  dialog: 1100,
} as const;

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
    <DialogContext.Provider value={{ open: current, setOpen }}>{children}</DialogContext.Provider>
  );
}

export interface DialogContentProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl" | "full";
  placement?: "center" | "top" | "bottom";
}

function DialogContent({
  className = "",
  children,
  size = "md",
  placement = "center",
  ...props
}: DialogContentProps) {
  const ctx = useContext(DialogContext);
  const dialogRef = useRef<HTMLDivElement>(null);

  if (!ctx) throw new Error("DialogContent must be used within <Dialog>");

  const { open, setOpen } = ctx;
  const isBrowser = typeof window !== "undefined" && typeof document !== "undefined";

  // Size variants with responsive design
  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
    full: "max-w-[90vw]",
  };

  // Placement variants with viewport guards
  const placementClasses = {
    center: "top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2",
    top: "top-4 left-1/2 -translate-x-1/2 md:top-8",
    bottom: "bottom-4 left-1/2 -translate-x-1/2 md:bottom-8",
  };

  // Viewport guards for responsive max height
  const getMaxHeight = () => {
    if (typeof window === "undefined") return "85vh";

    const vh = window.innerHeight;
    const padding = placement === "center" ? 80 : 32; // More padding for center placement

    return `${Math.min(vh - padding, vh * 0.9)}px`;
  };

  // Focus trap and keyboard handling
  useEffect(() => {
    if (!isBrowser || !open) {
      return;
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
      }

      // Focus trap
      if (e.key === "Tab") {
        const dialog = dialogRef.current;
        if (!dialog) return;

        const focusableElements = dialog.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        );
        const firstElement = focusableElements[0] as HTMLElement;
        const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement?.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement?.focus();
          }
        }
      }
    };

    // Position adjustment for viewport guards
    const adjustPosition = () => {
      const dialog = dialogRef.current;
      if (!dialog) return;

      const rect = dialog.getBoundingClientRect();
      const viewport = {
        width: window.innerWidth,
        height: window.innerHeight,
      };

      // Check if dialog is outside viewport bounds
      if (rect.right > viewport.width - 16) {
        dialog.style.left = `${viewport.width - rect.width - 16}px`;
        dialog.style.transform = "translateY(-50%)";
      }

      if (rect.bottom > viewport.height - 16) {
        dialog.style.top = `${viewport.height - rect.height - 16}px`;
        dialog.style.transform = "translateX(-50%)";
      }

      if (rect.left < 16) {
        dialog.style.left = "16px";
        dialog.style.transform = "translateY(-50%)";
      }

      if (rect.top < 16) {
        dialog.style.top = "16px";
        dialog.style.transform = "translateX(-50%)";
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    window.addEventListener("resize", adjustPosition);

    // Prevent body scroll when dialog is open
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    // Focus first focusable element and adjust position
    const timer = window.setTimeout(() => {
      const dialog = dialogRef.current;
      if (dialog) {
        adjustPosition();
        const firstFocusable = dialog.querySelector(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        ) as HTMLElement;
        firstFocusable?.focus();
      }
    }, 100);

    return () => {
      clearTimeout(timer);
      document.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("resize", adjustPosition);
      document.body.style.overflow = originalOverflow;
    };
  }, [isBrowser, open, setOpen, placement]);

  if (!isBrowser || !open) return null;

  return createPortal(
    <>
      <div
        className="fixed inset-0 bg-black/40 backdrop-blur-sm"
        style={{ zIndex: Z_INDEX.overlay }}
        onClick={() => setOpen(false)}
      />
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        className={`fixed ${placementClasses[placement]} w-full ${sizeClasses[size]} rounded-2xl bg-white shadow-xl outline-none dark:bg-gray-900 ${className}`}
        style={{
          zIndex: Z_INDEX.dialog,
          maxHeight: getMaxHeight(),
        }}
        onClick={(e) => e.stopPropagation()}
        {...props}
      >
        <div className="flex h-full max-h-full flex-col overflow-hidden">{children}</div>
      </div>
    </>,
    document.body,
  );
}

export interface DialogHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}
function DialogHeader({ className = "", ...props }: DialogHeaderProps) {
  return (
    <div
      className={`flex-shrink-0 border-b border-gray-200 px-6 py-4 dark:border-gray-800 ${className}`}
      {...props}
    />
  );
}

export interface DialogTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}
function DialogTitle({ className = "", ...props }: DialogTitleProps) {
  return (
    <h2
      className={`text-lg font-semibold text-gray-900 dark:text-slate-100 ${className}`}
      {...props}
    />
  );
}

export interface DialogBodyProps extends React.HTMLAttributes<HTMLDivElement> {}
function DialogBody({ className = "", ...props }: DialogBodyProps) {
  return <div className={`flex-1 overflow-y-auto px-6 py-4 ${className}`} {...props} />;
}

export interface DialogFooterProps extends React.HTMLAttributes<HTMLDivElement> {}
function DialogFooter({ className = "", ...props }: DialogFooterProps) {
  return (
    <div
      className={`flex-shrink-0 border-t border-gray-200 px-6 py-4 dark:border-gray-800 ${className}`}
      {...props}
    />
  );
}

export interface DialogTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}
function DialogTrigger({ className = "", children, onClick, ...props }: DialogTriggerProps) {
  const ctx = useContext(DialogContext);
  if (!ctx) throw new Error("DialogTrigger must be used within <Dialog>");

  const baseClasses =
    "inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100 dark:hover:bg-gray-800";

  return (
    <button
      type="button"
      className={`${baseClasses} ${className}`}
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

export {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogBody,
  DialogFooter,
  DialogTrigger,
};
