"use client";

import type { SafetyLevel } from "@/lib/types";

type MascotState = SafetyLevel | "welcome" | "success";

const MASCOT_EMOJI: Record<MascotState, string> = {
  safe: "🦀",
  attention: "🦀",
  risk: "🦀",
  welcome: "🦀",
  success: "🛡️",
};

const MASCOT_EXPRESSION: Record<MascotState, string> = {
  safe: "😊",
  attention: "😟",
  risk: "🚨",
  welcome: "👋",
  success: "✅",
};

const SIZES = {
  sm: "text-2xl",
  md: "text-4xl",
  lg: "text-6xl",
};

interface MascotIllustrationProps {
  state: MascotState;
  size?: "sm" | "md" | "lg";
}

export default function MascotIllustration({
  state,
  size = "md",
}: MascotIllustrationProps) {
  return (
    <div
      className={`inline-flex items-center gap-1 ${SIZES[size]}`}
      role="img"
      aria-label={`ClawSafe mascot: ${state}`}
      data-hide-minimal="true"
    >
      <span>{MASCOT_EMOJI[state]}</span>
      <span className="text-[0.6em]">{MASCOT_EXPRESSION[state]}</span>
    </div>
  );
}
