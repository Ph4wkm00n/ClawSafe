"use client";

import { useState } from "react";

import CategoryCards from "@/components/dashboard/CategoryCards";
import FixFlow from "@/components/dashboard/FixFlow";
import RecentActivity from "@/components/dashboard/RecentActivity";
import StatusHeader from "@/components/dashboard/StatusHeader";
import ErrorState from "@/components/ui/ErrorState";
import { SkeletonCard, SkeletonStatus } from "@/components/ui/Skeleton";
import { useActivity } from "@/hooks/useActivity";
import { useStatus } from "@/hooks/useStatus";

export default function DashboardPage() {
  const { status, loading, error, refresh } = useStatus();
  const { events, loading: activityLoading } = useActivity(5);
  const [activeFixId, setActiveFixId] = useState<string | null>(null);

  if (error) {
    return <ErrorState message={error} onRetry={refresh} />;
  }

  if (loading || !status) {
    return (
      <div className="flex flex-col gap-6">
        <SkeletonStatus />
        <div className="grid gap-4 sm:grid-cols-2">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
      </div>
    );
  }

  return (
    <div id="main-content" className="flex flex-col gap-6">
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
