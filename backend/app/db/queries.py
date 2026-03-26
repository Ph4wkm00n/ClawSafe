"""Database abstraction — normalizes access patterns across SQLite and PostgreSQL."""

from __future__ import annotations

from typing import Any


class Database:
    """Unified database interface. Results returned as dicts for portable access."""

    async def execute(self, sql: str, params: tuple = ()) -> Any:
        raise NotImplementedError

    async def fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        raise NotImplementedError

    async def fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        raise NotImplementedError

    async def fetch_scalar(self, sql: str, params: tuple = ()) -> Any:
        """Fetch the first column of the first row."""
        row = await self.fetch_one(sql, params)
        if row is None:
            return None
        return next(iter(row.values()))

    async def insert_returning_id(self, sql: str, params: tuple = ()) -> int:
        """Execute an INSERT and return the last inserted row ID."""
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def executescript(self, sql: str) -> None:
        """Execute multiple SQL statements (for migrations)."""
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def health_check(self) -> bool:
        try:
            result = await self.fetch_scalar("SELECT 1")
            return result == 1
        except Exception:
            return False


class SQLiteDatabase(Database):
    """SQLite implementation using aiosqlite."""

    def __init__(self, connection):
        self._conn = connection

    async def execute(self, sql: str, params: tuple = ()) -> Any:
        return await self._conn.execute(sql, params)

    async def fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        cursor = await self._conn.execute(sql, params)
        row = await cursor.fetchone()
        if row is None:
            return None
        # aiosqlite Row → dict
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    async def fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        cursor = await self._conn.execute(sql, params)
        rows = await cursor.fetchall()
        if not rows:
            return []
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    async def insert_returning_id(self, sql: str, params: tuple = ()) -> int:
        cursor = await self._conn.execute(sql, params)
        return cursor.lastrowid or 0

    async def commit(self) -> None:
        await self._conn.commit()

    async def executescript(self, sql: str) -> None:
        await self._conn.executescript(sql)
        await self._conn.commit()

    async def close(self) -> None:
        await self._conn.close()
