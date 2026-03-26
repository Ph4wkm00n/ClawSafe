"""Instance models for multi-instance support."""

from pydantic import BaseModel


class InstanceCreate(BaseModel):
    name: str
    config_path: str
    tags: str = ""


class InstanceUpdate(BaseModel):
    name: str | None = None
    config_path: str | None = None
    tags: str | None = None
    active: bool | None = None


class InstanceResponse(BaseModel):
    id: str
    name: str
    config_path: str
    tags: str
    active: bool
    created_at: str


class InstanceList(BaseModel):
    instances: list[InstanceResponse]
    total: int
