"""Email service — sends notifications via SMTP."""

from __future__ import annotations

import logging
from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    recipient: str,
    subject: str,
    body: str,
    retries: int = 2,
) -> bool:
    """Send an email via SMTP. Returns True on success."""
    if not settings.smtp_host:
        logger.warning("Email not sent: SMTP not configured (CLAWSAFE_SMTP_HOST is empty)")
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from or settings.smtp_user
    msg["To"] = recipient
    msg.set_content(body)

    for attempt in range(retries):
        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_user or None,
                password=settings.smtp_password or None,
                start_tls=settings.smtp_port == 587,
                use_tls=settings.smtp_port == 465,
            )
            logger.info("Email sent to %s: %s", recipient, subject)
            return True
        except Exception as e:
            logger.warning("Email failed (attempt %d): %s", attempt + 1, e)

    logger.error("Email to %s failed after %d attempts", recipient, retries)
    return False


async def send_escalation_email(
    recipient: str,
    old_status: str,
    new_status: str,
) -> bool:
    """Send a risk escalation alert email."""
    subject = f"[ClawSafe] Safety status changed: {old_status} → {new_status}"
    body = (
        f"ClawSafe has detected a change in your safety status.\n\n"
        f"Previous status: {old_status}\n"
        f"Current status:  {new_status}\n\n"
        f"Please review your ClawSafe dashboard for details and recommended actions.\n\n"
        f"— ClawSafe Security Monitor"
    )
    return await send_email(recipient, subject, body)


async def send_test_email(recipient: str) -> bool:
    """Send a test email to verify SMTP configuration."""
    subject = "[ClawSafe] Test notification"
    body = (
        "This is a test email from ClawSafe.\n\n"
        "If you received this, your email notifications are configured correctly.\n\n"
        "— ClawSafe Security Monitor"
    )
    return await send_email(recipient, subject, body)
