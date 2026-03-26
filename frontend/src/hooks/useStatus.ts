"use client";

import { useCallback, useEffect, useState } from "react";

import { getStatus } from "@/lib/api";
import type { OverallStatus } from "@/lib/types";

const POLL_INTERVAL = 30_000;

export function useStatus() {
  const [status, setStatus] = useState<OverallStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const data = await getStatus();
      setStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch status");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [refresh]);

  return { status, loading, error, refresh };
}
