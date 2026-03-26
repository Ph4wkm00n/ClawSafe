"""Scanner service — detects OpenClaw configuration and computes raw findings."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

import yaml

from app.core.config import settings

logger = logging.getLogger(__name__)


def _load_openclaw_config(config_path: str | None = None) -> dict | None:
    path = Path(config_path or settings.openclaw_config_path)
    if not path.exists():
        return None
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else None
    except Exception as e:
        logger.error("Failed to load OpenClaw config at %s: %s", path, e)
        return None


def _check_network(config: dict | None) -> dict:
    if config is None:
        return {
            "bind_address": "unknown",
            "is_localhost": False,
            "port": None,
            "exposed": True,
        }
    bind = config.get("bind_address", config.get("host", "0.0.0.0"))
    port = config.get("port", 8080)
    is_localhost = bind in ("127.0.0.1", "localhost", "::1")
    return {
        "bind_address": bind,
        "is_localhost": is_localhost,
        "port": port,
        "exposed": not is_localhost,
    }


def _check_tools(config: dict | None) -> dict:
    if config is None:
        return {"skills": [], "high_risk_enabled": True, "total": 0}
    skills = config.get("skills", config.get("tools", []))
    if not isinstance(skills, list):
        skills = []
    high_risk = [
        s for s in skills
        if isinstance(s, dict) and s.get("risk", "low") in ("high", "critical")
        and s.get("enabled", True)
    ]
    return {
        "skills": skills,
        "high_risk_enabled": len(high_risk) > 0,
        "high_risk_skills": [s.get("name", "unknown") for s in high_risk],
        "total": len(skills),
    }


def _check_data(config: dict | None) -> dict:
    if config is None:
        return {"mounts": [], "broad_access": False}
    mounts = config.get("mounts", config.get("volumes", []))
    if not isinstance(mounts, list):
        mounts = []
    sensitive = {"/", "/etc", "/root", "/home"}
    broad = any(
        isinstance(m, str) and (m in sensitive or m.rstrip("/") in sensitive)
        for m in mounts
    )
    return {"mounts": mounts, "broad_access": broad}


def _check_auth(config: dict | None) -> dict:
    if config is None:
        return {"auth_enabled": False, "method": None}
    auth = config.get("auth", {})
    enabled = auth.get("enabled", False) if isinstance(auth, dict) else bool(auth)
    method = auth.get("method", "unknown") if isinstance(auth, dict) else None
    return {"auth_enabled": enabled, "method": method}


def _detect_openclaw_version() -> str | None:
    """Try to detect OpenClaw version from running container or config."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=openclaw", "--format", "{{.Image}}"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            image = result.stdout.strip().split("\n")[0]
            # Extract tag as version (e.g., "openclaw:1.2.3" → "1.2.3")
            if ":" in image:
                return image.split(":")[-1]
            return "latest"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _check_openclaw_reachable() -> bool:
    """Check if OpenClaw API is reachable."""
    try:
        import httpx
        resp = httpx.get("http://localhost:8080/health", timeout=5)
        return resp.status_code < 500
    except Exception:
        return False


def _check_updates() -> dict:
    """Check for version updates using live detection."""
    detected = _detect_openclaw_version()
    current = detected or "unknown"

    # Compare against known latest (in real deployment, fetch from registry)
    latest = "1.2.0"
    up_to_date = current == latest or current == "latest" or current == "unknown"

    return {
        "up_to_date": up_to_date,
        "current_version": current,
        "latest_version": latest,
        "detected": detected is not None,
    }


def scan_openclaw(config_path: str | None = None) -> dict:
    """Run a full scan and return raw findings.

    Args:
        config_path: Optional override for OpenClaw config path.
                     Uses settings.openclaw_config_path if not provided.
    """
    config = _load_openclaw_config(config_path)
    detected = config is not None

    return {
        "openclaw_detected": detected,
        "network": _check_network(config),
        "tools": _check_tools(config),
        "data": _check_data(config),
        "auth": _check_auth(config),
        "updates": _check_updates(),
    }


def get_demo_findings() -> dict:
    """Return demo findings when OpenClaw is not installed (for development)."""
    return {
        "openclaw_detected": False,
        "network": {
            "bind_address": "0.0.0.0",
            "is_localhost": False,
            "port": 8080,
            "exposed": True,
        },
        "tools": {
            "skills": [
                {"name": "web_search", "risk": "low", "enabled": True},
                {"name": "file_read", "risk": "medium", "enabled": True},
                {"name": "shell_exec", "risk": "high", "enabled": True},
            ],
            "high_risk_enabled": True,
            "high_risk_skills": ["shell_exec"],
            "total": 3,
        },
        "data": {
            "mounts": ["/home/user/documents", "/"],
            "broad_access": True,
        },
        "auth": {"auth_enabled": False, "method": None},
        "updates": {
            "up_to_date": False,
            "current_version": "0.0.9",
            "latest_version": "1.0.0",
        },
    }
