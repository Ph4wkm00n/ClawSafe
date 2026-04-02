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
    version: str = "2.0.0"


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
    format: str = "json"  # "json", "slack", "teams"
    hmac_secret: str = ""


class NotificationConfig(BaseModel):
    webhooks: list[WebhookConfig] = []
    email_enabled: bool = False
    email_address: str = ""
    events: list[str] = ["escalation", "weekly_summary"]
    dnd_start: str = ""  # HH:MM (e.g., "22:00")
    dnd_end: str = ""  # HH:MM (e.g., "08:00")
    digest_enabled: bool = False
    digest_interval: str = "daily"  # "daily" or "weekly"


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


# ── v1.2+ Models ──────────────────────────────────────────────────────────────


class NotificationTemplate(BaseModel):
    id: int | None = None
    name: str
    channel: str = "json"
    template_text: str
    created_at: str | None = None


class NotificationTemplateCreate(BaseModel):
    name: str
    channel: str = "json"
    template_text: str


class ApiKeyCreate(BaseModel):
    name: str
    expires_in_days: int | None = None


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    expires_at: str | None = None
    revoked: bool = False
    created_at: str


class ApiKeyCreated(BaseModel):
    id: int
    name: str
    key: str  # Only returned on creation
    key_prefix: str
    expires_at: str | None = None


class InstancePermission(BaseModel):
    id: int | None = None
    user_id: int
    instance_id: str
    role: str = "viewer"


class InstancePermissionCreate(BaseModel):
    user_id: int
    instance_id: str
    role: str = "viewer"


class InstanceScore(BaseModel):
    instance_id: str
    score: int
    status: str
    timestamp: str


class PolicyTemplateResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    config: PolicyConfig


class PolicySimulationRequest(BaseModel):
    policy: dict
    findings: dict | None = None


class PolicySimulationResult(BaseModel):
    current_score: int
    simulated_score: int
    current_status: str
    simulated_status: str
    category_changes: list[dict]


class SkillExecution(BaseModel):
    id: int | None = None
    instance_id: str | None = None
    skill_name: str
    parameters: str = "{}"
    result: str = "{}"
    duration_ms: int = 0
    timestamp: str | None = None


class EvidenceEntry(BaseModel):
    id: int | None = None
    compliance_control: str
    snapshot_json: str
    captured_at: str | None = None


class SbomEntry(BaseModel):
    name: str
    version: str
    license: str = "unknown"
    type: str = "library"


class SbomResponse(BaseModel):
    format: str = "CycloneDX"
    spec_version: str = "1.4"
    components: list[SbomEntry]
    generated_at: str


class IntegrationConfig(BaseModel):
    pagerduty_routing_key: str = ""
    jira_url: str = ""
    jira_project: str = ""
    jira_email: str = ""
    jira_token: str = ""
    github_repo: str = ""
    github_token: str = ""
    enabled_integrations: list[str] = []


class ComparisonItem(BaseModel):
    field: str
    current_value: str
    recommended_value: str
    status: str  # "match", "mismatch", "missing"


class ComparisonResponse(BaseModel):
    items: list[ComparisonItem]
    match_percentage: int


class BulkFixRequest(BaseModel):
    action_id: str


class BulkFixResponse(BaseModel):
    results: list[FixResult]
    total: int
    succeeded: int
    failed: int
