"use client";

import { useCallback, useEffect, useState } from "react";

import { getActivity } from "@/lib/api";
import type { ActivityEvent } from "@/lib/types";

export function useActivity(limit = 5) {
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const data = await getActivity(limit);
      setEvents(data.events);
      setTotal(data.total);
    } catch {
      // Silently fail — dashboard still works without activity
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 30_000);
    return () => clearInterval(interval);
  }, [refresh]);

  return { events, total, loading, refresh };
}
