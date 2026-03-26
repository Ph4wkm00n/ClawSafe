import pytest


@pytest.mark.anyio
async def test_activity_returns_list(client):
    resp = await client.get("/api/v1/activity")
    assert resp.status_code == 200
    data = resp.json()
    assert "events" in data
    assert "total" in data
    assert isinstance(data["events"], list)


@pytest.mark.anyio
async def test_activity_pagination(client):
    resp = await client.get("/api/v1/activity?limit=2&offset=0")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["events"]) <= 2
