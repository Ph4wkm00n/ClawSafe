"""Dependency vulnerability scanner — checks installed packages against known CVEs."""

from __future__ import annotations

import importlib.metadata
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Bundled advisory database (subset for common packages)
ADVISORY_DB: list[dict] = [
    {
        "package": "requests",
        "cve_id": "CVE-2024-35195",
        "affected_max": "2.31.0",
        "severity": "medium",
        "title": "Proxy-Authorization header leak on HTTP redirects",
        "fixed_in": "2.32.0",
    },
    {
        "package": "urllib3",
        "cve_id": "CVE-2024-37891",
        "affected_max": "2.2.1",
        "severity": "medium",
        "title": "Proxy-Authorization header not stripped on cross-origin redirect",
        "fixed_in": "2.2.2",
    },
    {
        "package": "cryptography",
        "cve_id": "CVE-2024-26130",
        "affected_max": "42.0.3",
        "severity": "high",
        "title": "NULL pointer dereference in PKCS12 parsing",
        "fixed_in": "42.0.4",
    },
    {
        "package": "jinja2",
        "cve_id": "CVE-2024-34064",
        "affected_max": "3.1.3",
        "severity": "medium",
        "title": "HTML attribute injection in xmlattr filter",
        "fixed_in": "3.1.4",
    },
    {
        "package": "pyyaml",
        "cve_id": "CVE-2020-14343",
        "affected_max": "5.4",
        "severity": "critical",
        "title": "Arbitrary code execution via FullLoader",
        "fixed_in": "5.4.1",
    },
]


def _parse_version_tuple(v: str) -> tuple:
    """Parse version string into comparable tuple."""
    parts = []
    for p in v.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def get_installed_packages() -> list[dict]:
    """Get all installed Python packages with versions."""
    packages = []
    for dist in importlib.metadata.distributions():
        packages.append({
            "name": dist.metadata["Name"].lower(),
            "version": dist.metadata["Version"],
        })
    return sorted(packages, key=lambda p: p["name"])


def scan_dependencies() -> list[dict]:
    """Scan installed packages against the advisory database."""
    installed = {p["name"]: p["version"] for p in get_installed_packages()}
    vulnerabilities = []

    for adv in ADVISORY_DB:
        pkg_name = adv["package"]
        if pkg_name not in installed:
            continue
        installed_ver = _parse_version_tuple(installed[pkg_name])
        affected_max = _parse_version_tuple(adv["affected_max"])

        if installed_ver <= affected_max:
            vulnerabilities.append({
                "package": pkg_name,
                "installed_version": installed[pkg_name],
                "cve_id": adv["cve_id"],
                "severity": adv["severity"],
                "title": adv["title"],
                "fixed_in": adv["fixed_in"],
            })

    return vulnerabilities


def scan_requirements_file(path: str) -> list[dict]:
    """Scan a requirements.txt file against advisories."""
    p = Path(path)
    if not p.exists():
        return []

    packages: dict[str, str] = {}
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            packages[name.strip().lower()] = version.strip()

    vulnerabilities = []
    for adv in ADVISORY_DB:
        pkg_name = adv["package"]
        if pkg_name not in packages:
            continue
        installed_ver = _parse_version_tuple(packages[pkg_name])
        affected_max = _parse_version_tuple(adv["affected_max"])

        if installed_ver <= affected_max:
            vulnerabilities.append({
                "package": pkg_name,
                "installed_version": packages[pkg_name],
                "cve_id": adv["cve_id"],
                "severity": adv["severity"],
                "title": adv["title"],
                "fixed_in": adv["fixed_in"],
            })

    return vulnerabilities
