"use client";

import { useCallback, useRef } from "react";

import SettingRow from "@/components/ui/SettingRow";
import { t } from "@/i18n/en";
import type { PolicyConfig } from "@/lib/types";

interface NetworkTabProps {
  policy: PolicyConfig;
  onSave: (policy: PolicyConfig) => void;
}

export default function NetworkTab({ policy, onSave }: NetworkTabProps) {
  const net = policy.network as Record<string, unknown>;
  const bindAddress = (net.bind_address as string) || "127.0.0.1";
  const cidrs = ((net.allowed_cidrs as string[]) || []).join(", ");
  const vpnOnly = (net.vpn_only as boolean) || false;

  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const update = useCallback(
    (changes: Record<string, unknown>) => {
      const updated = {
        ...policy,
        network: { ...net, ...changes },
      };
      if (debounceRef.current) clearTimeout(debounceRef.current);
      debounceRef.current = setTimeout(() => onSave(updated), 800);
    },
    [policy, net, onSave]
  );

  return (
    <div className="flex flex-col">
      <SettingRow
        label={t("settings.network.bind")}
        description={t("settings.network.bind_desc")}
        tooltip={t("settings.network.bind_tooltip")}
      >
        <select
          value={bindAddress}
          onChange={(e) => update({ bind_address: e.target.value })}
          className="rounded-md border px-3 py-1.5 text-sm"
          aria-label={t("settings.network.bind")}
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
          defaultValue={cidrs}
          onBlur={(e) =>
            update({
              allowed_cidrs: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
            })
          }
          aria-label={t("settings.network.cidrs")}
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
          onClick={() => update({ vpn_only: !vpnOnly })}
          className="relative h-6 w-11 rounded-full transition-colors"
          style={{
            backgroundColor: vpnOnly ? "var(--color-brand-primary)" : "var(--color-border)",
          }}
          role="switch"
          aria-checked={vpnOnly}
          aria-label={t("settings.network.vpn")}
        >
          <span
            className="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform"
            style={{ left: vpnOnly ? "calc(100% - 1.375rem)" : "0.125rem" }}
          />
        </button>
      </SettingRow>
    </div>
  );
}
