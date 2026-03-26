"use client";

import type { ReactNode } from "react";

import type { SafetyLevel } from "@/lib/types";

import StatusChip from "./StatusChip";

const ICONS: Record<string, string> = {
  network: "🌐",
  tools: "🔧",
  data: "📁",
  updates: "🔄",
};

interface CategoryCardProps {
  category: string;
  title: string;
  icon?: ReactNode;
  status: SafetyLevel;
  summary: string;
  actionLabel: string;
  onAction: () => void;
}

export default function CategoryCard({
  category,
  title,
  icon,
  status,
  summary,
  actionLabel,
  onAction,
}: CategoryCardProps) {
  const isPrimary = status !== "safe";

  return (
    <div
      className="flex flex-col gap-3 border p-5"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderColor: "var(--color-border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-sm)",
      }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl">{icon ?? ICONS[category] ?? "📦"}</span>
          <h3
            className="text-base"
            style={{ fontWeight: "var(--font-weight-semibold)" }}
          >
            {title}
          </h3>
        </div>
        <StatusChip status={status} size="sm" />
      </div>

      <p
        className="text-sm"
        style={{ color: "var(--color-text-secondary)" }}
      >
        {summary}
      </p>

      <button
        onClick={onAction}
        className="mt-auto self-start rounded-lg px-4 py-2 text-sm font-medium transition-opacity hover:opacity-80"
        style={{
          backgroundColor: isPrimary
            ? "var(--color-brand-primary)"
            : "transparent",
          color: isPrimary ? "#fff" : "var(--color-brand-primary)",
          border: isPrimary ? "none" : "1px solid var(--color-border)",
          borderRadius: "var(--radius-md)",
        }}
      >
        {actionLabel}
      </button>
    </div>
  );
}
