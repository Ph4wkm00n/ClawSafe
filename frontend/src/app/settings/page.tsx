"use client";

import { t } from "@/i18n/en";

const TABS = [
  { id: "network", label: t("settings.tab.network") },
  { id: "tools", label: t("settings.tab.tools") },
  { id: "data", label: t("settings.tab.data") },
  { id: "integrations", label: t("settings.tab.integrations") },
];

export default function SettingsPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1
        className="text-2xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("settings.title")}
      </h1>

      <div className="flex gap-2 border-b" style={{ borderColor: "var(--color-border)" }}>
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className="border-b-2 px-4 py-2.5 text-sm font-medium transition-colors"
            style={{
              borderColor: "var(--color-brand-primary)",
              color: "var(--color-brand-primary)",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div
        className="flex flex-col items-center justify-center gap-3 rounded-lg border p-12"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        <p className="text-4xl">⚙️</p>
        <p
          className="text-sm"
          style={{ color: "var(--color-text-muted)" }}
        >
          Advanced Settings will be available in v0.2.
        </p>
      </div>
    </div>
  );
}
