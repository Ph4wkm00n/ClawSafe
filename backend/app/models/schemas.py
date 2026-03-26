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
    version: str = "0.1.0"
