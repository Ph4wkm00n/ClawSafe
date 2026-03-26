"""Tests for container/CVE scanning."""

import pytest
from unittest.mock import patch


@pytest.mark.anyio
async def test_vulnerabilities_endpoint(client):
    resp = await client.get("/api/v1/vulnerabilities")
    assert resp.status_code == 200
    data = resp.json()
    assert "containers" in data
    assert "total_containers" in data
    assert "total_vulnerabilities" in data


@pytest.mark.anyio
async def test_containers_endpoint(client):
    resp = await client.get("/api/v1/containers")
    assert resp.status_code == 200
    data = resp.json()
    assert "containers" in data


def test_list_containers_no_docker():
    """When Docker is not available, returns empty list."""
    from app.services.container_scanner import list_containers

    with patch("app.services.container_scanner.subprocess.run", side_effect=FileNotFoundError):
        result = list_containers()
        assert result == []


def test_scan_image_trivy_disabled():
    """When Trivy is disabled, returns empty list."""
    from app.services.container_scanner import scan_image_trivy

    result = scan_image_trivy("test:latest")
    assert result == []
