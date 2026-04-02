import pytest

from app.models.schemas import PolicyConfig
from app.services.policy import merge_policies


def test_merge_policies_override():
    base = PolicyConfig(name="base", network={"bind_address": "0.0.0.0"}, tools={"rules": []})
    override = PolicyConfig(name="override", network={"bind_address": "127.0.0.1"})
    merged = merge_policies(base, override)
    assert merged.network["bind_address"] == "127.0.0.1"


def test_merge_policies_preserves_base():
    base = PolicyConfig(name="base", network={"bind_address": "0.0.0.0", "vpn_only": True})
    override = PolicyConfig(name="override", network={"bind_address": "127.0.0.1"})
    merged = merge_policies(base, override)
    assert merged.network["vpn_only"] is True
    assert merged.network["bind_address"] == "127.0.0.1"


@pytest.mark.anyio
async def test_policy_simulation(client):
    resp = await client.post("/api/v1/policy/simulate", json={
        "policy": {"tools": {"rules": [{"name": "*", "risk": "high", "action": "allow"}]}},
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "current_score" in data
    assert "simulated_score" in data


@pytest.mark.anyio
async def test_list_policy_templates(client):
    resp = await client.get("/api/v1/policy/templates")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    names = [t["name"] for t in data]
    assert "strict" in names
    assert "permissive" in names


@pytest.mark.anyio
async def test_effective_policy_without_override(client):
    # First create an active policy
    await client.put("/api/v1/policy", json={
        "version": "1", "name": "test", "network": {}, "tools": {}, "data": {}, "auth": {},
    })
    resp = await client.get("/api/v1/policy/effective/default")
    assert resp.status_code == 200
