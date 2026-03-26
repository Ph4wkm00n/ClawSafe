"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { getStatus } from "@/lib/api";
import type { OverallStatus } from "@/lib/types";

const BASE_INTERVAL = 30_000;
const MAX_INTERVAL = 300_000;

export function useStatus() {
  const [status, setStatus] = useState<OverallStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef(BASE_INTERVAL);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const inFlightRef = useRef(false);

  const refresh = useCallback(async () => {
    if (inFlightRef.current) return;
    inFlightRef.current = true;
    try {
      const data = await getStatus();
      setStatus(data);
      setError(null);
      intervalRef.current = BASE_INTERVAL; // Reset on success
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch status");
      // Exponential backoff on failure
      intervalRef.current = Math.min(intervalRef.current * 2, MAX_INTERVAL);
    } finally {
      setLoading(false);
      inFlightRef.current = false;
    }
  }, []);

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

  return { status, loading, error, refresh };
}
