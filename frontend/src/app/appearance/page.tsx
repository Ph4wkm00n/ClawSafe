"use client";

import { useEffect } from "react";

import { t } from "@/i18n/en";
import { useSettings } from "@/hooks/useSettings";

export default function AppearancePage() {
  const { settings, save } = useSettings();

  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      settings.theme === "minimal" ? "minimal" : "playful"
    );
    if (settings.mode === "dark") {
      document.documentElement.setAttribute("data-mode", "dark");
    } else if (settings.mode === "light") {
      document.documentElement.removeAttribute("data-mode");
    } else {
      // System preference
      const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (dark) {
        document.documentElement.setAttribute("data-mode", "dark");
      } else {
        document.documentElement.removeAttribute("data-mode");
      }
    }
  }, [settings.theme, settings.mode]);

  return (
    <div className="flex flex-col gap-8">
      <h1
        className="text-2xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("appearance.title")}
      </h1>

      {/* Visual Style */}
      <div className="flex flex-col gap-3">
        <h2
          className="text-lg"
          style={{ fontWeight: "var(--font-weight-semibold)" }}
        >
          {t("appearance.style")}
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {(["playful", "minimal"] as const).map((theme) => (
            <button
              key={theme}
              onClick={() => save({ ...settings, theme })}
              className="flex flex-col gap-2 rounded-xl border p-5 text-left transition-all"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor:
                  settings.theme === theme
                    ? "var(--color-brand-primary)"
                    : "var(--color-border)",
                borderWidth: settings.theme === theme ? "2px" : "1px",
                borderRadius: "var(--radius-lg)",
              }}
            >
              <span className="text-2xl">
                {theme === "playful" ? "🦀" : "🔲"}
              </span>
              <span style={{ fontWeight: "var(--font-weight-semibold)" }}>
                {t(`appearance.style.${theme}`)}
              </span>
              <span
                className="text-sm"
                style={{ color: "var(--color-text-secondary)" }}
              >
                {t(`appearance.style.${theme}_desc`)}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Mode */}
      <div className="flex flex-col gap-3">
        <h2
          className="text-lg"
          style={{ fontWeight: "var(--font-weight-semibold)" }}
        >
          {t("appearance.mode")}
        </h2>
        <div className="flex flex-col gap-2">
          {(["system", "light", "dark"] as const).map((mode) => (
            <label
              key={mode}
              className="flex cursor-pointer items-center gap-3 rounded-lg border p-4"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor:
                  settings.mode === mode
                    ? "var(--color-brand-primary)"
                    : "var(--color-border)",
                borderRadius: "var(--radius-md)",
              }}
            >
              <input
                type="radio"
                name="mode"
                checked={settings.mode === mode}
                onChange={() => save({ ...settings, mode })}
                className="accent-[var(--color-brand-primary)]"
              />
              <span className="text-sm font-medium">
                {t(`appearance.mode.${mode}`)}
              </span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
