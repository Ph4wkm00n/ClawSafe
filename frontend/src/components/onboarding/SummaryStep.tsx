"use client";

import { t } from "@/i18n/en";

interface SummaryStepProps {
  onApply: () => void;
  onBack: () => void;
}

const ACTIONS = [
  "onboarding.summary.private",
  "onboarding.summary.tools",
  "onboarding.summary.auth",
];

export default function SummaryStep({ onApply, onBack }: SummaryStepProps) {
  return (
    <div className="flex flex-col items-center gap-6">
      <h2
        className="text-xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("onboarding.summary.title")}
      </h2>

      <div
        className="flex w-full max-w-sm flex-col gap-3 rounded-lg p-5"
        style={{
          backgroundColor: "var(--color-bg-card)",
          border: "1px solid var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        {ACTIONS.map((key) => (
          <div key={key} className="flex items-start gap-3">
            <span
              className="mt-0.5 text-lg"
              style={{ color: "var(--color-status-safe)" }}
            >
              ✓
            </span>
            <p className="text-sm" style={{ color: "var(--color-text-primary)" }}>
              {t(key)}
            </p>
          </div>
        ))}
      </div>

      <button
        onClick={onApply}
        className="w-full max-w-sm rounded-lg px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90"
        style={{
          backgroundColor: "var(--color-brand-primary)",
          borderRadius: "var(--radius-md)",
        }}
      >
        {t("onboarding.summary.cta")}
      </button>

      <button
        onClick={onBack}
        className="text-sm transition-opacity hover:opacity-70"
        style={{ color: "var(--color-text-muted)" }}
      >
        {t("common.back")}
      </button>
    </div>
  );
}
