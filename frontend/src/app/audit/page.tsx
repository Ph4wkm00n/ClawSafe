"use client";

import { useCallback, useEffect, useState } from "react";

import { t } from "@/i18n/en";

interface AuditEntry {
  id: number;
  timestamp: string;
  user_email: string;
  action: string;
  resource: string;
  resource_id: string;
  details: string;
}

export default function AuditPage() {
  const [entries, setEntries] = useState<AuditEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";
      const resp = await fetch(`${API_BASE}/api/v1/audit?limit=100`, {
        headers: API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {},
      });
      const data = await resp.json();
      setEntries(data.entries || []);
      setTotal(data.total || 0);
    } catch {
      // Best effort
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl" style={{ fontWeight: "var(--font-weight-bold)" }}>
        {t("audit.title")}
      </h1>

      <div
        className="overflow-x-auto rounded-lg border"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        <table className="w-full text-sm">
          <thead>
            <tr style={{ backgroundColor: "var(--color-bg-accent)", color: "var(--color-text-secondary)" }}>
              <th className="px-4 py-2.5 text-left font-medium">{t("audit.time")}</th>
              <th className="px-4 py-2.5 text-left font-medium">{t("audit.user")}</th>
              <th className="px-4 py-2.5 text-left font-medium">{t("audit.action")}</th>
              <th className="px-4 py-2.5 text-left font-medium">{t("audit.resource")}</th>
              <th className="px-4 py-2.5 text-left font-medium">{t("audit.details")}</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center" style={{ color: "var(--color-text-muted)" }}>
                  {t("common.loading")}
                </td>
              </tr>
            )}
            {!loading && entries.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center" style={{ color: "var(--color-text-muted)" }}>
                  {t("audit.empty")}
                </td>
              </tr>
            )}
            {entries.map((entry) => (
              <tr key={entry.id} className="border-t" style={{ borderColor: "var(--color-border)" }}>
                <td className="px-4 py-2 text-xs" style={{ color: "var(--color-text-muted)" }}>
                  {new Date(entry.timestamp).toLocaleString()}
                </td>
                <td className="px-4 py-2 text-xs">{entry.user_email || "system"}</td>
                <td className="px-4 py-2 text-xs font-mono">{entry.action}</td>
                <td className="px-4 py-2 text-xs">{entry.resource}{entry.resource_id ? `/${entry.resource_id}` : ""}</td>
                <td className="px-4 py-2 text-xs" style={{ color: "var(--color-text-secondary)" }}>
                  {entry.details || "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {total > entries.length && (
        <p className="text-center text-xs" style={{ color: "var(--color-text-muted)" }}>
          Showing {entries.length} of {total} entries
        </p>
      )}
    </div>
  );
}
