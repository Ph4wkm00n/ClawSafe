import pytest


@pytest.mark.anyio
async def test_validate_valid_policy(client):
    policy = {
        "version": "1",
        "name": "test",
        "network": {"bind_address": "127.0.0.1"},
        "tools": {"rules": [{"name": "shell_exec", "action": "block"}]},
        "data": {"allowed_mounts": ["/app"]},
        "auth": {"enabled": True},
    }
    resp = await client.post("/api/v1/policy/validate", json=policy)
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert data["errors"] == []


@pytest.mark.anyio
async def test_validate_policy_with_bad_rules(client):
    policy = {
        "version": "1",
        "name": "bad",
        "network": {"bind_address": "127.0.0.1"},
        "tools": {"rules": [{"action": "invalid_action"}]},
        "data": {},
        "auth": {},
    }
    resp = await client.post("/api/v1/policy/validate", json=policy)
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is False
    assert len(data["errors"]) > 0


@pytest.mark.anyio
async def test_update_and_get_policy(client):
    policy = {
        "version": "1",
        "name": "test-policy",
        "network": {"bind_address": "127.0.0.1"},
        "tools": {"default_action": "ask", "rules": []},
        "data": {"allowed_mounts": ["/app"]},
        "auth": {"enabled": True},
    }
    resp = await client.put("/api/v1/policy", json=policy)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "test-policy"
    assert data["active"] is True

    resp2 = await client.get("/api/v1/policy")
    assert resp2.status_code == 200
    assert resp2.json()["name"] == "test-policy"
