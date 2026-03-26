"use client";

import { useCallback, useEffect, useState } from "react";

import { fetchAPI } from "@/lib/api";

export interface Instance {
  id: string;
  name: string;
  config_path: string;
  tags: string;
  active: boolean;
  created_at: string;
}

interface InstanceList {
  instances: Instance[];
  total: number;
}

// Re-export fetchAPI for use in this module
async function apiCall<T>(path: string, init?: RequestInit): Promise<T> {
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
  };
  const res = await fetch(`${API_BASE}${path}`, { headers, ...init });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json() as Promise<T>;
}

export function useInstances() {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const data = await apiCall<InstanceList>("/api/v1/instances");
      setInstances(data.instances);
    } catch {
      // Best effort
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const addInstance = useCallback(
    async (name: string, config_path: string) => {
      await apiCall<Instance>("/api/v1/instances", {
        method: "POST",
        body: JSON.stringify({ name, config_path }),
      });
      await refresh();
    },
    [refresh]
  );

  const removeInstance = useCallback(
    async (id: string) => {
      await apiCall("/api/v1/instances/" + id, { method: "DELETE" });
      await refresh();
    },
    [refresh]
  );

  return { instances, loading, refresh, addInstance, removeInstance };
}
