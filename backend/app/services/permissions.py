"""Instance permissions service — per-instance access control."""

from __future__ import annotations

import logging

from app.db.database import get_db
from app.models.schemas import InstancePermission, InstancePermissionCreate

logger = logging.getLogger(__name__)


async def grant_permission(data: InstancePermissionCreate) -> InstancePermission:
    """Grant a user access to an instance with a specific role."""
    db = await get_db()
    # Upsert: update role if permission already exists
    existing = await db.fetch_one(
        "SELECT id FROM instance_permissions WHERE user_id = ? AND instance_id = ?",
        (data.user_id, data.instance_id),
    )
    if existing:
        await db.execute(
            "UPDATE instance_permissions SET role = ? WHERE id = ?",
            (data.role, existing["id"]),
        )
        await db.commit()
        return InstancePermission(id=existing["id"], user_id=data.user_id, instance_id=data.instance_id, role=data.role)

    pid = await db.insert_returning_id(
        "INSERT INTO instance_permissions (user_id, instance_id, role) VALUES (?, ?, ?)",
        (data.user_id, data.instance_id, data.role),
    )
    await db.commit()
    logger.info("Granted %s access to instance %s for user %d", data.role, data.instance_id, data.user_id)
    return InstancePermission(id=pid, user_id=data.user_id, instance_id=data.instance_id, role=data.role)


async def revoke_permission(user_id: int, instance_id: str) -> bool:
    """Revoke a user's access to an instance."""
    db = await get_db()
    row = await db.fetch_one(
        "SELECT id FROM instance_permissions WHERE user_id = ? AND instance_id = ?",
        (user_id, instance_id),
    )
    if row is None:
        return False
    await db.execute("DELETE FROM instance_permissions WHERE id = ?", (row["id"],))
    await db.commit()
    logger.info("Revoked access to instance %s for user %d", instance_id, user_id)
    return True


async def get_user_permissions(user_id: int) -> list[InstancePermission]:
    """Get all instance permissions for a user."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, user_id, instance_id, role FROM instance_permissions WHERE user_id = ?",
        (user_id,),
    )
    return [
        InstancePermission(id=row["id"], user_id=row["user_id"], instance_id=row["instance_id"], role=row["role"])
        for row in rows
    ]


async def get_instance_permissions(instance_id: str) -> list[InstancePermission]:
    """Get all user permissions for an instance."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, user_id, instance_id, role FROM instance_permissions WHERE instance_id = ?",
        (instance_id,),
    )
    return [
        InstancePermission(id=row["id"], user_id=row["user_id"], instance_id=row["instance_id"], role=row["role"])
        for row in rows
    ]


async def check_instance_permission(user_id: int, instance_id: str, required_role: str = "viewer") -> bool:
    """Check if a user has the required role for an instance.

    Role hierarchy: admin > officer > viewer
    """
    role_levels = {"viewer": 0, "officer": 1, "admin": 2}

    # Check if user is a global admin
    db = await get_db()
    user_row = await db.fetch_one("SELECT role FROM users WHERE id = ?", (user_id,))
    if user_row and user_row["role"] == "admin":
        return True  # Global admins bypass instance permissions

    # Check instance-specific permission
    row = await db.fetch_one(
        "SELECT role FROM instance_permissions WHERE user_id = ? AND instance_id = ?",
        (user_id, instance_id),
    )
    if row is None:
        return False

    user_level = role_levels.get(row["role"], 0)
    required_level = role_levels.get(required_role, 0)
    return user_level >= required_level
