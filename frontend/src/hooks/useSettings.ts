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

function applyThemeToDOM(theme: string, mode: string) {
  document.documentElement.setAttribute(
    "data-theme",
    theme === "minimal" ? "minimal" : "playful"
  );
  if (mode === "dark") {
    document.documentElement.setAttribute("data-mode", "dark");
  } else if (mode === "light") {
    document.documentElement.removeAttribute("data-mode");
  } else {
    const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (dark) {
      document.documentElement.setAttribute("data-mode", "dark");
    } else {
      document.documentElement.removeAttribute("data-mode");
    }
  }
  // Persist to localStorage for flash prevention
  try {
    localStorage.setItem("clawsafe-theme", theme);
    localStorage.setItem("clawsafe-mode", mode);
  } catch {
    // localStorage might be unavailable
  }
}

export function useSettings() {
  const [settings, setSettings] = useState<UserSettings>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSettings()
      .then((s) => {
        setSettings(s);
        applyThemeToDOM(s.theme, s.mode);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  // Listen for system preference changes
  useEffect(() => {
    if (settings.mode !== "system") return;
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => {
      if (e.matches) {
        document.documentElement.setAttribute("data-mode", "dark");
      } else {
        document.documentElement.removeAttribute("data-mode");
      }
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [settings.mode]);

  const save = useCallback(async (updated: UserSettings) => {
    setSettings(updated);
    applyThemeToDOM(updated.theme, updated.mode);
    try {
      await updateSettings(updated);
    } catch {
      // Best effort
    }
  }, []);

  return { settings, loading, save };
}
