import pytest


@pytest.mark.anyio
async def test_recommendations_returns_list(client):
    resp = await client.get("/api/v1/recommendations")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Demo findings should produce at least one recommendation
    assert len(data) > 0
    for rec in data:
        assert "id" in rec
        assert "title" in rec
        assert "steps" in rec
