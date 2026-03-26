"use client";

import { useState } from "react";

import ProgressDots from "@/components/ui/ProgressDots";
import { t } from "@/i18n/en";
import type { UserSettings } from "@/lib/types";

import DetectStep from "./DetectStep";
import QuestionsStep from "./QuestionsStep";
import SummaryStep from "./SummaryStep";
import WelcomeStep from "./WelcomeStep";

interface OnboardingWizardProps {
  onComplete: (settings: Partial<UserSettings>) => void;
}

export default function OnboardingWizard({ onComplete }: OnboardingWizardProps) {
  const [step, setStep] = useState(0);
  const [usageType, setUsageType] = useState("");
  const [networkPref, setNetworkPref] = useState("");
  const [done, setDone] = useState(false);

  if (done) {
    return (
      <div className="flex flex-col items-center gap-6 py-12 text-center">
        <span className="text-6xl">🛡️</span>
        <h1
          className="text-2xl"
          style={{ fontWeight: "var(--font-weight-bold)" }}
        >
          {t("onboarding.done.title")}
        </h1>
        <p
          className="max-w-sm text-base"
          style={{ color: "var(--color-text-secondary)" }}
        >
          {t("onboarding.done.body")}
        </p>
        <button
          onClick={() =>
            onComplete({
              onboarding_complete: true,
              usage_type: usageType,
              network_preference: networkPref,
            })
          }
          className="rounded-lg px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            borderRadius: "var(--radius-md)",
          }}
        >
          {t("onboarding.done.cta")}
        </button>
      </div>
    );
  }

  const steps = [
    <WelcomeStep key="welcome" onNext={() => setStep(1)} />,
    <DetectStep
      key="detect"
      detected={false}
      onNext={() => setStep(2)}
      onBack={() => setStep(0)}
    />,
    <QuestionsStep
      key="questions"
      onNext={(usage, net) => {
        setUsageType(usage);
        setNetworkPref(net);
        setStep(3);
      }}
      onBack={() => setStep(1)}
    />,
    <SummaryStep
      key="summary"
      onApply={() => setDone(true)}
      onBack={() => setStep(2)}
    />,
  ];

  return (
    <div className="mx-auto flex max-w-lg flex-col gap-8 py-12">
      <ProgressDots total={4} current={step} />
      {steps[step]}
    </div>
  );
}
