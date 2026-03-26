"""Tests for API key authentication and input validation."""

import pytest

from app.core.auth import validate_action_id


def test_validate_action_id_accepts_valid():
    assert validate_action_id("fix_network_binding") == "fix_network_binding"
    assert validate_action_id("fix_auth") == "fix_auth"


def test_validate_action_id_rejects_invalid():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        validate_action_id("../etc/passwd")
    assert exc_info.value.status_code == 400

    with pytest.raises(HTTPException):
        validate_action_id("")

    with pytest.raises(HTTPException):
        validate_action_id("FIX_UPPER")

    with pytest.raises(HTTPException):
        validate_action_id("fix network")


@pytest.mark.anyio
async def test_read_endpoints_no_auth_needed(client):
    """Read endpoints should always work without auth."""
    for path in ["/api/v1/status", "/api/v1/health", "/api/v1/activity"]:
        resp = await client.get(path)
        assert resp.status_code == 200, f"GET {path} failed"


@pytest.mark.anyio
async def test_write_endpoints_work_without_key_in_dev(client):
    """When API key is empty (dev mode), write endpoints work without auth."""
    resp = await client.post("/api/v1/fix/fix_network_binding")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_invalid_action_id_at_api_level(client):
    """Action IDs with invalid characters should be rejected."""
    resp = await client.post("/api/v1/fix/UPPER_CASE")
    assert resp.status_code == 400
