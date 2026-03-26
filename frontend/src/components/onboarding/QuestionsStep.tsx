"use client";

import { useState } from "react";

import { t } from "@/i18n/en";

interface QuestionsStepProps {
  onNext: (usageType: string, networkPref: string) => void;
  onBack: () => void;
}

export default function QuestionsStep({ onNext, onBack }: QuestionsStepProps) {
  const [usageType, setUsageType] = useState("");
  const [networkPref, setNetworkPref] = useState("");

  const canProceed = usageType !== "" && networkPref !== "";

  return (
    <div className="flex flex-col gap-8">
      {/* Q1 */}
      <div className="flex flex-col gap-3">
        <h2
          className="text-lg"
          style={{ fontWeight: "var(--font-weight-semibold)" }}
        >
          {t("onboarding.q1.title")}
        </h2>
        <div className="flex flex-col gap-2">
          {(["home", "business", "not_sure"] as const).map((opt) => (
            <label
              key={opt}
              className="flex cursor-pointer items-center gap-3 rounded-lg border p-4"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor:
                  usageType === opt
                    ? "var(--color-brand-primary)"
                    : "var(--color-border)",
                borderRadius: "var(--radius-md)",
              }}
            >
              <input
                type="radio"
                name="usage"
                checked={usageType === opt}
                onChange={() => setUsageType(opt)}
                className="accent-[var(--color-brand-primary)]"
              />
              <div className="flex flex-col">
                <span className="text-sm font-medium">
                  {t(`onboarding.q1.${opt}`)}
                </span>
                {opt === "not_sure" && (
                  <span
                    className="text-xs"
                    style={{ color: "var(--color-text-muted)" }}
                  >
                    {t("onboarding.q1.not_sure_help")}
                  </span>
                )}
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Q2 */}
      <div className="flex flex-col gap-3">
        <h2
          className="text-lg"
          style={{ fontWeight: "var(--font-weight-semibold)" }}
        >
          {t("onboarding.q2.title")}
        </h2>
        <div className="flex flex-col gap-2">
          {(["no", "yes", "not_sure"] as const).map((opt) => (
            <label
              key={opt}
              className="flex cursor-pointer items-center gap-3 rounded-lg border p-4"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor:
                  networkPref === opt
                    ? "var(--color-brand-primary)"
                    : "var(--color-border)",
                borderRadius: "var(--radius-md)",
              }}
            >
              <input
                type="radio"
                name="network"
                checked={networkPref === opt}
                onChange={() => setNetworkPref(opt)}
                className="accent-[var(--color-brand-primary)]"
              />
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">
                  {t(`onboarding.q2.${opt}`)}
                </span>
                {opt === "no" && (
                  <span
                    className="rounded-full px-2 py-0.5 text-xs font-medium"
                    style={{
                      backgroundColor: "var(--color-status-safe-bg)",
                      color: "var(--color-status-safe)",
                    }}
                  >
                    {t("onboarding.q2.no_badge")}
                  </span>
                )}
              </div>
              {opt === "not_sure" && (
                <span
                  className="ml-auto text-xs"
                  style={{ color: "var(--color-text-muted)" }}
                >
                  {t("onboarding.q2.not_sure_help")}
                </span>
              )}
            </label>
          ))}
        </div>
      </div>

      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="text-sm transition-opacity hover:opacity-70"
          style={{ color: "var(--color-text-muted)" }}
        >
          {t("common.back")}
        </button>
        <button
          onClick={() => onNext(usageType, networkPref)}
          disabled={!canProceed}
          className="rounded-lg px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-40"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            borderRadius: "var(--radius-md)",
          }}
        >
          {t("common.next")}
        </button>
      </div>
    </div>
  );
}
