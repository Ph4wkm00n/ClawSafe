import pytest


@pytest.mark.anyio
async def test_capture_evidence(client):
    resp = await client.post("/api/v1/security/evidence/capture?control_id=CIS-1.1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["compliance_control"] == "CIS-1.1"
    assert "snapshot_json" in data


@pytest.mark.anyio
async def test_list_evidence(client):
    # Capture one first
    await client.post("/api/v1/security/evidence/capture?control_id=CIS-2.1")
    resp = await client.get("/api/v1/security/evidence")
    assert resp.status_code == 200
    data = resp.json()
    assert "evidence" in data
    assert len(data["evidence"]) >= 1


@pytest.mark.anyio
async def test_list_evidence_by_control(client):
    await client.post("/api/v1/security/evidence/capture?control_id=CIS-3.1")
    resp = await client.get("/api/v1/security/evidence?control_id=CIS-3.1")
    assert resp.status_code == 200
    data = resp.json()
    for e in data["evidence"]:
        assert e["compliance_control"] == "CIS-3.1"
