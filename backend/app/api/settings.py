
from fastapi import APIRouter, Depends

from app.core.auth import require_auth

from app.db.database import get_db
from app.models.schemas import UserSettings

router = APIRouter()

SETTINGS_KEY = "user_settings"


async def _load_settings() -> UserSettings:
    db = await get_db()
    cursor = await db.execute(
        "SELECT value FROM settings WHERE key = ?", (SETTINGS_KEY,)
    )
    row = await cursor.fetchone()
    if row is None:
        return UserSettings()
    return UserSettings.model_validate_json(row[0])


async def _save_settings(s: UserSettings) -> None:
    db = await get_db()
    await db.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (SETTINGS_KEY, s.model_dump_json()),
    )
    await db.commit()


@router.get("/settings", response_model=UserSettings)
async def get_settings():
    return await _load_settings()


@router.put("/settings", response_model=UserSettings, dependencies=[Depends(require_auth)])
async def update_settings(payload: UserSettings):
    await _save_settings(payload)
    return payload
