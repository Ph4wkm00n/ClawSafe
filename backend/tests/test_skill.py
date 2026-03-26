import pytest


@pytest.mark.anyio
async def test_skill_status(client):
    resp = await client.get("/api/v1/skill/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data
    assert "status" in data
    assert "score" in data
    assert "top_actions" in data
    assert isinstance(data["top_actions"], list)


@pytest.mark.anyio
async def test_skill_actions(client):
    resp = await client.get("/api/v1/skill/actions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
