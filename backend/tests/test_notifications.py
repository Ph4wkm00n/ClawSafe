import pytest


@pytest.mark.anyio
async def test_get_notifications(client):
    resp = await client.get("/api/v1/settings/notifications")
    assert resp.status_code == 200
    data = resp.json()
    assert "webhooks" in data
    assert "events" in data


@pytest.mark.anyio
async def test_update_notifications(client):
    config = {
        "webhooks": [{"url": "https://example.com/hook", "name": "test", "events": ["escalation"]}],
        "email_enabled": False,
        "email_address": "",
        "events": ["escalation"],
    }
    resp = await client.put("/api/v1/settings/notifications", json=config)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["webhooks"]) == 1
    assert data["webhooks"][0]["url"] == "https://example.com/hook"
