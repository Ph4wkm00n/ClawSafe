"use client";

import { useState } from "react";

import DataTab from "@/components/settings/DataTab";
import IntegrationsTab from "@/components/settings/IntegrationsTab";
import NetworkTab from "@/components/settings/NetworkTab";
import ToolsTab from "@/components/settings/ToolsTab";
import { t } from "@/i18n/en";

const TABS = [
  { id: "network", label: t("settings.tab.network"), Component: NetworkTab },
  { id: "tools", label: t("settings.tab.tools"), Component: ToolsTab },
  { id: "data", label: t("settings.tab.data"), Component: DataTab },
  { id: "integrations", label: t("settings.tab.integrations"), Component: IntegrationsTab },
];

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("network");
  const ActiveComponent = TABS.find((tab) => tab.id === activeTab)?.Component ?? NetworkTab;

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
      >
        {TABS.map((tab) => {
          const active = tab.id === activeTab;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className="border-b-2 px-4 py-2.5 text-sm font-medium transition-colors"
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
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        <ActiveComponent />
      </div>
    </div>
  );
}
