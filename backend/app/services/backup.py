"""Backup service — creates and restores config backups before fixes."""

from __future__ import annotations

import logging
import re
import shutil
from datetime import datetime
from pathlib import Path

from app.db.database import get_db
from app.models.schemas import BackupEntry, BackupList

logger = logging.getLogger(__name__)

BACKUP_DIR = Path("/data/backups")
MAX_BACKUPS = 50


def _sanitize_action_id(action_id: str) -> str:
    """Remove anything that isn't alphanumeric or underscore."""
    return re.sub(r"[^a-z0-9_]", "", action_id)


async def create_backup(config_path: str, action_id: str) -> int:
    """Copy config file and record backup in DB. Returns backup ID."""
    safe_id = _sanitize_action_id(action_id)
    src = Path(config_path)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{src.stem}_{ts}_{safe_id}{src.suffix}"
    dest = BACKUP_DIR / backup_name

    try:
        if src.exists():
            shutil.copy2(str(src), str(dest))
        else:
            dest.write_text("")
    except OSError as e:
        logger.error("Failed to create backup file %s: %s", dest, e)
        raise

    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO backups (config_path, backup_path, action_id) VALUES (?, ?, ?)",
        (str(src), str(dest), safe_id),
    )
    await db.commit()

    await _cleanup_old_backups()

    return cursor.lastrowid or 0


async def list_backups() -> BackupList:
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, timestamp, config_path, backup_path, action_id, status "
        "FROM backups ORDER BY timestamp DESC"
    )
    rows = await cursor.fetchall()
    entries = [
        BackupEntry(
            id=row[0],
            timestamp=row[1],
            config_path=row[2],
            backup_path=row[3],
            action_id=row[4],
            status=row[5],
        )
        for row in rows
    ]
    return BackupList(backups=entries)


async def restore_backup(backup_id: int) -> bool:
    """Restore config from a backup. Returns True on success."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT config_path, backup_path FROM backups WHERE id = ?", (backup_id,)
    )
    row = await cursor.fetchone()
    if row is None:
        return False

    config_path, backup_path = row[0], row[1]
    backup = Path(backup_path)
    if not backup.exists():
        logger.error("Backup file missing: %s", backup_path)
        return False

    try:
        shutil.copy2(str(backup), config_path)
    except OSError as e:
        logger.error("Failed to restore backup %s: %s", backup_path, e)
        return False

    await db.execute(
        "UPDATE backups SET status = 'restored' WHERE id = ?", (backup_id,)
    )
    await db.commit()
    return True


async def _cleanup_old_backups() -> None:
    """Remove oldest backups if we exceed MAX_BACKUPS."""
    db = await get_db()
    cursor = await db.execute("SELECT COUNT(*) FROM backups")
    count = (await cursor.fetchone())[0]
    if count <= MAX_BACKUPS:
        return

    to_delete = count - MAX_BACKUPS
    cursor = await db.execute(
        "SELECT id, backup_path FROM backups ORDER BY timestamp ASC LIMIT ?",
        (to_delete,),
    )
    rows = await cursor.fetchall()
    for row in rows:
        path = Path(row[1])
        if path.exists():
            try:
                path.unlink()
            except OSError:
                pass
        await db.execute("DELETE FROM backups WHERE id = ?", (row[0],))
    await db.commit()
    logger.info("Cleaned up %d old backups", to_delete)
