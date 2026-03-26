"use client";

import { type ReactNode, useEffect } from "react";

import { t } from "@/i18n/en";

interface SideSheetProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export default function SideSheet({
  open,
  onClose,
  title,
  children,
}: SideSheetProps) {
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (open) {
      document.addEventListener("keydown", handleEsc);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", handleEsc);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="absolute inset-0"
        style={{ backgroundColor: "var(--color-backdrop)" }}
        onClick={onClose}
      />

      {/* Sheet */}
      <div
        className="relative flex h-full w-full max-w-md flex-col overflow-y-auto"
        style={{
          backgroundColor: "var(--color-bg-card)",
          boxShadow: "var(--shadow-lg)",
        }}
      >
        <div className="flex items-center justify-between border-b p-5">
          <h2
            className="text-lg"
            style={{ fontWeight: "var(--font-weight-semibold)" }}
          >
            {title}
          </h2>
          <button
            onClick={onClose}
            className="rounded-lg p-2 transition-colors hover:opacity-70"
            aria-label={t("common.close")}
          >
            ✕
          </button>
        </div>
        <div className="flex-1 p-5">{children}</div>
      </div>
    </div>
  );
}
