"use client";

import { useState } from "react";

import CategoryCards from "@/components/dashboard/CategoryCards";
import FixFlow from "@/components/dashboard/FixFlow";
import RecentActivity from "@/components/dashboard/RecentActivity";
import StatusHeader from "@/components/dashboard/StatusHeader";
import { t } from "@/i18n/en";
import { useActivity } from "@/hooks/useActivity";
import { useStatus } from "@/hooks/useStatus";

export default function DashboardPage() {
  const { status, loading, refresh } = useStatus();
  const { events, loading: activityLoading } = useActivity(5);
  const [activeFixId, setActiveFixId] = useState<string | null>(null);

  if (loading || !status) {
    return (
      <div className="flex items-center justify-center py-20">
        <p style={{ color: "var(--color-text-muted)" }}>{t("common.loading")}</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <StatusHeader
        status={status.status}
        subtitle={status.subtitle}
        onRefresh={refresh}
      />

      <CategoryCards
        categories={status.categories}
        onAction={setActiveFixId}
      />

      <RecentActivity events={events} loading={activityLoading} />

      <FixFlow actionId={activeFixId} onClose={() => setActiveFixId(null)} />
    </div>
  );
}
