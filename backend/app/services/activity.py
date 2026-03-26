"""Activity service — logs and retrieves security-relevant events."""

from __future__ import annotations

from app.db.database import get_db
from app.models.schemas import ActivityEvent, ActivityList


async def log_event(
    event_type: str,
    description: str,
    severity: str = "safe",
) -> None:
    db = await get_db()
    await db.execute(
        "INSERT INTO activity (event_type, description, severity) VALUES (?, ?, ?)",
        (event_type, description, severity),
    )
    await db.commit()


async def get_recent(limit: int = 20, offset: int = 0) -> ActivityList:
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, timestamp, event_type, description, severity "
        "FROM activity ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )
    rows = await cursor.fetchall()

    count_cursor = await db.execute("SELECT COUNT(*) FROM activity")
    total = (await count_cursor.fetchone())[0]

    events = [
        ActivityEvent(
            id=row[0],
            timestamp=row[1],
            event_type=row[2],
            description=row[3],
            severity=row[4],
        )
        for row in rows
    ]

    return ActivityList(events=events, total=total)


async def seed_demo_activity() -> None:
    """Insert demo activity events if the table is empty."""
    db = await get_db()
    cursor = await db.execute("SELECT COUNT(*) FROM activity")
    count = (await cursor.fetchone())[0]
    if count > 0:
        return

    demo_events = [
        ("skill_change", "New skill 'shell_exec' enabled", "risk"),
        ("config_change", "Port changed from 127.0.0.1 to 0.0.0.0", "risk"),
        ("policy_update", "Policy updated by user", "safe"),
        ("scan_complete", "Security scan completed — 3 issues found", "attention"),
        ("auth_change", "Authentication was disabled", "risk"),
    ]
    for event_type, description, severity in demo_events:
        await db.execute(
            "INSERT INTO activity (event_type, description, severity) VALUES (?, ?, ?)",
            (event_type, description, severity),
        )
    await db.commit()
