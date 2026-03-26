"use client";

import { useEffect, useState } from "react";

import SideSheet from "@/components/ui/SideSheet";
import StepList from "@/components/ui/StepList";
import { t } from "@/i18n/en";
import { applyFix, getRecommendations, undoFix } from "@/lib/api";
import type { Recommendation } from "@/lib/types";

type FixState = "idle" | "fixing" | "success" | "error";

interface FixFlowProps {
  actionId: string | null;
  onClose: () => void;
}

export default function FixFlow({ actionId, onClose }: FixFlowProps) {
  const [rec, setRec] = useState<Recommendation | null>(null);
  const [showSteps, setShowSteps] = useState(false);
  const [fixState, setFixState] = useState<FixState>("idle");
  const [fixMessage, setFixMessage] = useState("");

  useEffect(() => {
    if (!actionId) {
      setRec(null);
      setShowSteps(false);
      setFixState("idle");
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

  const handleAutoFix = async () => {
    setFixState("fixing");
    try {
      const result = await applyFix(rec.id);
      if (result.success) {
        setFixState("success");
        setFixMessage(result.message);
      } else {
        setFixState("error");
        setFixMessage(result.message);
      }
    } catch {
      setFixState("error");
      setFixMessage(t("fix.error"));
    }
  };

  const handleUndo = async () => {
    try {
      const result = await undoFix(rec.id);
      if (result.success) {
        setFixState("idle");
        setFixMessage("");
      }
    } catch {
      // Best effort
    }
  };

  return (
    <SideSheet open={!!actionId} onClose={onClose} title={rec.title}>
      <div className="flex flex-col gap-5">
        <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>
          {rec.description}
        </p>

        {fixState === "success" && (
          <div
            className="flex flex-col gap-3 rounded-lg p-4"
            style={{
              backgroundColor: "var(--color-status-safe-bg)",
              borderRadius: "var(--radius-md)",
            }}
          >
            <div className="flex items-center gap-2">
              <span style={{ color: "var(--color-status-safe)" }}>✓</span>
              <span
                className="text-sm font-medium"
                style={{ color: "var(--color-status-safe)" }}
              >
                {t("fix.success")} {fixMessage}
              </span>
            </div>
            <button
              onClick={handleUndo}
              className="self-start text-xs transition-opacity hover:opacity-70"
              style={{ color: "var(--color-brand-primary)" }}
            >
              {t("fix.undo")}
            </button>
          </div>
        )}

        {fixState === "error" && (
          <div
            className="flex flex-col gap-3 rounded-lg p-4"
            style={{
              backgroundColor: "var(--color-status-risk-bg)",
              borderRadius: "var(--radius-md)",
            }}
          >
            <span
              className="text-sm"
              style={{ color: "var(--color-status-risk)" }}
            >
              {fixMessage}
            </span>
            <button
              onClick={handleAutoFix}
              className="self-start text-xs font-medium transition-opacity hover:opacity-70"
              style={{ color: "var(--color-brand-primary)" }}
            >
              {t("fix.try_again")}
            </button>
          </div>
        )}

        {fixState !== "success" && (
          <>
            <button
              onClick={handleAutoFix}
              disabled={fixState === "fixing"}
              className="w-full rounded-lg px-4 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
              style={{
                backgroundColor: "var(--color-brand-primary)",
                borderRadius: "var(--radius-md)",
              }}
            >
              {fixState === "fixing" ? t("fix.applying") : t("fix.auto")}
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
          </>
        )}

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
