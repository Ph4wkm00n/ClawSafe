"""Data management — retention, export, and scheduled backup."""

from __future__ import annotations

import csv
import io
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.db.database import get_db

logger = logging.getLogger(__name__)


# ── Data Retention ──────────────────────────────────────────────────────────

async def purge_old_data(retention_days: int = 90) -> dict:
    """Delete scans and activity older than retention_days. Returns counts."""
    db = await get_db()
    cutoff = f"-{retention_days} days"

    await db.execute(
        "DELETE FROM scans WHERE timestamp < datetime('now', ?)", (cutoff,)
    )
    await db.execute(
        "DELETE FROM activity WHERE timestamp < datetime('now', ?)", (cutoff,)
    )
    await db.commit()

    # Get remaining counts
    scan_count = await db.fetch_scalar("SELECT COUNT(*) FROM scans") or 0
    activity_count = await db.fetch_scalar("SELECT COUNT(*) FROM activity") or 0

    logger.info("Purged data older than %d days", retention_days)
    return {
        "retention_days": retention_days,
        "remaining_scans": scan_count,
        "remaining_activity": activity_count,
    }


# ── Database Backup ─────────────────────────────────────────────────────────

async def create_db_backup(backup_dir: str = "/data/backups") -> str:
    """Create a backup of the SQLite database. Returns backup path."""
    if settings.db_type != "sqlite":
        raise ValueError("Scheduled backup only supported for SQLite. Use pg_dump for PostgreSQL.")

    src = Path(settings.database_path)
    if not src.exists():
        raise FileNotFoundError(f"Database not found: {src}")

    dest_dir = Path(backup_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    dest = dest_dir / f"clawsafe_db_{ts}.sqlite"

    shutil.copy2(str(src), str(dest))
    logger.info("Database backed up to %s", dest)
    return str(dest)


# ── CSV/JSON Export ─────────────────────────────────────────────────────────

async def export_scans(format: str = "json") -> str:
    """Export scan history to JSON or CSV string."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, timestamp, overall_status, score FROM scans ORDER BY timestamp DESC"
    )

    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "timestamp", "overall_status", "score"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return output.getvalue()

    return json.dumps(rows, indent=2, default=str)


async def export_activity(format: str = "json") -> str:
    """Export activity events to JSON or CSV string."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, timestamp, event_type, description, severity "
        "FROM activity ORDER BY timestamp DESC"
    )

    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "timestamp", "event_type", "description", "severity"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return output.getvalue()

    return json.dumps(rows, indent=2, default=str)
