"""API key management service — create, list, revoke, and validate API keys."""

from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.schemas import ApiKeyCreate, ApiKeyCreated, ApiKeyResponse

logger = logging.getLogger(__name__)


def _hash_key(key: str) -> str:
    """Hash an API key with SHA-256."""
    return hashlib.sha256(key.encode()).hexdigest()


async def create_api_key(data: ApiKeyCreate, user_id: int | None = None) -> ApiKeyCreated:
    """Create a new API key. Returns the raw key (shown once)."""
    raw_key = f"cs_{secrets.token_urlsafe(32)}"
    key_hash = _hash_key(raw_key)
    key_prefix = raw_key[:10] + "..."

    expires_at = None
    if data.expires_in_days:
        expires_at = (datetime.utcnow() + timedelta(days=data.expires_in_days)).isoformat()

    db = await get_db()
    key_id = await db.insert_returning_id(
        "INSERT INTO api_keys (user_id, key_hash, name, expires_at) VALUES (?, ?, ?, ?)",
        (user_id, key_hash, data.name, expires_at),
    )
    await db.commit()
    logger.info("Created API key '%s' (id=%d)", data.name, key_id)

    return ApiKeyCreated(
        id=key_id,
        name=data.name,
        key=raw_key,
        key_prefix=key_prefix,
        expires_at=expires_at,
    )


async def list_api_keys(user_id: int | None = None) -> list[ApiKeyResponse]:
    """List all API keys (without revealing the actual key)."""
    db = await get_db()
    if user_id is not None:
        rows = await db.fetch_all(
            "SELECT id, name, key_hash, expires_at, revoked, created_at "
            "FROM api_keys WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
    else:
        rows = await db.fetch_all(
            "SELECT id, name, key_hash, expires_at, revoked, created_at "
            "FROM api_keys ORDER BY created_at DESC"
        )
    return [
        ApiKeyResponse(
            id=row["id"],
            name=row["name"],
            key_prefix=row["key_hash"][:10] + "...",
            expires_at=row["expires_at"],
            revoked=bool(row["revoked"]),
            created_at=row["created_at"],
        )
        for row in rows
    ]


async def revoke_api_key(key_id: int) -> bool:
    """Revoke an API key."""
    db = await get_db()
    row = await db.fetch_one("SELECT id FROM api_keys WHERE id = ?", (key_id,))
    if row is None:
        return False
    await db.execute("UPDATE api_keys SET revoked = 1 WHERE id = ?", (key_id,))
    await db.commit()
    logger.info("Revoked API key id=%d", key_id)
    return True


async def validate_api_key(key: str) -> bool:
    """Check if an API key is valid (exists, not revoked, not expired)."""
    key_hash = _hash_key(key)
    db = await get_db()
    row = await db.fetch_one(
        "SELECT id, expires_at, revoked FROM api_keys WHERE key_hash = ?",
        (key_hash,),
    )
    if row is None:
        return False
    if row["revoked"]:
        return False
    if row["expires_at"]:
        try:
            expires = datetime.fromisoformat(row["expires_at"])
            if datetime.utcnow() > expires:
                return False
        except (ValueError, TypeError):
            pass
    return True
