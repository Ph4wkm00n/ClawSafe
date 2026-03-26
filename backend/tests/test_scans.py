import pytest


@pytest.mark.anyio
async def test_scans_list(client):
    resp = await client.get("/api/v1/scans")
    assert resp.status_code == 200
    data = resp.json()
    assert "scans" in data
    assert "total" in data
    assert isinstance(data["scans"], list)
