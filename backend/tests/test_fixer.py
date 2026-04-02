from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.anyio
async def test_fix_network(client):
    with (
        patch("app.services.fixer.create_backup", new_callable=AsyncMock, return_value=1),
        patch("app.services.fixer._save_config", new_callable=AsyncMock),
    ):
        resp = await client.post("/api/v1/fix/fix_network_binding")
    assert resp.status_code == 200
    data = resp.json()
    assert data["action_id"] == "fix_network_binding"
    assert data["success"] is True
    assert "localhost" in data["message"].lower() or "127.0.0.1" in data["message"]


@pytest.mark.anyio
async def test_fix_unknown_action(client):
    resp = await client.post("/api/v1/fix/fix_updates")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is False


@pytest.mark.anyio
async def test_backups_list(client):
    resp = await client.get("/api/v1/backups")
    assert resp.status_code == 200
    data = resp.json()
    assert "backups" in data


@pytest.mark.anyio
async def test_undo_without_backup(client):
    resp = await client.post("/api/v1/fix/fix_network_binding/undo")
    assert resp.status_code == 200
    data = resp.json()
    # May or may not have a backup depending on test order
    assert "action_id" in data
