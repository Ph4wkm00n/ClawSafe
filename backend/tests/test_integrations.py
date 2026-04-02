import pytest


@pytest.mark.anyio
async def test_get_integrations(client):
    resp = await client.get("/api/v1/integrations")
    assert resp.status_code == 200
    data = resp.json()
    assert "enabled_integrations" in data
    assert isinstance(data["enabled_integrations"], list)


@pytest.mark.anyio
async def test_update_integrations(client):
    resp = await client.put("/api/v1/integrations", json={
        "pagerduty_routing_key": "test-key",
        "enabled_integrations": ["pagerduty"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["pagerduty_routing_key"] == "test-key"
    assert "pagerduty" in data["enabled_integrations"]


@pytest.mark.anyio
async def test_test_unconfigured_integration(client):
    # Reset config first
    await client.put("/api/v1/integrations", json={"enabled_integrations": []})
    resp = await client.post("/api/v1/integrations/test/jira")
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_test_unknown_integration(client):
    resp = await client.post("/api/v1/integrations/test/unknown_service")
    assert resp.status_code == 400
