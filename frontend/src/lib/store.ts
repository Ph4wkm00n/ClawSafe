/**
 * Global state management with Zustand + cross-tab sync via BroadcastChannel.
 */
import { create } from "zustand";

interface StatusData {
  status: string;
  score: number;
  subtitle: string;
  categories: Array<{
    category: string;
    label: string;
    status: string;
    score: number;
    summary: string;
  }>;
}

interface ActivityEvent {
  id: number;
  timestamp: string;
  event_type: string;
  description: string;
  severity: string;
}

interface AppState {
  // Status
  status: StatusData | null;
  statusLoading: boolean;
  setStatus: (status: StatusData | null) => void;
  setStatusLoading: (loading: boolean) => void;

  // Activity
  activity: ActivityEvent[];
  activityLoading: boolean;
  setActivity: (events: ActivityEvent[]) => void;
  setActivityLoading: (loading: boolean) => void;

  // Settings
  theme: string;
  mode: string;
  setTheme: (theme: string) => void;
  setMode: (mode: string) => void;

  // Instances
  instances: Array<{ id: string; name: string; active: boolean }>;
  setInstances: (instances: Array<{ id: string; name: string; active: boolean }>) => void;

  // Last refresh timestamp
  lastRefresh: number;
  setLastRefresh: (ts: number) => void;
}

export const useAppStore = create<AppState>((set) => ({
  status: null,
  statusLoading: false,
  setStatus: (status) => set({ status, lastRefresh: Date.now() }),
  setStatusLoading: (statusLoading) => set({ statusLoading }),

  activity: [],
  activityLoading: false,
  setActivity: (activity) => set({ activity }),
  setActivityLoading: (activityLoading) => set({ activityLoading }),

  theme: "playful",
  mode: "system",
  setTheme: (theme) => set({ theme }),
  setMode: (mode) => set({ mode }),

  instances: [],
  setInstances: (instances) => set({ instances }),

  lastRefresh: 0,
  setLastRefresh: (lastRefresh) => set({ lastRefresh }),
}));

// Cross-tab sync via BroadcastChannel
if (typeof window !== "undefined" && "BroadcastChannel" in window) {
  const channel = new BroadcastChannel("clawsafe-sync");

  // Listen for updates from other tabs
  channel.onmessage = (event) => {
    const { type, payload } = event.data;
    const store = useAppStore.getState();

    switch (type) {
      case "theme":
        store.setTheme(payload);
        break;
      case "mode":
        store.setMode(payload);
        break;
      case "status":
        store.setStatus(payload);
        break;
    }
  };

  // Broadcast theme/mode changes to other tabs
  const originalSetTheme = useAppStore.getState().setTheme;
  const originalSetMode = useAppStore.getState().setMode;

  useAppStore.setState({
    setTheme: (theme: string) => {
      originalSetTheme(theme);
      channel.postMessage({ type: "theme", payload: theme });
    },
    setMode: (mode: string) => {
      originalSetMode(mode);
      channel.postMessage({ type: "mode", payload: mode });
    },
  });
}
