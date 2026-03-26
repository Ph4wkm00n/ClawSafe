"""Database initialization and connection management."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import aiosqlite

from app.core.config import settings
from app.db.queries import Database, SQLiteDatabase

logger = logging.getLogger(__name__)

_db: Database | None = None
_lock = asyncio.Lock()

MIGRATIONS_DIR = Path(__file__).parent.parent.parent / "migrations"


async def _run_migrations(db: Database) -> None:
    """Run any unapplied migration files."""
    await db.executescript(
        "CREATE TABLE IF NOT EXISTS schema_version ("
        "version INTEGER PRIMARY KEY, "
        "applied_at TEXT NOT NULL DEFAULT (datetime('now'))"
        ")"
    )

    applied = await db.fetch_all("SELECT version FROM schema_version ORDER BY version")
    applied_versions = {row["version"] for row in applied}

    if not MIGRATIONS_DIR.exists():
        return

    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for mf in migration_files:
        try:
            version = int(mf.stem.split("_")[0])
        except (ValueError, IndexError):
            continue
        if version in applied_versions:
            continue
        logger.info("Applying migration %s", mf.name)
        sql = mf.read_text()
        await db.executescript(sql)
        await db.execute(
            "INSERT OR IGNORE INTO schema_version (version) VALUES (?)", (version,)
        )
        await db.commit()


async def get_db() -> Database:
    """Get the database instance. Creates and migrates on first call."""
    global _db
    async with _lock:
        if _db is None:
            conn = await aiosqlite.connect(settings.database_path)
            _db = SQLiteDatabase(conn)
            await _run_migrations(_db)
    return _db


async def close_db() -> None:
    """Close the database connection."""
    global _db
    async with _lock:
        if _db is not None:
            await _db.close()
            _db = None


async def db_health_check() -> bool:
    """Return True if DB is responsive."""
    try:
        db = await get_db()
        return await db.health_check()
    except Exception:
        return False
