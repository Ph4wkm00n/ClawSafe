"use client";

import { useEffect, useState } from "react";

import SideSheet from "@/components/ui/SideSheet";
import StepList from "@/components/ui/StepList";
import { t } from "@/i18n/en";
import { getRecommendations } from "@/lib/api";
import type { Recommendation } from "@/lib/types";

interface FixFlowProps {
  actionId: string | null;
  onClose: () => void;
}

export default function FixFlow({ actionId, onClose }: FixFlowProps) {
  const [rec, setRec] = useState<Recommendation | null>(null);
  const [showSteps, setShowSteps] = useState(false);

  useEffect(() => {
    if (!actionId) {
      setRec(null);
      setShowSteps(false);
      return;
    }
    getRecommendations().then((recs) => {
      const found = recs.find((r) => r.id === actionId);
      setRec(found ?? null);
    });
  }, [actionId]);

  if (!rec) return null;

  const steps = rec.steps.map((text, i) => ({
    text,
    code: rec.commands[i],
  }));

  return (
    <SideSheet
      open={!!actionId}
      onClose={onClose}
      title={rec.title}
    >
      <div className="flex flex-col gap-5">
        <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>
          {rec.description}
        </p>

        {/* Auto-fix disabled in v0.1 */}
        <button
          disabled
          className="w-full rounded-lg px-4 py-3 text-sm font-medium opacity-50"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            color: "#fff",
            borderRadius: "var(--radius-md)",
          }}
          title="Coming in v0.2"
        >
          {t("fix.auto")}
        </button>

        <button
          onClick={() => setShowSteps((s) => !s)}
          className="w-full rounded-lg border px-4 py-3 text-sm font-medium transition-opacity hover:opacity-80"
          style={{
            borderColor: "var(--color-border)",
            color: "var(--color-brand-primary)",
            borderRadius: "var(--radius-md)",
          }}
        >
          {t("fix.show_how")}
        </button>

        {showSteps && (
          <StepList
            steps={steps}
            result={`${rec.title} completed successfully.`}
          />
        )}
      </div>
    </SideSheet>
  );
}
