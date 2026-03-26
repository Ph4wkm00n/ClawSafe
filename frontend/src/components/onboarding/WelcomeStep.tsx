"use client";

import { t } from "@/i18n/en";

interface WelcomeStepProps {
  onNext: () => void;
}

export default function WelcomeStep({ onNext }: WelcomeStepProps) {
  return (
    <div className="flex flex-col items-center gap-6 text-center">
      <span className="text-6xl">🦀</span>
      <h1
        className="text-2xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("onboarding.welcome.title")}
      </h1>
      <p
        className="max-w-sm text-base"
        style={{ color: "var(--color-text-secondary)" }}
      >
        {t("onboarding.welcome.body")}
      </p>
      <button
        onClick={onNext}
        className="rounded-lg px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90"
        style={{
          backgroundColor: "var(--color-brand-primary)",
          borderRadius: "var(--radius-md)",
        }}
      >
        {t("onboarding.welcome.cta")}
      </button>
    </div>
  );
}
