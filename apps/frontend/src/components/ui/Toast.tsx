'use client';

import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

type ToastItem = { id: number; msg: string; type: 'success' | 'error' };

let queue: ToastItem[] = [];
const listeners = new Set<(items: ToastItem[]) => void>();
let idCounter = 0;

function emit() {
  listeners.forEach((l) => l([...queue]));
}

function add(type: 'success' | 'error', msg: string) {
  const item: ToastItem = { id: ++idCounter, msg, type };
  queue.push(item);
  emit();
  setTimeout(() => {
    queue = queue.filter((t) => t.id !== item.id);
    emit();
  }, 3000);
}

export const toast = {
  success: (msg: string) => add('success', msg),
  error: (msg: string) => add('error', msg),
};

export function ToastViewport() {
  const [items, setItems] = useState<ToastItem[]>([]);
  useEffect(() => {
    const handler = (i: ToastItem[]) => setItems(i);
    listeners.add(handler);
    return () => listeners.delete(handler);
  }, []);
  if (typeof document === 'undefined') return null;
  return createPortal(
    <div className="fixed top-2 right-2 z-50 flex flex-col gap-2">
      {items.map((t) => (
        <div
          key={t.id}
          className={`rounded px-2 py-1 text-sm text-white shadow ${
            t.type === 'success' ? 'bg-green-600' : 'bg-red-600'
          }`}
        >
          {t.msg}
        </div>
      ))}
    </div>,
    document.body
  );
}

export default toast;
