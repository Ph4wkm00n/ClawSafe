"""Notification service — sends webhooks and manages notification config."""

from __future__ import annotations

import ipaddress
import logging
from urllib.parse import urlparse

import httpx

from app.db.database import get_db
from app.models.schemas import NotificationConfig

logger = logging.getLogger(__name__)

SETTINGS_KEY = "notification_config"
MAX_RETRIES = 3


def validate_webhook_url(url: str) -> str | None:
    """Validate that URL is safe (not targeting private networks). Returns error or None."""
    try:
        parsed = urlparse(url)
    except Exception:
        return "Invalid URL format."

    if parsed.scheme not in ("http", "https"):
        return "URL must use http or https."

    hostname = parsed.hostname or ""
    if not hostname:
        return "URL must have a hostname."

    # Block obviously private addresses
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            return "URL must not target private or loopback addresses."
    except ValueError:
        # Hostname is not an IP — check for common private hostnames
        if hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return "URL must not target localhost."

    return None


async def load_config() -> NotificationConfig:
    db = await get_db()
    row = await db.fetch_one(
        "SELECT value FROM settings WHERE key = ?", (SETTINGS_KEY,)
    )
    if row is None:
        return NotificationConfig()
    return NotificationConfig.model_validate_json(row["value"])


async def save_config(config: NotificationConfig) -> None:
    db = await get_db()
    await db.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (SETTINGS_KEY, config.model_dump_json()),
    )
    await db.commit()


async def send_webhook(url: str, payload: dict, retries: int = MAX_RETRIES) -> bool:
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code < 400:
                    return True
                logger.warning("Webhook %s returned %d (attempt %d)", url, resp.status_code, attempt + 1)
        except Exception as e:
            logger.warning("Webhook failed (%s, attempt %d): %s", url, attempt + 1, e)
    logger.error("Webhook %s failed after %d attempts", url, retries)
    return False


async def send_test_notification(url: str) -> bool:
    payload = {
        "source": "clawsafe",
        "type": "test",
        "message": "This is a test notification from ClawSafe.",
    }
    return await send_webhook(url, payload, retries=1)


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

    # Send email notification if configured
    if config.email_enabled and config.email_address:
        from app.services.email import send_escalation_email

        await send_escalation_email(config.email_address, old_status, new_status)
