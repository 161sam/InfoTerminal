"use client";

import { createPortal } from "react-dom";
import { useToastState } from "./index";

export default function ToastViewportImpl() {
  const toasts = useToastState();
  if (typeof document === "undefined") return null;
  return createPortal(
    <div className="fixed top-2 right-2 z-50 flex flex-col gap-2">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`rounded px-2 py-1 text-sm text-white shadow ${
            t.variant === "success"
              ? "bg-green-600"
              : t.variant === "error"
                ? "bg-red-600"
                : "bg-blue-600"
          }`}
        >
          {t.message}
        </div>
      ))}
    </div>,
    document.body,
  );
}
