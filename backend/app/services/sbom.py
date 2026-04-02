"""SBOM generation — Software Bill of Materials in CycloneDX format."""

from __future__ import annotations

import importlib.metadata
import logging
from datetime import datetime

from app.models.schemas import SbomEntry, SbomResponse

logger = logging.getLogger(__name__)


def generate_sbom() -> SbomResponse:
    """Generate a CycloneDX-style SBOM from installed packages."""
    components = []
    for dist in importlib.metadata.distributions():
        name = dist.metadata["Name"]
        version = dist.metadata["Version"]
        license_info = dist.metadata.get("License", "unknown") or "unknown"
        # Truncate long license strings
        if len(license_info) > 100:
            license_info = license_info[:97] + "..."

        components.append(SbomEntry(
            name=name,
            version=version,
            license=license_info,
            type="library",
        ))

    # Sort by name for consistent output
    components.sort(key=lambda c: c.name.lower())

    return SbomResponse(
        format="CycloneDX",
        spec_version="1.4",
        components=components,
        generated_at=datetime.utcnow().isoformat(),
    )


def generate_sbom_json() -> dict:
    """Generate CycloneDX JSON format SBOM."""
    sbom = generate_sbom()
    return {
        "bomFormat": "CycloneDX",
        "specVersion": sbom.spec_version,
        "version": 1,
        "metadata": {
            "timestamp": sbom.generated_at,
            "tools": [{"vendor": "ClawSafe", "name": "sbom-generator", "version": "1.0.0"}],
        },
        "components": [
            {
                "type": comp.type,
                "name": comp.name,
                "version": comp.version,
                "licenses": [{"license": {"name": comp.license}}] if comp.license != "unknown" else [],
            }
            for comp in sbom.components
        ],
    }
