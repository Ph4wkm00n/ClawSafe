import pytest

from app.services.skill_audit import get_skill_executions, log_skill_execution


@pytest.mark.anyio
async def test_log_and_query_skill_execution(client):
    exec_id = await log_skill_execution(
        skill_name="file_read",
        instance_id="default",
        parameters={"path": "/tmp/test"},
        result={"success": True},
        duration_ms=42,
    )
    assert exec_id > 0

    executions = await get_skill_executions(instance_id="default")
    assert len(executions) >= 1
    assert executions[0].skill_name == "file_read"
    assert executions[0].duration_ms == 42


@pytest.mark.anyio
async def test_skill_audit_endpoint(client):
    resp = await client.get("/api/v1/security/skill-audit")
    assert resp.status_code == 200
    data = resp.json()
    assert "executions" in data
    assert "total" in data
