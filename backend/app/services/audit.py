"""Audit trail — records who changed what, when."""

from __future__ import annotations

import logging

from app.db.database import get_db

logger = logging.getLogger(__name__)


async def log_audit(
    action: str,
    resource: str,
    resource_id: str = "",
    details: str = "",
    user_id: str = "",
    user_email: str = "",
    ip_address: str = "",
) -> None:
    """Record an action in the audit trail."""
    db = await get_db()
    await db.execute(
        "INSERT INTO audit_log (user_id, user_email, action, resource, resource_id, details, ip_address) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, user_email, action, resource, resource_id, details, ip_address),
    )
    await db.commit()
    logger.info("Audit: %s %s/%s by %s", action, resource, resource_id, user_email or "system")


async def get_audit_log(limit: int = 50, offset: int = 0) -> dict:
    """Get recent audit log entries."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, timestamp, user_id, user_email, action, resource, resource_id, details, ip_address "
        "FROM audit_log ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )
    total = await db.fetch_scalar("SELECT COUNT(*) FROM audit_log") or 0
    return {"entries": rows, "total": total}
