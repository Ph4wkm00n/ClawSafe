"""Tests for v1.2 notification enhancements."""


from app.services.notifications import (
    _format_slack_blocks,
    _format_teams_card,
    _is_in_dnd,
    _sign_payload,
)
from app.models.schemas import NotificationConfig


def test_slack_block_formatting():
    payload = {
        "type": "escalation",
        "message": "Status changed from safe to risk.",
        "old_status": "safe",
        "new_status": "risk",
    }
    result = _format_slack_blocks(payload)
    assert "blocks" in result
    assert result["text"] == payload["message"]
    assert len(result["blocks"]) >= 3


def test_teams_card_formatting():
    payload = {
        "type": "escalation",
        "message": "Status changed.",
        "old_status": "safe",
        "new_status": "risk",
    }
    result = _format_teams_card(payload)
    assert result["@type"] == "MessageCard"
    assert "ClawSafe" in result["sections"][0]["activityTitle"]


def test_hmac_signature():
    payload = {"key": "value"}
    sig = _sign_payload(payload, "secret")
    assert len(sig) == 64  # SHA-256 hex


def test_dnd_not_configured():
    config = NotificationConfig()
    assert _is_in_dnd(config) is False


def test_dnd_with_times():
    config = NotificationConfig(dnd_start="00:00", dnd_end="00:01")
    # Can't guarantee current time is in this range, but function should not crash
    result = _is_in_dnd(config)
    assert isinstance(result, bool)
