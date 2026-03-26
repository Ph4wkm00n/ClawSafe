import aiosqlite

from app.core.config import settings

_db: aiosqlite.Connection | None = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    overall_status TEXT NOT NULL,
    score INTEGER NOT NULL,
    results_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    event_type TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'safe'
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    config_path TEXT NOT NULL,
    backup_path TEXT NOT NULL,
    action_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    name TEXT NOT NULL,
    content_json TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 0
);
"""


async def get_db() -> aiosqlite.Connection:
    global _db
    if _db is None:
        _db = await aiosqlite.connect(settings.database_path)
        _db.row_factory = aiosqlite.Row
        await _db.executescript(SCHEMA)
        await _db.commit()
    return _db


async def close_db() -> None:
    global _db
    if _db is not None:
        await _db.close()
        _db = None
