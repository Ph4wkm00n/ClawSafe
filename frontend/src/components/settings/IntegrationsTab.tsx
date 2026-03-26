"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import SettingRow from "@/components/ui/SettingRow";
import { useToast } from "@/components/ui/Toast";
import { t } from "@/i18n/en";
import {
  getNotificationConfig,
  testNotification,
  updateNotificationConfig,
} from "@/lib/api";

export default function IntegrationsTab() {
  const [webhooks, setWebhooks] = useState<string[]>([]);
  const [newUrl, setNewUrl] = useState("");
  const [logFormat, setLogFormat] = useState("json");
  const [emailEnabled, setEmailEnabled] = useState(false);
  const [emailAddress, setEmailAddress] = useState("");
  const [testingEmail, setTestingEmail] = useState(false);
  const { toast } = useToast();
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Load notification config on mount
  useEffect(() => {
    getNotificationConfig().then((config) => {
      const c = config as Record<string, unknown>;
      setEmailEnabled((c.email_enabled as boolean) || false);
      setEmailAddress((c.email_address as string) || "");
      const wh = (c.webhooks as Array<{ url: string }>) || [];
      setWebhooks(wh.map((w) => w.url));
    }).catch(() => {});
  }, []);

  const saveConfig = useCallback(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      try {
        await updateNotificationConfig({
          webhooks: webhooks.map((url) => ({ url, name: "", events: ["escalation"] })),
          email_enabled: emailEnabled,
          email_address: emailAddress,
          events: ["escalation", "weekly_summary"],
        });
        toast(t("settings.saved"), "success");
      } catch {
        toast(t("settings.save_failed"), "error");
      }
    }, 800);
  }, [webhooks, emailEnabled, emailAddress, toast]);

  const addWebhook = () => {
    if (newUrl.trim()) {
      setWebhooks((prev) => [...prev, newUrl.trim()]);
      setNewUrl("");
      // Save after state update
      setTimeout(saveConfig, 100);
    }
  };

  const removeWebhook = (idx: number) => {
    setWebhooks((prev) => prev.filter((_, i) => i !== idx));
    setTimeout(saveConfig, 100);
  };

  const handleTestWebhook = async (url: string) => {
    try {
      const result = await testNotification(url);
      toast(result.success ? t("settings.integrations.test_success") : t("settings.integrations.test_failed"), result.success ? "success" : "error");
    } catch {
      toast(t("settings.integrations.test_failed"), "error");
    }
  };

  const handleTestEmail = async () => {
    setTestingEmail(true);
    try {
      // Save config first so email address is persisted
      await updateNotificationConfig({
        webhooks: webhooks.map((url) => ({ url, name: "", events: ["escalation"] })),
        email_enabled: true,
        email_address: emailAddress,
        events: ["escalation", "weekly_summary"],
      });
      const resp = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/settings/notifications/test-email`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(process.env.NEXT_PUBLIC_API_KEY ? { Authorization: `Bearer ${process.env.NEXT_PUBLIC_API_KEY}` } : {}),
          },
        }
      );
      const result = await resp.json();
      toast(
        result.success ? t("settings.integrations.email_test_sent") : t("settings.integrations.email_test_failed"),
        result.success ? "success" : "error"
      );
    } catch {
      toast(t("settings.integrations.email_test_failed"), "error");
    } finally {
      setTestingEmail(false);
    }
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
          aria-label={t("settings.integrations.log_format")}
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
              onClick={() => handleTestWebhook(url)}
              className="text-xs transition-opacity hover:opacity-70"
              style={{ color: "var(--color-brand-primary)" }}
            >
              Test
            </button>
            <button
              onClick={() => removeWebhook(i)}
              className="text-xs transition-opacity hover:opacity-70"
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
            aria-label={t("settings.integrations.webhooks")}
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
          onClick={() => {
            setEmailEnabled((v) => !v);
            setTimeout(saveConfig, 100);
          }}
          className="relative h-6 w-11 rounded-full transition-colors"
          style={{
            backgroundColor: emailEnabled ? "var(--color-brand-primary)" : "var(--color-border)",
          }}
          role="switch"
          aria-checked={emailEnabled}
          aria-label={t("settings.integrations.email")}
        >
          <span
            className="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform"
            style={{ left: emailEnabled ? "calc(100% - 1.375rem)" : "0.125rem" }}
          />
        </button>
      </SettingRow>

      {emailEnabled && (
        <div className="flex gap-2 pl-4">
          <input
            type="email"
            value={emailAddress}
            onChange={(e) => setEmailAddress(e.target.value)}
            onBlur={saveConfig}
            placeholder="alerts@example.com"
            aria-label={t("settings.integrations.email_address")}
            className="flex-1 rounded-md border px-3 py-1.5 text-sm"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-sm)",
            }}
          />
          <button
            onClick={handleTestEmail}
            disabled={!emailAddress || testingEmail}
            className="rounded-md px-3 py-1.5 text-xs font-medium transition-opacity hover:opacity-80 disabled:opacity-40"
            style={{
              backgroundColor: "var(--color-brand-primary)",
              color: "#fff",
              borderRadius: "var(--radius-sm)",
            }}
          >
            {testingEmail ? t("settings.integrations.sending") : t("settings.integrations.test_email")}
          </button>
        </div>
      )}
    </div>
  );
}
