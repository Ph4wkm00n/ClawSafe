"""Notification service — sends webhooks and manages notification config."""

from __future__ import annotations

import logging

import httpx

from app.db.database import get_db
from app.models.schemas import NotificationConfig

logger = logging.getLogger(__name__)

SETTINGS_KEY = "notification_config"


async def load_config() -> NotificationConfig:
    db = await get_db()
    cursor = await db.execute(
        "SELECT value FROM settings WHERE key = ?", (SETTINGS_KEY,)
    )
    row = await cursor.fetchone()
    if row is None:
        return NotificationConfig()
    return NotificationConfig.model_validate_json(row[0])


async def save_config(config: NotificationConfig) -> None:
    db = await get_db()
    await db.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (SETTINGS_KEY, config.model_dump_json()),
    )
    await db.commit()


async def send_webhook(url: str, payload: dict) -> bool:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload)
            return resp.status_code < 400
    except Exception as e:
        logger.error("Webhook failed (%s): %s", url, e)
        return False


async def send_test_notification(url: str) -> bool:
    payload = {
        "source": "clawsafe",
        "type": "test",
        "message": "This is a test notification from ClawSafe.",
    }
    return await send_webhook(url, payload)


async def notify_escalation(old_status: str, new_status: str) -> None:
    config = await load_config()
    if "escalation" not in config.events:
        return

    payload = {
        "source": "clawsafe",
        "type": "escalation",
        "message": f"Safety status changed from {old_status} to {new_status}.",
        "old_status": old_status,
        "new_status": new_status,
    }

    for webhook in config.webhooks:
        if "escalation" in webhook.events:
            await send_webhook(webhook.url, payload)
