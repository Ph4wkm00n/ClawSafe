import pytest


@pytest.mark.anyio
async def test_comparison_endpoint(client):
    resp = await client.get("/api/v1/comparison")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "match_percentage" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
    # Each item should have required fields
    for item in data["items"]:
        assert "field" in item
        assert "current_value" in item
        assert "recommended_value" in item
        assert item["status"] in ("match", "mismatch", "missing")
