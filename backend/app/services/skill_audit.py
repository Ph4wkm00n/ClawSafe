"""Skill execution auditing — track which skills ran, what they accessed."""

from __future__ import annotations

import json
import logging

from app.db.database import get_db
from app.models.schemas import SkillExecution

logger = logging.getLogger(__name__)


async def log_skill_execution(
    skill_name: str,
    instance_id: str | None = None,
    parameters: dict | None = None,
    result: dict | None = None,
    duration_ms: int = 0,
) -> int:
    """Log a skill execution event. Returns the execution ID."""
    db = await get_db()
    exec_id = await db.insert_returning_id(
        "INSERT INTO skill_executions (instance_id, skill_name, parameters, result, duration_ms) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            instance_id,
            skill_name,
            json.dumps(parameters or {}),
            json.dumps(result or {}),
            duration_ms,
        ),
    )
    await db.commit()
    logger.info("Logged skill execution: %s (id=%d, %dms)", skill_name, exec_id, duration_ms)
    return exec_id


async def get_skill_executions(
    instance_id: str | None = None,
    skill_name: str | None = None,
    limit: int = 50,
) -> list[SkillExecution]:
    """Query skill execution history."""
    db = await get_db()

    query = "SELECT id, instance_id, skill_name, parameters, result, duration_ms, timestamp FROM skill_executions"
    conditions = []
    params: list = []

    if instance_id:
        conditions.append("instance_id = ?")
        params.append(instance_id)
    if skill_name:
        conditions.append("skill_name = ?")
        params.append(skill_name)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    rows = await db.fetch_all(query, tuple(params))
    return [
        SkillExecution(
            id=row["id"],
            instance_id=row["instance_id"],
            skill_name=row["skill_name"],
            parameters=row["parameters"],
            result=row["result"],
            duration_ms=row["duration_ms"],
            timestamp=row["timestamp"],
        )
        for row in rows
    ]


async def get_skill_execution_stats() -> dict:
    """Get aggregated skill execution statistics."""
    db = await get_db()
    total = await db.fetch_scalar("SELECT COUNT(*) FROM skill_executions") or 0
    by_skill = await db.fetch_all(
        "SELECT skill_name, COUNT(*) as count, AVG(duration_ms) as avg_duration "
        "FROM skill_executions GROUP BY skill_name ORDER BY count DESC LIMIT 20"
    )
    return {
        "total_executions": total,
        "by_skill": [
            {
                "skill_name": row["skill_name"],
                "count": row["count"],
                "avg_duration_ms": round(row["avg_duration"] or 0, 1),
            }
            for row in by_skill
        ],
    }
