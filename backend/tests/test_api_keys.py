import pytest


@pytest.mark.anyio
async def test_create_api_key(client):
    resp = await client.post("/api/v1/api-keys", json={"name": "test-key"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "test-key"
    assert "key" in data  # Raw key only returned on creation
    assert data["key"].startswith("cs_")


@pytest.mark.anyio
async def test_list_api_keys(client):
    # Create a key first
    await client.post("/api/v1/api-keys", json={"name": "list-test-key"})
    resp = await client.get("/api/v1/api-keys")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.anyio
async def test_revoke_api_key(client):
    create_resp = await client.post("/api/v1/api-keys", json={"name": "revoke-test"})
    key_id = create_resp.json()["id"]
    resp = await client.delete(f"/api/v1/api-keys/{key_id}")
    assert resp.status_code == 200
    assert resp.json()["revoked"] is True


@pytest.mark.anyio
async def test_revoke_nonexistent_key(client):
    resp = await client.delete("/api/v1/api-keys/99999")
    assert resp.status_code == 404
