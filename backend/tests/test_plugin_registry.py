import pytest

from app.services.plugin_registry import BUNDLED_REGISTRY, fetch_registry, search_plugins


@pytest.mark.anyio
async def test_fetch_registry_returns_bundled():
    registry = await fetch_registry()
    assert len(registry) >= 5
    assert any(p["name"] == "trivy-scanner" for p in registry)


def test_search_plugins_by_name():
    results = search_plugins(BUNDLED_REGISTRY, "trivy")
    assert len(results) == 1
    assert results[0]["name"] == "trivy-scanner"


def test_search_plugins_by_description():
    results = search_plugins(BUNDLED_REGISTRY, "vulnerability")
    assert len(results) >= 1


def test_search_plugins_no_match():
    results = search_plugins(BUNDLED_REGISTRY, "nonexistent-xyz")
    assert results == []


@pytest.mark.anyio
async def test_registry_endpoint(client):
    resp = await client.get("/api/v1/plugins/registry")
    assert resp.status_code == 200
    data = resp.json()
    assert "plugins" in data
    assert data["total"] >= 5
