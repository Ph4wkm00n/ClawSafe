"""Backup service — creates and restores config backups before fixes."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from app.db.database import get_db
from app.models.schemas import BackupEntry, BackupList


BACKUP_DIR = Path("/data/backups")


async def create_backup(config_path: str, action_id: str) -> int:
    """Copy config file and record backup in DB. Returns backup ID."""
    src = Path(config_path)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{src.stem}_{ts}_{action_id}{src.suffix}"
    dest = BACKUP_DIR / backup_name

    if src.exists():
        shutil.copy2(str(src), str(dest))
    else:
        dest.write_text("")

    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO backups (config_path, backup_path, action_id) VALUES (?, ?, ?)",
        (str(src), str(dest), action_id),
    )
    await db.commit()
    return cursor.lastrowid  # type: ignore[return-value]


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
        return False

    shutil.copy2(str(backup), config_path)
    await db.execute(
        "UPDATE backups SET status = 'restored' WHERE id = ?", (backup_id,)
    )
    await db.commit()
    return True
