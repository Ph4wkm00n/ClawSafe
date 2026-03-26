"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { getActivity } from "@/lib/api";
import type { ActivityEvent } from "@/lib/types";

const BASE_INTERVAL = 30_000;
const MAX_INTERVAL = 300_000;

export function useActivity(limit = 5) {
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef(BASE_INTERVAL);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const refresh = useCallback(async () => {
    try {
      const data = await getActivity(limit);
      setEvents(data.events);
      setTotal(data.total);
      intervalRef.current = BASE_INTERVAL;
    } catch {
      intervalRef.current = Math.min(intervalRef.current * 2, MAX_INTERVAL);
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    refresh();

    const poll = () => {
      timerRef.current = setTimeout(async () => {
        await refresh();
        poll();
      }, intervalRef.current);
    };
    poll();

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [refresh]);

  return { events, total, loading, refresh };
}
