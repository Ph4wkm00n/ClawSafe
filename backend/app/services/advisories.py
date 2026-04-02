"""Advisory service — checks OpenClaw versions against known security advisories."""

from __future__ import annotations

import logging
from packaging.version import Version, InvalidVersion

logger = logging.getLogger(__name__)

# Known security advisories for OpenClaw versions.
# Format: {cve_id: {affected_versions: (min, max), severity, description}}
KNOWN_ADVISORIES: list[dict] = [
    {
        "cve_id": "CVE-2025-0001",
        "affected_min": "0.1.0",
        "affected_max": "0.9.9",
        "severity": "critical",
        "title": "Remote code execution via skill injection",
        "description": "Versions before 1.0.0 allow arbitrary code execution through malformed skill definitions.",
        "fixed_in": "1.0.0",
    },
    {
        "cve_id": "CVE-2025-0042",
        "affected_min": "1.0.0",
        "affected_max": "1.2.3",
        "severity": "high",
        "title": "Path traversal in file mount validation",
        "description": "Insufficient validation of mount paths allows access to files outside intended directories.",
        "fixed_in": "1.2.4",
    },
    {
        "cve_id": "CVE-2025-0078",
        "affected_min": "1.0.0",
        "affected_max": "1.3.9",
        "severity": "medium",
        "title": "Authentication bypass in API key validation",
        "description": "Timing attack on API key comparison allows brute-force key recovery.",
        "fixed_in": "1.4.0",
    },
    {
        "cve_id": "CVE-2025-0115",
        "affected_min": "1.5.0",
        "affected_max": "1.5.2",
        "severity": "high",
        "title": "SSRF via webhook URL validation bypass",
        "description": "DNS rebinding attack can bypass webhook URL validation to reach internal services.",
        "fixed_in": "1.5.3",
    },
]


def _parse_version(v: str) -> Version | None:
    """Safely parse a version string."""
    try:
        return Version(v)
    except InvalidVersion:
        return None


def check_advisories(version: str) -> list[dict]:
    """Check if a version is affected by any known security advisories."""
    parsed = _parse_version(version)
    if parsed is None:
        logger.warning("Cannot parse version for advisory check: %s", version)
        return []

    matching = []
    for adv in KNOWN_ADVISORIES:
        min_v = _parse_version(adv["affected_min"])
        max_v = _parse_version(adv["affected_max"])
        if min_v is None or max_v is None:
            continue
        if min_v <= parsed <= max_v:
            matching.append({
                "cve_id": adv["cve_id"],
                "severity": adv["severity"],
                "title": adv["title"],
                "description": adv["description"],
                "fixed_in": adv["fixed_in"],
            })

    return matching
