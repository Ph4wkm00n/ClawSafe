"use client";

import { createContext, type ReactNode, useCallback, useContext, useState } from "react";

type ToastType = "success" | "error" | "info";

interface ToastMessage {
  id: number;
  message: string;
  type: ToastType;
}

interface ToastContextValue {
  toast: (message: string, type?: ToastType) => void;
}

const ToastContext = createContext<ToastContextValue>({ toast: () => {} });

export function useToast() {
  return useContext(ToastContext);
}

const COLORS: Record<ToastType, { bg: string; color: string }> = {
  success: { bg: "var(--color-status-safe-bg)", color: "var(--color-status-safe)" },
  error: { bg: "var(--color-status-risk-bg)", color: "var(--color-status-risk)" },
  info: { bg: "var(--color-bg-card)", color: "var(--color-text-primary)" },
};

let nextId = 0;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const toast = useCallback((message: string, type: ToastType = "info") => {
    const id = nextId++;
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);
  }, []);

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div
        className="fixed bottom-20 right-4 z-50 flex flex-col gap-2 lg:bottom-4"
        role="status"
        aria-live="polite"
      >
        {toasts.map((t) => (
          <div
            key={t.id}
            className="rounded-lg px-4 py-2.5 text-sm font-medium shadow-lg"
            role="alert"
            style={{
              backgroundColor: COLORS[t.type].bg,
              color: COLORS[t.type].color,
              borderRadius: "var(--radius-md)",
              boxShadow: "var(--shadow-md)",
            }}
          >
            {t.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
