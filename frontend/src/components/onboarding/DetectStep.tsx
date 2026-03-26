"use client";

import { t } from "@/i18n/en";

interface DetectStepProps {
  detected: boolean;
  onNext: () => void;
  onBack: () => void;
}

export default function DetectStep({ detected, onNext, onBack }: DetectStepProps) {
  return (
    <div className="flex flex-col items-center gap-6 text-center">
      <span className="text-4xl">{detected ? "✅" : "ℹ️"}</span>
      <p
        className="max-w-sm text-base"
        style={{ color: "var(--color-text-secondary)" }}
      >
        {detected
          ? t("onboarding.detect.found")
          : t("onboarding.detect.not_found")}
      </p>
      <div className="flex flex-col gap-3 w-full max-w-xs">
        <button
          onClick={onNext}
          className="rounded-lg px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            borderRadius: "var(--radius-md)",
          }}
        >
          {detected
            ? t("onboarding.detect.secure_existing")
            : t("onboarding.detect.setup_new")}
        </button>
      </div>
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
