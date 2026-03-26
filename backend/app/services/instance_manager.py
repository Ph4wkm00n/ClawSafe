"""Instance manager — CRUD for OpenClaw instances."""

from __future__ import annotations

import logging
import uuid

from app.db.database import get_db
from app.models.instance import (
    InstanceCreate,
    InstanceList,
    InstanceResponse,
    InstanceUpdate,
)

logger = logging.getLogger(__name__)


async def list_instances() -> InstanceList:
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, name, config_path, tags, active, created_at "
        "FROM instances ORDER BY created_at"
    )
    instances = [
        InstanceResponse(
            id=row["id"],
            name=row["name"],
            config_path=row["config_path"],
            tags=row["tags"],
            active=bool(row["active"]),
            created_at=row["created_at"],
        )
        for row in rows
    ]
    return InstanceList(instances=instances, total=len(instances))


async def get_instance(instance_id: str) -> InstanceResponse | None:
    db = await get_db()
    row = await db.fetch_one(
        "SELECT id, name, config_path, tags, active, created_at "
        "FROM instances WHERE id = ?",
        (instance_id,),
    )
    if row is None:
        return None
    return InstanceResponse(
        id=row["id"],
        name=row["name"],
        config_path=row["config_path"],
        tags=row["tags"],
        active=bool(row["active"]),
        created_at=row["created_at"],
    )


async def create_instance(data: InstanceCreate) -> InstanceResponse:
    db = await get_db()
    instance_id = str(uuid.uuid4())[:8]
    await db.execute(
        "INSERT INTO instances (id, name, config_path, tags) VALUES (?, ?, ?, ?)",
        (instance_id, data.name, data.config_path, data.tags),
    )
    await db.commit()
    logger.info("Created instance %s (%s)", instance_id, data.name)
    return (await get_instance(instance_id))  # type: ignore[return-value]


async def update_instance(instance_id: str, data: InstanceUpdate) -> InstanceResponse | None:
    db = await get_db()
    existing = await get_instance(instance_id)
    if existing is None:
        return None

    updates = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.config_path is not None:
        updates["config_path"] = data.config_path
    if data.tags is not None:
        updates["tags"] = data.tags
    if data.active is not None:
        updates["active"] = 1 if data.active else 0

    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = tuple(updates.values()) + (instance_id,)
        await db.execute(f"UPDATE instances SET {set_clause} WHERE id = ?", values)
        await db.commit()

    return await get_instance(instance_id)


async def delete_instance(instance_id: str) -> bool:
    if instance_id == "default":
        return False  # Cannot delete the default instance
    db = await get_db()
    existing = await get_instance(instance_id)
    if existing is None:
        return False
    await db.execute("DELETE FROM instances WHERE id = ?", (instance_id,))
    await db.commit()
    logger.info("Deleted instance %s", instance_id)
    return True


async def get_active_instances() -> list[InstanceResponse]:
    """Get all active instances for scanning."""
    result = await list_instances()
    return [i for i in result.instances if i.active]
