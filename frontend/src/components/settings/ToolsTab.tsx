"use client";

import { useCallback } from "react";

import { t } from "@/i18n/en";
import type { PolicyConfig, SkillAction, SkillRule } from "@/lib/types";

const DEFAULT_SKILLS: SkillRule[] = [
  { name: "web_search", risk: "low", action: "allow" },
  { name: "file_read", risk: "medium", action: "ask" },
  { name: "file_write", risk: "medium", action: "ask" },
  { name: "shell_exec", risk: "high", action: "block" },
  { name: "network_request", risk: "medium", action: "ask" },
];

const RISK_COLORS: Record<string, string> = {
  low: "var(--color-status-safe)",
  medium: "var(--color-status-attention)",
  high: "var(--color-status-risk)",
  critical: "var(--color-status-risk)",
};

const RISK_BG: Record<string, string> = {
  low: "var(--color-status-safe-bg)",
  medium: "var(--color-status-attention-bg)",
  high: "var(--color-status-risk-bg)",
  critical: "var(--color-status-risk-bg)",
};

interface ToolsTabProps {
  policy: PolicyConfig;
  onSave: (policy: PolicyConfig) => void;
}

export default function ToolsTab({ policy, onSave }: ToolsTabProps) {
  const toolsConfig = policy.tools as Record<string, unknown>;
  const rules = (toolsConfig.rules as SkillRule[]) || DEFAULT_SKILLS;
  const skills = rules.length > 0 ? rules : DEFAULT_SKILLS;

  const saveRules = useCallback(
    (updated: SkillRule[]) => {
      onSave({
        ...policy,
        tools: { ...toolsConfig, rules: updated },
      });
    },
    [policy, toolsConfig, onSave]
  );

  const blockAllHighRisk = () => {
    const updated = skills.map((s) =>
      s.risk === "high" || s.risk === "critical"
        ? { ...s, action: "block" as SkillAction }
        : s
    );
    saveRules(updated);
  };

  const updateAction = (name: string, action: SkillAction) => {
    const updated = skills.map((s) => (s.name === name ? { ...s, action } : s));
    saveRules(updated);
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex justify-end">
        <button
          onClick={blockAllHighRisk}
          className="rounded-md px-3 py-1.5 text-xs font-medium transition-opacity hover:opacity-80"
          style={{
            backgroundColor: "var(--color-status-risk-bg)",
            color: "var(--color-status-risk)",
            borderRadius: "var(--radius-sm)",
          }}
        >
          {t("settings.tools.block_high_risk")}
        </button>
      </div>

      <div
        className="overflow-x-auto rounded-lg border"
        style={{
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-md)",
        }}
      >
        <table className="w-full text-sm">
          <thead>
            <tr
              style={{
                backgroundColor: "var(--color-bg-accent)",
                color: "var(--color-text-secondary)",
              }}
            >
              <th className="px-4 py-2.5 text-left font-medium">{t("settings.tools.name")}</th>
              <th className="px-4 py-2.5 text-left font-medium">{t("settings.tools.risk")}</th>
              <th className="px-4 py-2.5 text-left font-medium">{t("settings.tools.status")}</th>
            </tr>
          </thead>
          <tbody>
            {skills.map((skill) => (
              <tr
                key={skill.name}
                className="border-t"
                style={{ borderColor: "var(--color-border)" }}
              >
                <td className="px-4 py-2.5 font-mono text-xs">{skill.name}</td>
                <td className="px-4 py-2.5">
                  <span
                    className="rounded-full px-2 py-0.5 text-xs font-medium"
                    style={{
                      backgroundColor: RISK_BG[skill.risk] || RISK_BG.medium,
                      color: RISK_COLORS[skill.risk] || RISK_COLORS.medium,
                    }}
                  >
                    {skill.risk}
                  </span>
                </td>
                <td className="px-4 py-2.5">
                  <select
                    value={skill.action}
                    onChange={(e) =>
                      updateAction(skill.name, e.target.value as SkillAction)
                    }
                    aria-label={`${skill.name} action`}
                    className="rounded-md border px-2 py-1 text-xs"
                    style={{
                      backgroundColor: "var(--color-bg-card)",
                      borderColor: "var(--color-border)",
                      borderRadius: "var(--radius-sm)",
                    }}
                  >
                    <option value="allow">Allowed</option>
                    <option value="ask">Ask</option>
                    <option value="block">Blocked</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
