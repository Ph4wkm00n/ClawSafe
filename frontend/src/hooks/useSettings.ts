"use client";

import { useCallback, useEffect, useState } from "react";

import { getSettings, updateSettings } from "@/lib/api";
import type { UserSettings } from "@/lib/types";

const DEFAULT_SETTINGS: UserSettings = {
  onboarding_complete: false,
  theme: "playful",
  mode: "system",
  usage_type: "",
  network_preference: "",
};

export function useSettings() {
  const [settings, setSettings] = useState<UserSettings>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSettings()
      .then(setSettings)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const save = useCallback(async (updated: UserSettings) => {
    setSettings(updated);
    try {
      await updateSettings(updated);
    } catch {
      // Best effort
    }
  }, []);

  return { settings, loading, save };
}
