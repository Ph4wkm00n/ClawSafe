import pytest


@pytest.mark.anyio
async def test_metrics_endpoint(client):
    resp = await client.get("/metrics")
    assert resp.status_code == 200
    text = resp.text
    assert "clawsafe_" in text or "HELP" in text or "TYPE" in text
