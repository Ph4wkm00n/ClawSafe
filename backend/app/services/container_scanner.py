"""Container scanner — lists running containers and optionally scans for CVEs."""

from __future__ import annotations

import json
import logging
import subprocess

from app.core.config import settings

logger = logging.getLogger(__name__)


def list_containers() -> list[dict]:
    """List running Docker containers via CLI."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            logger.warning("docker ps failed: %s", result.stderr.strip())
            return []
        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    data = json.loads(line)
                    containers.append({
                        "id": data.get("ID", ""),
                        "name": data.get("Names", ""),
                        "image": data.get("Image", ""),
                        "status": data.get("Status", ""),
                        "state": data.get("State", ""),
                    })
                except json.JSONDecodeError:
                    continue
        return containers
    except FileNotFoundError:
        logger.info("Docker CLI not available")
        return []
    except subprocess.TimeoutExpired:
        logger.warning("docker ps timed out")
        return []
    except Exception as e:
        logger.error("Container listing failed: %s", e)
        return []


def scan_image_trivy(image: str) -> list[dict]:
    """Scan a container image for CVEs using Trivy CLI."""
    if not settings.trivy_enabled:
        return []
    try:
        result = subprocess.run(
            ["trivy", "image", "--format", "json", "--severity", "CRITICAL,HIGH", image],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            logger.warning("Trivy scan failed for %s: %s", image, result.stderr[:200])
            return []
        data = json.loads(result.stdout)
        vulns = []
        for r in data.get("Results", []):
            for v in r.get("Vulnerabilities", []):
                vulns.append({
                    "id": v.get("VulnerabilityID", ""),
                    "severity": v.get("Severity", "UNKNOWN").lower(),
                    "title": v.get("Title", ""),
                    "package": v.get("PkgName", ""),
                    "installed_version": v.get("InstalledVersion", ""),
                    "fixed_version": v.get("FixedVersion", ""),
                })
        return vulns
    except FileNotFoundError:
        logger.info("Trivy CLI not available")
        return []
    except subprocess.TimeoutExpired:
        logger.warning("Trivy scan timed out for %s", image)
        return []
    except Exception as e:
        logger.error("Trivy scan failed for %s: %s", image, e)
        return []


def get_container_findings() -> dict:
    """Get container listing and CVE scan results."""
    containers = list_containers()
    total_vulns = 0
    critical_count = 0

    for container in containers:
        vulns = scan_image_trivy(container["image"])
        container["vulnerabilities"] = vulns
        total_vulns += len(vulns)
        critical_count += sum(1 for v in vulns if v["severity"] == "critical")

    return {
        "containers": containers,
        "total_containers": len(containers),
        "total_vulnerabilities": total_vulns,
        "critical_vulnerabilities": critical_count,
    }
