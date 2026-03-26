"use client";

import StatusChip from "@/components/ui/StatusChip";
import { t } from "@/i18n/en";
import type { SafetyLevel } from "@/lib/types";

interface StatusHeaderProps {
  status: SafetyLevel;
  subtitle: string;
  onRefresh: () => void;
}

export default function StatusHeader({
  status,
  subtitle,
  onRefresh,
}: StatusHeaderProps) {
  return (
    <div
      className="flex flex-col items-center gap-4 rounded-2xl p-8 text-center"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-md)",
      }}
    >
      <StatusChip status={status} size="lg" />
      <p
        className="max-w-md text-base"
        style={{ color: "var(--color-text-secondary)" }}
      >
        {subtitle}
      </p>
      <button
        onClick={onRefresh}
        className="text-sm transition-opacity hover:opacity-70"
        style={{ color: "var(--color-brand-primary)" }}
        aria-label={t("common.refresh")}
      >
        {t("common.refresh")}
      </button>
    </div>
  );
}
