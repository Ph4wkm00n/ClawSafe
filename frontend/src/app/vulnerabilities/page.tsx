"use client";

import { useCallback, useEffect, useState } from "react";

import EmptyState from "@/components/ui/EmptyState";
import { SkeletonCard } from "@/components/ui/Skeleton";
import StatusChip from "@/components/ui/StatusChip";
import { t } from "@/i18n/en";

interface Vulnerability {
  id: string;
  severity: string;
  title: string;
  package: string;
  installed_version: string;
  fixed_version: string;
}

interface Container {
  id: string;
  name: string;
  image: string;
  status: string;
  vulnerabilities?: Vulnerability[];
}

interface ScanResult {
  containers: Container[];
  total_containers: number;
  total_vulnerabilities: number;
  critical_vulnerabilities: number;
}

const SEVERITY_MAP: Record<string, "safe" | "attention" | "risk"> = {
  low: "safe",
  medium: "attention",
  high: "risk",
  critical: "risk",
};

export default function VulnerabilitiesPage() {
  const [data, setData] = useState<ScanResult | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";
      const resp = await fetch(`${API_BASE}/api/v1/vulnerabilities`, {
        headers: API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {},
      });
      setData(await resp.json());
    } catch {
      // Best effort
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  if (loading) {
    return (
      <div className="flex flex-col gap-6">
        <h1 className="text-2xl" style={{ fontWeight: "var(--font-weight-bold)" }}>
          {t("vulns.title")}
        </h1>
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  if (!data || data.total_containers === 0) {
    return (
      <div className="flex flex-col gap-6">
        <h1 className="text-2xl" style={{ fontWeight: "var(--font-weight-bold)" }}>
          {t("vulns.title")}
        </h1>
        <EmptyState
          icon="🐳"
          message={t("vulns.no_containers")}
          action={{ label: t("common.refresh"), onClick: refresh }}
        />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl" style={{ fontWeight: "var(--font-weight-bold)" }}>
          {t("vulns.title")}
        </h1>
        <button
          onClick={refresh}
          className="text-sm transition-opacity hover:opacity-70"
          style={{ color: "var(--color-brand-primary)" }}
        >
          {t("common.refresh")}
        </button>
      </div>

      {/* Summary */}
      <div
        className="flex gap-6 rounded-lg border p-5"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
        <div className="flex flex-col">
          <span className="text-2xl font-bold">{data.total_containers}</span>
          <span className="text-xs" style={{ color: "var(--color-text-muted)" }}>
            {t("vulns.containers")}
          </span>
        </div>
        <div className="flex flex-col">
          <span className="text-2xl font-bold">{data.total_vulnerabilities}</span>
          <span className="text-xs" style={{ color: "var(--color-text-muted)" }}>
            {t("vulns.total_vulns")}
          </span>
        </div>
        <div className="flex flex-col">
          <span className="text-2xl font-bold" style={{ color: "var(--color-status-risk)" }}>
            {data.critical_vulnerabilities}
          </span>
          <span className="text-xs" style={{ color: "var(--color-text-muted)" }}>
            {t("vulns.critical")}
          </span>
        </div>
      </div>

      {/* Container list */}
      {data.containers.map((container) => (
        <div
          key={container.id}
          className="flex flex-col gap-3 rounded-lg border p-5"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-lg)",
          }}
        >
          <div className="flex items-center justify-between">
            <div>
              <span className="font-semibold">{container.name}</span>
              <span className="ml-2 font-mono text-xs" style={{ color: "var(--color-text-muted)" }}>
                {container.image}
              </span>
            </div>
            <span className="text-xs" style={{ color: "var(--color-text-muted)" }}>
              {container.status}
            </span>
          </div>

          {container.vulnerabilities && container.vulnerabilities.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr style={{ color: "var(--color-text-secondary)" }}>
                    <th className="px-2 py-1 text-left">CVE</th>
                    <th className="px-2 py-1 text-left">Severity</th>
                    <th className="px-2 py-1 text-left">Package</th>
                    <th className="px-2 py-1 text-left">Fixed In</th>
                  </tr>
                </thead>
                <tbody>
                  {container.vulnerabilities.map((vuln) => (
                    <tr key={vuln.id} className="border-t" style={{ borderColor: "var(--color-border)" }}>
                      <td className="px-2 py-1 font-mono">{vuln.id}</td>
                      <td className="px-2 py-1">
                        <StatusChip status={SEVERITY_MAP[vuln.severity] || "attention"} size="sm" />
                      </td>
                      <td className="px-2 py-1">{vuln.package} {vuln.installed_version}</td>
                      <td className="px-2 py-1">{vuln.fixed_version || "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>
              {t("vulns.no_vulns")}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
