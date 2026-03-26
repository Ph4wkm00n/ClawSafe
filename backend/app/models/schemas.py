from enum import Enum

from pydantic import BaseModel


class SafetyLevel(str, Enum):
    safe = "safe"
    attention = "attention"
    risk = "risk"


class CategoryName(str, Enum):
    network = "network"
    tools = "tools"
    data = "data"
    updates = "updates"


CATEGORY_LABELS = {
    CategoryName.network: "Network",
    CategoryName.tools: "Tools & Skills",
    CategoryName.data: "Data & Files",
    CategoryName.updates: "Updates & Health",
}


class CategoryStatus(BaseModel):
    category: CategoryName
    label: str
    status: SafetyLevel
    score: int
    summary: str
    description: str
    action_label: str
    action_id: str


class OverallStatus(BaseModel):
    status: SafetyLevel
    score: int
    subtitle: str
    categories: list[CategoryStatus]


class ActivityEvent(BaseModel):
    id: int
    timestamp: str
    event_type: str
    description: str
    severity: SafetyLevel


class ActivityList(BaseModel):
    events: list[ActivityEvent]
    total: int


class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    category: CategoryName
    severity: SafetyLevel
    action_label: str
    steps: list[str]
    commands: list[str]


class UserSettings(BaseModel):
    onboarding_complete: bool = False
    theme: str = "playful"
    mode: str = "system"
    usage_type: str = ""
    network_preference: str = ""


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"


class FixResult(BaseModel):
    success: bool
    action_id: str
    message: str
    backup_id: int | None = None


class BackupEntry(BaseModel):
    id: int
    timestamp: str
    config_path: str
    backup_path: str
    action_id: str
    status: str


class BackupList(BaseModel):
    backups: list[BackupEntry]


class PolicyConfig(BaseModel):
    version: str = "1"
    name: str = "default"
    network: dict = {}
    tools: dict = {}
    data: dict = {}
    auth: dict = {}
    monitoring: dict = {}
    integrations: dict = {}


class PolicyValidation(BaseModel):
    valid: bool
    errors: list[str] = []


class PolicyResponse(BaseModel):
    id: int | None = None
    name: str
    active: bool
    config: PolicyConfig


class WebhookConfig(BaseModel):
    url: str
    name: str = ""
    events: list[str] = ["escalation"]


class NotificationConfig(BaseModel):
    webhooks: list[WebhookConfig] = []
    email_enabled: bool = False
    email_address: str = ""
    events: list[str] = ["escalation", "weekly_summary"]


class ScanHistoryEntry(BaseModel):
    id: int
    timestamp: str
    overall_status: str
    score: int


class ScanHistoryList(BaseModel):
    scans: list[ScanHistoryEntry]
    total: int


class SkillStatusResponse(BaseModel):
    summary: str
    status: str
    score: int
    top_actions: list[str]
