"""API key authentication for write endpoints."""

from __future__ import annotations

import re

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import settings

_api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

VALID_ACTION_ID = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


async def require_auth(api_key: str | None = Security(_api_key_header)) -> None:
    """Dependency that enforces API key auth on write endpoints.

    If CLAWSAFE_API_KEY is empty, auth is disabled (dev mode).
    """
    if not settings.api_key:
        return
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing Authorization header.")
    token = api_key.removeprefix("Bearer ").strip()
    if token != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")


def validate_action_id(action_id: str) -> str:
    """Validate action_id to prevent path traversal."""
    if not VALID_ACTION_ID.match(action_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid action_id '{action_id}'. Must be lowercase alphanumeric with underscores.",
        )
    return action_id
