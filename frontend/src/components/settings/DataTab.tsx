"use client";

import { useState } from "react";

import SettingRow from "@/components/ui/SettingRow";
import { t } from "@/i18n/en";

const DEMO_MOUNTS = [
  { path: "/home/user/documents", risk: "safe" as const },
  { path: "/home/user/media", risk: "safe" as const },
  { path: "/", risk: "risk" as const },
];

const RISK_STYLES = {
  safe: { bg: "var(--color-status-safe-bg)", color: "var(--color-status-safe)" },
  risk: { bg: "var(--color-status-risk-bg)", color: "var(--color-status-risk)" },
};

import type { PolicyConfig } from "@/lib/types";

interface DataTabProps {
  policy: PolicyConfig;
  onSave: (policy: PolicyConfig) => void;
}

export default function DataTab({ policy, onSave }: DataTabProps) {
  const dataConfig = policy.data as Record<string, unknown>;
  const allowedMounts = (dataConfig.allowed_mounts as string[]) || [];
  const backup = (dataConfig.backup as Record<string, unknown>) || {};
  const backupEnabled = (backup.enabled as boolean) ?? true;
  const backupFreq = (backup.frequency as string) || "daily";

  const mounts = allowedMounts.length > 0
    ? allowedMounts.map((p) => ({
        path: p,
        risk: (["/", "/etc", "/root", "/home"].includes(p.replace(/\/$/, "")) ? "risk" : "safe") as "safe" | "risk",
      }))
    : DEMO_MOUNTS;

  const removeMount = (path: string) => {
    const updated = mounts.filter((m) => m.path !== path);
    onSave({
      ...policy,
      data: { ...dataConfig, allowed_mounts: updated.map((m) => m.path) },
    });
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Mount paths */}
      <div className="flex flex-col gap-2">
        <h3
          className="text-sm"
          style={{ fontWeight: "var(--font-weight-semibold)" }}
        >
          {t("settings.data.mounts")}
        </h3>
        <div
          className="flex flex-col gap-1 rounded-lg border p-3"
          style={{
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-md)",
          }}
        >
          {mounts.map((mount) => {
            const style = RISK_STYLES[mount.risk];
            return (
              <div
                key={mount.path}
                className="flex items-center justify-between py-1.5"
              >
                <div className="flex items-center gap-2">
                  <span
                    className="rounded-full px-2 py-0.5 text-xs font-medium"
                    style={{ backgroundColor: style.bg, color: style.color }}
                  >
                    {mount.risk}
                  </span>
                  <span className="font-mono text-xs">{mount.path}</span>
                </div>
                <button
                  onClick={() => removeMount(mount.path)}
                  className="text-xs transition-opacity hover:opacity-70"
                  style={{ color: "var(--color-status-risk)" }}
                >
                  Remove
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Backup settings */}
      <SettingRow
        label={t("settings.data.backup")}
        description={t("settings.data.backup_desc")}
      >
        <button
          onClick={() => setBackupEnabled((v) => !v)}
          className="relative h-6 w-11 rounded-full transition-colors"
          style={{
            backgroundColor: backupEnabled ? "var(--color-brand-primary)" : "var(--color-border)",
          }}
          role="switch"
          aria-checked={backupEnabled}
        >
          <span
            className="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform"
            style={{ left: backupEnabled ? "calc(100% - 1.375rem)" : "0.125rem" }}
          />
        </button>
      </SettingRow>

      {backupEnabled && (
        <SettingRow
          label={t("settings.data.frequency")}
          description={t("settings.data.frequency_desc")}
        >
          <select
            value={backupFreq}
            onChange={(e) => setBackupFreq(e.target.value)}
            className="rounded-md border px-3 py-1.5 text-sm"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-sm)",
            }}
          >
            <option value="hourly">Hourly</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
        </SettingRow>
      )}
    </div>
  );
}
