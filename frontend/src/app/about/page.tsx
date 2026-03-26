"use client";

import { t } from "@/i18n/en";

export default function AboutPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1
        className="text-2xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("about.title")}
      </h1>

      <div
        className="flex flex-col gap-4 border p-6"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        <div className="flex items-center gap-3">
          <span className="text-3xl">🦀</span>
          <div>
            <h2
              className="text-lg"
              style={{ fontWeight: "var(--font-weight-semibold)" }}
            >
              {t("app.name")}
            </h2>
            <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>
              {t("app.tagline")}
            </p>
          </div>
        </div>

        <div className="flex flex-col gap-2 text-sm">
          <p>
            <span style={{ color: "var(--color-text-muted)" }}>
              {t("about.version")}:{" "}
            </span>
            <span style={{ fontWeight: "var(--font-weight-medium)" }}>0.1.0</span>
          </p>
        </div>

        <div className="flex flex-col gap-2 border-t pt-4" style={{ borderColor: "var(--color-border)" }}>
          <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>
            ClawSafe is a self-hosted security sidecar for OpenClaw that helps home users and small businesses secure, monitor, and understand their OpenClaw instances.
          </p>
        </div>
      </div>
    </div>
  );
}
