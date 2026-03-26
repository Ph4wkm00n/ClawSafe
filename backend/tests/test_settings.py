import pytest


@pytest.mark.anyio
async def test_get_default_settings(client):
    resp = await client.get("/api/v1/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["onboarding_complete"] is False
    assert data["theme"] == "playful"


@pytest.mark.anyio
async def test_update_settings(client):
    payload = {
        "onboarding_complete": True,
        "theme": "minimal",
        "mode": "dark",
        "usage_type": "home",
        "network_preference": "private",
    }
    resp = await client.put("/api/v1/settings", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["onboarding_complete"] is True
    assert data["theme"] == "minimal"
