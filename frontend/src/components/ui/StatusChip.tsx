"use client";

import { t } from "@/i18n/en";
import type { SafetyLevel } from "@/lib/types";

const STYLES: Record<SafetyLevel, { bg: string; color: string }> = {
  safe: { bg: "var(--color-status-safe-bg)", color: "var(--color-status-safe)" },
  attention: { bg: "var(--color-status-attention-bg)", color: "var(--color-status-attention)" },
  risk: { bg: "var(--color-status-risk-bg)", color: "var(--color-status-risk)" },
};

const LABELS: Record<SafetyLevel, string> = {
  safe: "status.safe",
  attention: "status.attention",
  risk: "status.risk",
};

const SIZES = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-3 py-1 text-sm",
  lg: "px-4 py-1.5 text-base",
};

interface StatusChipProps {
  status: SafetyLevel;
  size?: "sm" | "md" | "lg";
}

export default function StatusChip({ status, size = "md" }: StatusChipProps) {
  const style = STYLES[status];
  return (
    <span
      className={`inline-flex items-center font-semibold ${SIZES[size]}`}
      style={{
        backgroundColor: style.bg,
        color: style.color,
        borderRadius: "var(--radius-full)",
      }}
      role="status"
    >
      {t(LABELS[status])}
    </span>
  );
}
