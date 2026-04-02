import pytest

from app.models.schemas import InstancePermissionCreate
from app.services.permissions import (
    get_user_permissions,
    grant_permission,
    revoke_permission,
)


@pytest.mark.anyio
async def test_grant_and_list_permissions(client):
    # First create a user
    await client.post("/api/v1/auth/register", json={
        "email": "perm_user@test.com", "password": "TestPass123!", "name": "Perm User",
    })
    perm = await grant_permission(InstancePermissionCreate(
        user_id=1, instance_id="default", role="officer",
    ))
    assert perm.role == "officer"

    perms = await get_user_permissions(1)
    assert len(perms) >= 1


@pytest.mark.anyio
async def test_revoke_permission(client):
    await grant_permission(InstancePermissionCreate(
        user_id=1, instance_id="test-inst", role="viewer",
    ))
    result = await revoke_permission(1, "test-inst")
    assert result is True

    result = await revoke_permission(1, "nonexistent")
    assert result is False
