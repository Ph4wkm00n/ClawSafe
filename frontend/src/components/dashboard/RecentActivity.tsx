"use client";

import Link from "next/link";

import { t } from "@/i18n/en";
import type { ActivityEvent, SafetyLevel } from "@/lib/types";

const SEVERITY_DOTS: Record<SafetyLevel, string> = {
  safe: "var(--color-status-safe)",
  attention: "var(--color-status-attention)",
  risk: "var(--color-status-risk)",
};

const SEVERITY_LABELS: Record<SafetyLevel, string> = {
  safe: "info",
  attention: "warning",
  risk: "critical",
};

interface RecentActivityProps {
  events: ActivityEvent[];
  loading: boolean;
}

export default function RecentActivity({
  events,
  loading,
}: RecentActivityProps) {
  return (
    <div
      className="flex flex-col gap-3 border p-5"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderColor: "var(--color-border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-sm)",
      }}
    >
      <h3
        className="text-base"
        style={{ fontWeight: "var(--font-weight-semibold)" }}
      >
        {t("nav.activity")}
      </h3>

      {loading && (
        <p className="text-sm" style={{ color: "var(--color-text-muted)" }}>
          {t("common.loading")}
        </p>
      )}

      {!loading && events.length === 0 && (
        <p className="text-sm" style={{ color: "var(--color-text-muted)" }}>
          {t("activity.empty")}
        </p>
      )}

      <div className="flex flex-col gap-2">
        {events.map((event) => (
          <div key={event.id} className="flex items-start gap-3 text-sm">
            <span
              className="mt-1.5 h-2 w-2 shrink-0 rounded-full"
              style={{ backgroundColor: SEVERITY_DOTS[event.severity] }}
              aria-label={SEVERITY_LABELS[event.severity]}
              title={SEVERITY_LABELS[event.severity]}
            />
            <span style={{ color: "var(--color-text-muted)" }} className="shrink-0 text-xs">
              {new Date(event.timestamp).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
            <span style={{ color: "var(--color-text-primary)" }}>
              {event.description}
            </span>
          </div>
        ))}
      </div>

      {events.length > 0 && (
        <Link
          href="/activity"
          className="text-sm transition-opacity hover:opacity-70"
          style={{ color: "var(--color-brand-primary)" }}
        >
          {t("activity.view_all")}
        </Link>
      )}
    </div>
  );
}
