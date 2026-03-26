import pytest


@pytest.mark.anyio
async def test_overall_status(client):
    resp = await client.get("/api/v1/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("safe", "attention", "risk")
    assert "categories" in data
    assert len(data["categories"]) == 4


@pytest.mark.anyio
async def test_category_status(client):
    resp = await client.get("/api/v1/status/network")
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "network"
    assert data["status"] in ("safe", "attention", "risk")


@pytest.mark.anyio
async def test_invalid_category(client):
    resp = await client.get("/api/v1/status/invalid")
    assert resp.status_code == 422
