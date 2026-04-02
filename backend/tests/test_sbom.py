import pytest

from app.services.sbom import generate_sbom, generate_sbom_json


def test_generate_sbom():
    sbom = generate_sbom()
    assert sbom.format == "CycloneDX"
    assert len(sbom.components) > 0
    assert sbom.generated_at


def test_generate_sbom_json():
    data = generate_sbom_json()
    assert data["bomFormat"] == "CycloneDX"
    assert "components" in data
    assert len(data["components"]) > 0


@pytest.mark.anyio
async def test_sbom_endpoint(client):
    resp = await client.get("/api/v1/security/sbom")
    assert resp.status_code == 200
    data = resp.json()
    assert data["format"] == "CycloneDX"
    assert len(data["components"]) > 0
