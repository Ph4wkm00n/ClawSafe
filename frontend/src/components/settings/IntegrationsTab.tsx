"use client";

import { t } from "@/i18n/en";

export default function IntegrationsTab() {
  return (
    <div
      className="flex flex-col items-center justify-center gap-3 rounded-lg border p-12"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderColor: "var(--color-border)",
        borderRadius: "var(--radius-lg)",
      }}
    >
      <p className="text-4xl">🔗</p>
      <p
        className="text-sm"
        style={{ color: "var(--color-text-muted)" }}
      >
        {t("settings.integrations.coming_soon")}
      </p>
    </div>
  );
}
