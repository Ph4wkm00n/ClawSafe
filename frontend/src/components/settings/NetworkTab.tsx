"use client";

import { useState } from "react";

import SettingRow from "@/components/ui/SettingRow";
import { t } from "@/i18n/en";

export default function NetworkTab() {
  const [bindAddress, setBindAddress] = useState("127.0.0.1");
  const [cidrs, setCidrs] = useState("127.0.0.0/8");
  const [vpnOnly, setVpnOnly] = useState(false);
  const [port, setPort] = useState("8080");

  return (
    <div className="flex flex-col">
      <SettingRow
        label={t("settings.network.bind")}
        description={t("settings.network.bind_desc")}
        tooltip={t("settings.network.bind_tooltip")}
      >
        <select
          value={bindAddress}
          onChange={(e) => setBindAddress(e.target.value)}
          className="rounded-md border px-3 py-1.5 text-sm"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-sm)",
          }}
        >
          <option value="127.0.0.1">127.0.0.1 (localhost)</option>
          <option value="0.0.0.0">0.0.0.0 (all interfaces)</option>
        </select>
      </SettingRow>

      <SettingRow
        label={t("settings.network.cidrs")}
        description={t("settings.network.cidrs_desc")}
        tooltip={t("settings.network.cidrs_tooltip")}
      >
        <input
          type="text"
          value={cidrs}
          onChange={(e) => setCidrs(e.target.value)}
          className="w-40 rounded-md border px-3 py-1.5 text-sm"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-sm)",
          }}
        />
      </SettingRow>

      <SettingRow
        label={t("settings.network.vpn")}
        description={t("settings.network.vpn_desc")}
        tooltip={t("settings.network.vpn_tooltip")}
      >
        <button
          onClick={() => setVpnOnly((v) => !v)}
          className="relative h-6 w-11 rounded-full transition-colors"
          style={{
            backgroundColor: vpnOnly ? "var(--color-brand-primary)" : "var(--color-border)",
          }}
          role="switch"
          aria-checked={vpnOnly}
        >
          <span
            className="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform"
            style={{ left: vpnOnly ? "calc(100% - 1.375rem)" : "0.125rem" }}
          />
        </button>
      </SettingRow>

      <SettingRow
        label={t("settings.network.port")}
        description={t("settings.network.port_desc")}
      >
        <input
          type="number"
          value={port}
          onChange={(e) => setPort(e.target.value)}
          className="w-24 rounded-md border px-3 py-1.5 text-sm"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-sm)",
          }}
        />
      </SettingRow>
    </div>
  );
}
