"use client";

import { t } from "@/i18n/en";
import { useActivity } from "@/hooks/useActivity";
import type { SafetyLevel } from "@/lib/types";

const SEVERITY_DOTS: Record<SafetyLevel, string> = {
  safe: "var(--color-status-safe)",
  attention: "var(--color-status-attention)",
  risk: "var(--color-status-risk)",
};

export default function ActivityPage() {
  const { events, total, loading } = useActivity(50);

  return (
    <div className="flex flex-col gap-6">
      <h1
        className="text-2xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        {t("activity.title")}
      </h1>

      <div
        className="flex flex-col gap-1 border p-5"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
        }}
      >
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

        {events.map((event) => (
          <div
            key={event.id}
            className="flex items-start gap-3 border-b py-3 text-sm last:border-b-0"
            style={{ borderColor: "var(--color-border)" }}
          >
            <span
              className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full"
              style={{ backgroundColor: SEVERITY_DOTS[event.severity] }}
            />
            <div className="flex flex-1 flex-col gap-0.5">
              <span style={{ color: "var(--color-text-primary)" }}>
                {event.description}
              </span>
              <span
                className="text-xs"
                style={{ color: "var(--color-text-muted)" }}
              >
                {new Date(event.timestamp).toLocaleString()} · {event.event_type}
              </span>
            </div>
          </div>
        ))}

        {total > events.length && (
          <p
            className="pt-2 text-center text-sm"
            style={{ color: "var(--color-text-muted)" }}
          >
            Showing {events.length} of {total} events
          </p>
        )}
      </div>
    </div>
  );
}
