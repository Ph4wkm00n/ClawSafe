export type SafetyLevel = "safe" | "attention" | "risk";

export type CategoryName = "network" | "tools" | "data" | "updates";

export interface CategoryStatus {
  category: CategoryName;
  label: string;
  status: SafetyLevel;
  score: number;
  summary: string;
  description: string;
  action_label: string;
  action_id: string;
}

export interface OverallStatus {
  status: SafetyLevel;
  score: number;
  subtitle: string;
  categories: CategoryStatus[];
}

export interface ActivityEvent {
  id: number;
  timestamp: string;
  event_type: string;
  description: string;
  severity: SafetyLevel;
}

export interface ActivityList {
  events: ActivityEvent[];
  total: number;
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  category: CategoryName;
  severity: SafetyLevel;
  action_label: string;
  steps: string[];
  commands: string[];
}

export interface UserSettings {
  onboarding_complete: boolean;
  theme: string;
  mode: string;
  usage_type: string;
  network_preference: string;
}

export interface FixResult {
  success: boolean;
  action_id: string;
  message: string;
  backup_id: number | null;
}

export interface BackupEntry {
  id: number;
  timestamp: string;
  config_path: string;
  backup_path: string;
  action_id: string;
  status: string;
}

export interface PolicyConfig {
  version: string;
  name: string;
  network: Record<string, unknown>;
  tools: Record<string, unknown>;
  data: Record<string, unknown>;
  auth: Record<string, unknown>;
  monitoring: Record<string, unknown>;
  integrations: Record<string, unknown>;
}

export interface PolicyValidation {
  valid: boolean;
  errors: string[];
}

export interface PolicyResponse {
  id: number | null;
  name: string;
  active: boolean;
  config: PolicyConfig;
}

export type SkillAction = "allow" | "ask" | "block";

export interface SkillRule {
  name: string;
  risk: string;
  action: SkillAction;
  enabled?: boolean;
}
