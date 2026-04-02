import pytest

from app.services.instance_manager import get_instance_timeline, record_instance_score


@pytest.mark.anyio
async def test_record_and_get_timeline(client):
    await record_instance_score("default", 45, "attention")
    await record_instance_score("default", 30, "attention")
    await record_instance_score("default", 15, "safe")

    timeline = await get_instance_timeline("default", days=30)
    assert len(timeline) == 3
    assert timeline[0].score == 45
    assert timeline[2].score == 15


@pytest.mark.anyio
async def test_timeline_endpoint(client):
    resp = await client.get("/api/v1/instances/default/timeline")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
