import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.anyio
async def test_bulk_fix_endpoint(client):
    with patch("app.services.fixer.create_backup", new_callable=AsyncMock, return_value=1):
        resp = await client.post("/api/v1/instances/bulk-fix", json={"action_id": "fix_network_binding"})
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "succeeded" in data
    assert "failed" in data
    assert "results" in data
