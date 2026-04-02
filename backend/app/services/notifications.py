"""Notification service — multi-channel notifications with HMAC, DND, and digest."""

from __future__ import annotations

import hashlib
import hmac as hmac_lib
import ipaddress
import json
import logging
from datetime import datetime
from urllib.parse import urlparse

import httpx

from app.db.database import get_db
from app.models.schemas import NotificationConfig, WebhookConfig

logger = logging.getLogger(__name__)

SETTINGS_KEY = "notification_config"
MAX_RETRIES = 3


# ── URL Validation ──────────────────────────────────────────────────────────

def validate_webhook_url(url: str) -> str | None:
    """Validate that URL is safe (not targeting private networks)."""
    try:
        parsed = urlparse(url)
    except Exception:
        return "Invalid URL format."
    if parsed.scheme not in ("http", "https"):
        return "URL must use http or https."
    hostname = parsed.hostname or ""
    if not hostname:
        return "URL must have a hostname."
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            return "URL must not target private or loopback addresses."
    except ValueError:
        if hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return "URL must not target localhost."
    return None


# ── Config CRUD ─────────────────────────────────────────────────────────────

async def load_config() -> NotificationConfig:
    db = await get_db()
    row = await db.fetch_one("SELECT value FROM settings WHERE key = ?", (SETTINGS_KEY,))
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


# ── DND (Do Not Disturb) ───────────────────────────────────────────────────

def _is_in_dnd(config: NotificationConfig) -> bool:
    """Check if current time falls within DND hours."""
    if not config.dnd_start or not config.dnd_end:
        return False
    try:
        now = datetime.now().strftime("%H:%M")
        start, end = config.dnd_start, config.dnd_end
        if start <= end:
            return start <= now <= end
        else:  # Wraps midnight (e.g., 22:00–08:00)
            return now >= start or now <= end
    except Exception:
        return False


# ── Message Formatting ──────────────────────────────────────────────────────

STATUS_EMOJI = {"safe": "✅", "attention": "⚠️", "risk": "🚨"}


def _format_slack_blocks(payload: dict) -> dict:
    """Format payload as Slack Block Kit message."""
    event_type = payload.get("type", "notification")
    message = payload.get("message", "")
    emoji = STATUS_EMOJI.get(payload.get("new_status", ""), "ℹ️")

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{emoji} ClawSafe Alert", "emoji": True},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message},
        },
    ]

    if "old_status" in payload and "new_status" in payload:
        blocks.append({
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Previous:*\n{payload['old_status']}"},
                {"type": "mrkdwn", "text": f"*Current:*\n{payload['new_status']}"},
            ],
        })

    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": f"_ClawSafe • {event_type}_"}],
    })

    return {"blocks": blocks, "text": message}


def _format_teams_card(payload: dict) -> dict:
    """Format payload as Microsoft Teams Adaptive Card."""
    message = payload.get("message", "")
    emoji = STATUS_EMOJI.get(payload.get("new_status", ""), "ℹ️")

    return {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "E53935" if payload.get("new_status") == "risk" else "26A69A",
        "summary": f"ClawSafe: {message}",
        "sections": [{
            "activityTitle": f"{emoji} ClawSafe Alert",
            "facts": [
                {"name": "Status", "value": payload.get("new_status", "unknown")},
                {"name": "Previous", "value": payload.get("old_status", "unknown")},
            ],
            "text": message,
        }],
    }


def _format_payload(webhook: WebhookConfig, payload: dict) -> dict:
    """Format payload based on webhook format setting."""
    if webhook.format == "slack":
        return _format_slack_blocks(payload)
    elif webhook.format == "teams":
        return _format_teams_card(payload)
    return payload  # Default JSON


# ── HMAC Signing ────────────────────────────────────────────────────────────

def _sign_payload(payload: dict, secret: str) -> str:
    """Generate HMAC-SHA256 signature for webhook payload."""
    body = json.dumps(payload, sort_keys=True).encode()
    return hmac_lib.new(secret.encode(), body, hashlib.sha256).hexdigest()


# ── Webhook Sending ─────────────────────────────────────────────────────────

async def send_webhook(
    url: str,
    payload: dict,
    retries: int = MAX_RETRIES,
    hmac_secret: str = "",
    webhook_format: str = "json",
) -> bool:
    """Send webhook with optional HMAC signature."""
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if hmac_secret:
        sig = _sign_payload(payload, hmac_secret)
        headers["X-ClawSafe-Signature"] = f"sha256={sig}"

    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload, headers=headers)
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


# ── Escalation Handler ──────────────────────────────────────────────────────

async def notify_escalation(old_status: str, new_status: str) -> None:
    config = await load_config()
    if "escalation" not in config.events:
        return

    # Check DND hours
    if _is_in_dnd(config):
        logger.info("Notification suppressed (DND hours): %s → %s", old_status, new_status)
        return

    payload = {
        "source": "clawsafe",
        "type": "escalation",
        "message": f"Safety status changed from {old_status} to {new_status}.",
        "old_status": old_status,
        "new_status": new_status,
        "timestamp": datetime.utcnow().isoformat(),
    }

    for webhook in config.webhooks:
        if "escalation" in webhook.events:
            formatted = _format_payload(webhook, payload)
            await send_webhook(
                webhook.url,
                formatted,
                hmac_secret=webhook.hmac_secret,
                webhook_format=webhook.format,
            )

    # Send email notification if configured
    if config.email_enabled and config.email_address:
        from app.services.email import send_escalation_email
        await send_escalation_email(config.email_address, old_status, new_status)

    # Route to native integrations (PagerDuty, Jira, GitHub)
    try:
        from app.services.integrations import notify_integrations
        severity = "critical" if new_status == "risk" else "warning"
        await notify_integrations("escalation", payload["message"], severity)
    except Exception as e:
        logger.warning("Integration notification failed: %s", e)
