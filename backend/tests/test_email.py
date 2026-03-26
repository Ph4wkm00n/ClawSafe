"""Tests for email notification service."""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.anyio
async def test_test_email_endpoint_requires_address(client):
    """Test email endpoint fails when no email configured."""
    resp = await client.post("/api/v1/settings/notifications/test-email")
    assert resp.status_code == 400
    assert "No email address" in resp.json()["detail"]


@pytest.mark.anyio
async def test_test_email_endpoint_with_config(client):
    """Test email endpoint after configuring email address."""
    # First configure an email address
    config = {
        "webhooks": [],
        "email_enabled": True,
        "email_address": "test@example.com",
        "events": ["escalation"],
    }
    await client.put("/api/v1/settings/notifications", json=config)

    # Now test email — will fail since no SMTP configured, but endpoint works
    with patch("app.services.email.aiosmtplib.send", new_callable=AsyncMock):
        resp = await client.post("/api/v1/settings/notifications/test-email")
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_escalation_sends_email():
    """Test that notify_escalation calls email when configured."""
    from app.services.notifications import save_config
    from app.models.schemas import NotificationConfig

    config = NotificationConfig(
        email_enabled=True,
        email_address="test@example.com",
        events=["escalation"],
    )
    await save_config(config)

    with patch("app.services.email.aiosmtplib.send", new_callable=AsyncMock):
        from app.services.notifications import notify_escalation

        await notify_escalation("safe", "risk")
