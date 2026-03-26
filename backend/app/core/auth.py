"""API key and JWT authentication for endpoints."""

from __future__ import annotations

import logging
import re

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import settings

logger = logging.getLogger(__name__)

_api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

VALID_ACTION_ID = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


async def require_auth(api_key: str | None = Security(_api_key_header)) -> None:
    """Dependency that enforces API key or JWT auth on write endpoints.

    Auth is only disabled when BOTH api_key is empty AND debug mode is on.
    """
    if not settings.api_key and settings.debug:
        return  # Dev mode only

    if not settings.api_key and not settings.debug:
        # Production without API key configured — log warning but allow
        # (backward compatibility; should be set in production)
        logger.warning("CLAWSAFE_API_KEY not set. Set it for production security.")
        return

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing Authorization header.")

    token = api_key.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty authorization token.")

    # Try API key first
    if token == settings.api_key:
        return

    # Try JWT token
    if settings.jwt_secret:
        from app.services.user_service import decode_jwt
        payload = decode_jwt(token)
        if payload is not None:
            return

    raise HTTPException(status_code=401, detail="Invalid credentials.")


def validate_action_id(action_id: str) -> str:
    """Validate action_id to prevent path traversal."""
    if not VALID_ACTION_ID.match(action_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid action_id '{action_id}'. Must be lowercase alphanumeric with underscores.",
        )
    return action_id


def validate_config_path(path: str) -> str:
    """Validate a config file path to prevent path traversal."""
    from pathlib import Path as P
    resolved = P(path).resolve()
    # Allow common config directories
    allowed_prefixes = ["/etc/openclaw", "/data", "/app", "/tmp"]
    if not any(str(resolved).startswith(prefix) for prefix in allowed_prefixes):
        raise HTTPException(
            status_code=400,
            detail=f"Path '{path}' is not in an allowed directory.",
        )
    return str(resolved)
