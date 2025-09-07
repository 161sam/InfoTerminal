'use client';

import { createContext, PropsWithChildren, useContext, useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

export type ToastVariant = 'info' | 'success' | 'error';
export interface ToastMessage {
  id: number;
  message: string;
  variant: ToastVariant;
}

const listeners = new Set<(toast: ToastMessage) => void>();
let idCounter = 0;

export function toast(message: string, opts?: { variant?: ToastVariant }) {
  if (typeof window === 'undefined') return;
  const t: ToastMessage = {
    id: ++idCounter,
    message,
    variant: opts?.variant ?? 'info',
  };
  listeners.forEach((l) => l(t));
}

const ToastContext = createContext<ToastMessage[]>([]);
export function useToastState() {
  return useContext(ToastContext);
}

export function ToastProvider({ children }: PropsWithChildren) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  useEffect(() => {
    const handler = (t: ToastMessage) => {
      setToasts((prev) => [...prev, t]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((i) => i.id !== t.id));
      }, 3000);
    };
    listeners.add(handler);
    return () => {
      listeners.delete(handler);
    };
  }, []);

  return <ToastContext.Provider value={toasts}>{children}</ToastContext.Provider>;
}

export const ToastViewport = dynamic(() => import('./ToastViewportImpl'), { ssr: false });

