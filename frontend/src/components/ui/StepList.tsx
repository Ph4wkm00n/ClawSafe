"use client";

import CodeBlock from "./CodeBlock";

interface Step {
  text: string;
  code?: string;
}

interface StepListProps {
  steps: Step[];
  result?: string;
}

export default function StepList({ steps, result }: StepListProps) {
  return (
    <div className="flex flex-col gap-4">
      {steps.map((step, i) => (
        <div key={i} className="flex gap-3">
          <span
            className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold text-white"
            style={{ backgroundColor: "var(--color-brand-primary)" }}
          >
            {i + 1}
          </span>
          <div className="flex flex-1 flex-col gap-2">
            <p className="text-sm" style={{ color: "var(--color-text-primary)" }}>
              {step.text}
            </p>
            {step.code && <CodeBlock code={step.code} />}
          </div>
        </div>
      ))}

      {result && (
        <div
          className="mt-2 rounded-lg p-3 text-sm"
          style={{
            backgroundColor: "var(--color-status-safe-bg)",
            color: "var(--color-status-safe)",
            borderRadius: "var(--radius-md)",
          }}
        >
          <strong>Expected result:</strong> {result}
        </div>
      )}
    </div>
  );
}
