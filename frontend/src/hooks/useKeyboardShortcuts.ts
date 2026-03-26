"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

type ShortcutHandler = () => void;

const SHORTCUTS: Record<string, { key: string; handler?: string; description: string }> = {
  r: { key: "r", handler: "refresh", description: "Refresh dashboard" },
  d: { key: "d", handler: "navigate:/", description: "Go to Dashboard" },
  i: { key: "i", handler: "navigate:/instances", description: "Go to Instances" },
  a: { key: "a", handler: "navigate:/activity", description: "Go to Activity" },
  s: { key: "s", handler: "navigate:/settings", description: "Go to Settings" },
  "?": { key: "?", handler: "help", description: "Show keyboard shortcuts" },
};

export function useKeyboardShortcuts(handlers: Record<string, ShortcutHandler> = {}) {
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger shortcuts when typing in inputs
      const target = e.target as HTMLElement;
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.tagName === "SELECT") {
        return;
      }
      if (e.ctrlKey || e.metaKey || e.altKey) return;

      const key = e.key.toLowerCase();

      // Custom handlers first
      if (handlers[key]) {
        e.preventDefault();
        handlers[key]();
        return;
      }

      // Built-in navigation shortcuts
      const shortcut = SHORTCUTS[key];
      if (shortcut?.handler?.startsWith("navigate:")) {
        e.preventDefault();
        router.push(shortcut.handler.replace("navigate:", ""));
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handlers, router]);
}

export { SHORTCUTS };
