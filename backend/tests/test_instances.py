"""Tests for multi-instance support."""

import pytest


@pytest.mark.anyio
async def test_list_instances(client):
    resp = await client.get("/api/v1/instances")
    assert resp.status_code == 200
    data = resp.json()
    assert "instances" in data
    assert "total" in data
    # Default instance should exist from migration
    assert data["total"] >= 1


@pytest.mark.anyio
async def test_create_instance(client):
    resp = await client.post(
        "/api/v1/instances",
        json={"name": "Test Instance", "config_path": "/tmp/test.yaml"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Instance"
    assert data["active"] is True


@pytest.mark.anyio
async def test_get_instance(client):
    # Create first
    resp = await client.post(
        "/api/v1/instances",
        json={"name": "Get Test", "config_path": "/tmp/get.yaml"},
    )
    instance_id = resp.json()["id"]

    # Get
    resp = await client.get(f"/api/v1/instances/{instance_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Get Test"


@pytest.mark.anyio
async def test_delete_default_instance_fails(client):
    resp = await client.delete("/api/v1/instances/default")
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_instance_not_found(client):
    resp = await client.get("/api/v1/instances/nonexistent")
    assert resp.status_code == 404
