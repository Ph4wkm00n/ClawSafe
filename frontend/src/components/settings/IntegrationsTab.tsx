"use client";

import { useState } from "react";

import SettingRow from "@/components/ui/SettingRow";
import { t } from "@/i18n/en";

export default function IntegrationsTab() {
  const [webhooks, setWebhooks] = useState<string[]>([]);
  const [newUrl, setNewUrl] = useState("");
  const [logFormat, setLogFormat] = useState("json");
  const [emailEnabled, setEmailEnabled] = useState(false);
  const [emailAddress, setEmailAddress] = useState("");

  const addWebhook = () => {
    if (newUrl.trim()) {
      setWebhooks((prev) => [...prev, newUrl.trim()]);
      setNewUrl("");
    }
  };

  const removeWebhook = (idx: number) => {
    setWebhooks((prev) => prev.filter((_, i) => i !== idx));
  };

  return (
    <div className="flex flex-col gap-4">
      <SettingRow
        label={t("settings.integrations.metrics")}
        description={t("settings.integrations.metrics_desc")}
      >
        <span
          className="rounded-md px-3 py-1.5 font-mono text-xs"
          style={{
            backgroundColor: "var(--color-bg-primary)",
            border: "1px solid var(--color-border)",
          }}
        >
          http://localhost:8000/metrics
        </span>
      </SettingRow>

      <SettingRow
        label={t("settings.integrations.log_format")}
        description={t("settings.integrations.log_format_desc")}
      >
        <select
          value={logFormat}
          onChange={(e) => setLogFormat(e.target.value)}
          className="rounded-md border px-3 py-1.5 text-sm"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-sm)",
          }}
        >
          <option value="json">JSON</option>
          <option value="text">Plain text</option>
        </select>
      </SettingRow>

      {/* Webhooks */}
      <div className="flex flex-col gap-2 border-b py-4" style={{ borderColor: "var(--color-border)" }}>
        <span className="text-sm" style={{ fontWeight: "var(--font-weight-semibold)" }}>
          {t("settings.integrations.webhooks")}
        </span>
        <span className="text-xs" style={{ color: "var(--color-text-secondary)" }}>
          {t("settings.integrations.webhooks_desc")}
        </span>

        {webhooks.map((url, i) => (
          <div key={i} className="flex items-center gap-2">
            <span className="flex-1 truncate font-mono text-xs">{url}</span>
            <button
              onClick={() => removeWebhook(i)}
              className="text-xs"
              style={{ color: "var(--color-status-risk)" }}
            >
              Remove
            </button>
          </div>
        ))}

        <div className="flex gap-2">
          <input
            type="url"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            placeholder="https://hooks.slack.com/..."
            className="flex-1 rounded-md border px-3 py-1.5 text-sm"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-sm)",
            }}
          />
          <button
            onClick={addWebhook}
            className="rounded-md px-3 py-1.5 text-sm font-medium"
            style={{
              backgroundColor: "var(--color-brand-primary)",
              color: "#fff",
              borderRadius: "var(--radius-sm)",
            }}
          >
            Add
          </button>
        </div>
      </div>

      {/* Email */}
      <SettingRow
        label={t("settings.integrations.email")}
        description={t("settings.integrations.email_desc")}
      >
        <button
          onClick={() => setEmailEnabled((v) => !v)}
          className="relative h-6 w-11 rounded-full transition-colors"
          style={{
            backgroundColor: emailEnabled ? "var(--color-brand-primary)" : "var(--color-border)",
          }}
          role="switch"
          aria-checked={emailEnabled}
        >
          <span
            className="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform"
            style={{ left: emailEnabled ? "calc(100% - 1.375rem)" : "0.125rem" }}
          />
        </button>
      </SettingRow>

      {emailEnabled && (
        <div className="pl-4">
          <input
            type="email"
            value={emailAddress}
            onChange={(e) => setEmailAddress(e.target.value)}
            placeholder="alerts@example.com"
            className="w-full rounded-md border px-3 py-1.5 text-sm"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-sm)",
            }}
          />
        </div>
      )}
    </div>
  );
}
