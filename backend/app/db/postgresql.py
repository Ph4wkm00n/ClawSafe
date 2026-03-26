"""PostgreSQL implementation of the Database abstraction."""

from __future__ import annotations

import re
from typing import Any

from app.db.queries import Database


def _convert_placeholders(sql: str) -> str:
    """Convert SQLite-style ? placeholders to PostgreSQL $1, $2, etc."""
    counter = 0

    def replace_placeholder(match):
        nonlocal counter
        counter += 1
        return f"${counter}"

    return re.sub(r"\?", replace_placeholder, sql)


def _convert_autoincrement(sql: str) -> str:
    """Convert SQLite AUTOINCREMENT to PostgreSQL SERIAL."""
    sql = re.sub(
        r"INTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT",
        "SERIAL PRIMARY KEY",
        sql,
        flags=re.IGNORECASE,
    )
    # datetime('now') → NOW()
    sql = sql.replace("datetime('now')", "NOW()")
    # INSERT OR REPLACE → INSERT ... ON CONFLICT
    sql = re.sub(
        r"INSERT\s+OR\s+REPLACE\s+INTO\s+(\w+)\s*\((\w+),\s*(\w+)\)\s*VALUES",
        r"INSERT INTO \1 (\2, \3) VALUES",
        sql,
        flags=re.IGNORECASE,
    )
    # INSERT OR IGNORE → INSERT ... ON CONFLICT DO NOTHING
    sql = re.sub(
        r"INSERT\s+OR\s+IGNORE\s+INTO",
        "INSERT INTO",
        sql,
        flags=re.IGNORECASE,
    )
    return sql


class PostgreSQLDatabase(Database):
    """PostgreSQL implementation using asyncpg."""

    def __init__(self, pool):
        self._pool = pool

    async def execute(self, sql: str, params: tuple = ()) -> Any:
        sql = _convert_placeholders(sql)
        # Handle INSERT OR REPLACE for settings table
        if "INSERT INTO settings" in sql.upper() and "VALUES" in sql.upper():
            sql = sql.rstrip(")") if not sql.endswith(")") else sql
            if "ON CONFLICT" not in sql.upper():
                sql += " ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value"
        async with self._pool.acquire() as conn:
            return await conn.execute(sql, *params)

    async def fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        sql = _convert_placeholders(sql)
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(sql, *params)
            if row is None:
                return None
            return dict(row)

    async def fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        sql = _convert_placeholders(sql)
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            return [dict(row) for row in rows]

    async def insert_returning_id(self, sql: str, params: tuple = ()) -> int:
        sql = _convert_placeholders(sql)
        # Add RETURNING id if not present
        if "RETURNING" not in sql.upper():
            sql = sql.rstrip(";") + " RETURNING id"
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(sql, *params)
            return row["id"] if row else 0

    async def commit(self) -> None:
        # asyncpg auto-commits; no-op unless using transactions
        pass

    async def executescript(self, sql: str) -> None:
        sql = _convert_autoincrement(sql)
        async with self._pool.acquire() as conn:
            await conn.execute(sql)

    async def close(self) -> None:
        await self._pool.close()
