"""Tests for data management — retention, export."""

import pytest


@pytest.mark.anyio
async def test_export_scans_json(client):
    resp = await client.get("/api/v1/data/export/scans?format=json")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")


@pytest.mark.anyio
async def test_export_scans_csv(client):
    resp = await client.get("/api/v1/data/export/scans?format=csv")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]


@pytest.mark.anyio
async def test_export_activity_json(client):
    resp = await client.get("/api/v1/data/export/activity?format=json")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_purge_data(client):
    resp = await client.post("/api/v1/data/purge?retention_days=365")
    assert resp.status_code == 200
    data = resp.json()
    assert "retention_days" in data
    assert data["retention_days"] == 365
