"use client";

import { type ReactNode, useState } from "react";

interface SettingRowProps {
  label: string;
  description: string;
  tooltip?: string;
  children: ReactNode;
}

export default function SettingRow({
  label,
  description,
  tooltip,
  children,
}: SettingRowProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div
      className="flex flex-col gap-2 border-b py-4 last:border-b-0"
      style={{ borderColor: "var(--color-border)" }}
    >
      <div className="flex items-center justify-between gap-4">
        <div className="flex flex-col gap-0.5">
          <span
            className="text-sm"
            style={{ fontWeight: "var(--font-weight-semibold)" }}
          >
            {label}
          </span>
          <span
            className="text-xs"
            style={{ color: "var(--color-text-secondary)" }}
          >
            {description}
          </span>
        </div>
        <div className="shrink-0">{children}</div>
      </div>

      {tooltip && (
        <button
          onClick={() => setShowTooltip((s) => !s)}
          className="flex items-center gap-1 self-start text-xs transition-opacity hover:opacity-70"
          style={{ color: "var(--color-brand-primary)" }}
        >
          <span>ⓘ</span>
          <span>What this really means</span>
        </button>
      )}

      {showTooltip && tooltip && (
        <div
          className="rounded-lg p-3 text-xs"
          style={{
            backgroundColor: "var(--color-bg-accent)",
            color: "var(--color-text-secondary)",
            borderRadius: "var(--radius-md)",
          }}
        >
          {tooltip}
        </div>
      )}
    </div>
  );
}
