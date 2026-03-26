import type {
  ActivityList,
  OverallStatus,
  CategoryStatus,
  CategoryName,
  Recommendation,
  UserSettings,
  FixResult,
  BackupEntry,
  PolicyConfig,
  PolicyResponse,
  PolicyValidation,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";

async function fetchAPI<T>(path: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
  };
  const res = await fetch(`${API_BASE}${path}`, {
    headers,
    ...init,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export function getStatus(): Promise<OverallStatus> {
  return fetchAPI<OverallStatus>("/api/v1/status");
}

export function getCategoryStatus(
  category: CategoryName
): Promise<CategoryStatus> {
  return fetchAPI<CategoryStatus>(`/api/v1/status/${category}`);
}

export function getRecommendations(): Promise<Recommendation[]> {
  return fetchAPI<Recommendation[]>("/api/v1/recommendations");
}

export function getActivity(
  limit = 20,
  offset = 0
): Promise<ActivityList> {
  return fetchAPI<ActivityList>(
    `/api/v1/activity?limit=${limit}&offset=${offset}`
  );
}

export function getSettings(): Promise<UserSettings> {
  return fetchAPI<UserSettings>("/api/v1/settings");
}

export function updateSettings(
  settings: UserSettings
): Promise<UserSettings> {
  return fetchAPI<UserSettings>("/api/v1/settings", {
    method: "PUT",
    body: JSON.stringify(settings),
  });
}

export function applyFix(actionId: string): Promise<FixResult> {
  return fetchAPI<FixResult>(`/api/v1/fix/${actionId}`, { method: "POST" });
}

export function undoFix(actionId: string): Promise<FixResult> {
  return fetchAPI<FixResult>(`/api/v1/fix/${actionId}/undo`, { method: "POST" });
}

export function getBackups(): Promise<{ backups: BackupEntry[] }> {
  return fetchAPI<{ backups: BackupEntry[] }>("/api/v1/backups");
}

export function getPolicy(): Promise<PolicyResponse> {
  return fetchAPI<PolicyResponse>("/api/v1/policy");
}

export function updatePolicy(config: PolicyConfig): Promise<PolicyResponse> {
  return fetchAPI<PolicyResponse>("/api/v1/policy", {
    method: "PUT",
    body: JSON.stringify(config),
  });
}

export function validatePolicy(config: PolicyConfig): Promise<PolicyValidation> {
  return fetchAPI<PolicyValidation>("/api/v1/policy/validate", {
    method: "POST",
    body: JSON.stringify(config),
  });
}

export function getScans(limit = 20, offset = 0): Promise<{ scans: Array<{ id: number; timestamp: string; overall_status: string; score: number }>; total: number }> {
  return fetchAPI(`/api/v1/scans?limit=${limit}&offset=${offset}`);
}

export function getNotificationConfig(): Promise<Record<string, unknown>> {
  return fetchAPI("/api/v1/settings/notifications");
}

export function updateNotificationConfig(config: Record<string, unknown>): Promise<Record<string, unknown>> {
  return fetchAPI("/api/v1/settings/notifications", {
    method: "PUT",
    body: JSON.stringify(config),
  });
}

export function testNotification(url: string): Promise<{ success: boolean }> {
  return fetchAPI("/api/v1/settings/notifications/test", {
    method: "POST",
    body: JSON.stringify({ url }),
  });
}
