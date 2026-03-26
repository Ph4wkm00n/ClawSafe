"use client";

import { useCallback, useEffect, useState } from "react";

import DataTab from "@/components/settings/DataTab";
import IntegrationsTab from "@/components/settings/IntegrationsTab";
import NetworkTab from "@/components/settings/NetworkTab";
import ToolsTab from "@/components/settings/ToolsTab";
import { useToast } from "@/components/ui/Toast";
import { t } from "@/i18n/en";
import { getPolicy, updatePolicy } from "@/lib/api";
import type { PolicyConfig } from "@/lib/types";

const DEFAULT_POLICY: PolicyConfig = {
  version: "1",
  name: "default",
  network: { bind_address: "127.0.0.1", allowed_cidrs: ["127.0.0.0/8"], vpn_only: false },
  tools: { default_action: "ask", rules: [] },
  data: { allowed_mounts: [], backup: { enabled: true, frequency: "daily" } },
  auth: { enabled: true, method: "token" },
  monitoring: {},
  integrations: {},
};

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("network");
  const [policy, setPolicy] = useState<PolicyConfig>(DEFAULT_POLICY);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    getPolicy()
      .then((resp) => setPolicy(resp.config))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const savePolicy = useCallback(
    async (updated: PolicyConfig) => {
      setPolicy(updated);
      try {
        await updatePolicy(updated);
        toast("Settings saved", "success");
      } catch {
        toast("Failed to save settings", "error");
      }
    },
    [toast]
  );

  const TABS = [
    { id: "network", label: t("settings.tab.network") },
    { id: "tools", label: t("settings.tab.tools") },
    { id: "data", label: t("settings.tab.data") },
    { id: "integrations", label: t("settings.tab.integrations") },
  ];

  const renderTab = () => {
    switch (activeTab) {
      case "network":
        return <NetworkTab policy={policy} onSave={savePolicy} />;
      case "tools":
        return <ToolsTab policy={policy} onSave={savePolicy} />;
      case "data":
        return <DataTab policy={policy} onSave={savePolicy} />;
      case "integrations":
        return <IntegrationsTab />;
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <h1
        className="text-2xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("settings.title")}
      </h1>

      <div
        className="flex gap-1 border-b"
        style={{ borderColor: "var(--color-border)" }}
        role="tablist"
      >
        {TABS.map((tab) => {
          const active = tab.id === activeTab;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className="border-b-2 px-4 py-2.5 text-sm font-medium transition-colors"
              role="tab"
              aria-selected={active}
              style={{
                borderColor: active ? "var(--color-brand-primary)" : "transparent",
                color: active ? "var(--color-brand-primary)" : "var(--color-text-secondary)",
              }}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      <div
        className="rounded-lg border p-5"
        role="tabpanel"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        {loading ? (
          <p className="text-sm" style={{ color: "var(--color-text-muted)" }}>
            {t("common.loading")}
          </p>
        ) : (
          renderTab()
        )}
      </div>
    </div>
  );
}
