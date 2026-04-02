"""Plugin registry — discover, search, and install plugins from a registry."""

from __future__ import annotations

import logging
from pathlib import Path

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

# Bundled default registry index
BUNDLED_REGISTRY: list[dict] = [
    {
        "name": "trivy-scanner",
        "version": "1.0.0",
        "type": "scanner",
        "description": "Container image vulnerability scanner using Trivy",
        "author": "ClawSafe Community",
        "url": "",
    },
    {
        "name": "slack-notifier",
        "version": "1.0.0",
        "type": "notifier",
        "description": "Enhanced Slack notifications with thread support",
        "author": "ClawSafe Community",
        "url": "",
    },
    {
        "name": "cis-scanner",
        "version": "1.0.0",
        "type": "scanner",
        "description": "CIS Benchmark compliance scanner",
        "author": "ClawSafe Community",
        "url": "",
    },
    {
        "name": "auto-fixer",
        "version": "1.0.0",
        "type": "fixer",
        "description": "Automated remediation for common misconfigurations",
        "author": "ClawSafe Community",
        "url": "",
    },
    {
        "name": "pagerduty-notifier",
        "version": "1.0.0",
        "type": "notifier",
        "description": "PagerDuty incident creation on critical alerts",
        "author": "ClawSafe Community",
        "url": "",
    },
]


async def fetch_registry() -> list[dict]:
    """Fetch plugin registry index (remote or bundled fallback)."""
    registry_url = settings.plugin_registry_url
    if registry_url:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(registry_url)
                if resp.status_code == 200:
                    return resp.json()
        except Exception as e:
            logger.warning("Failed to fetch remote registry: %s", e)

    return BUNDLED_REGISTRY


def search_plugins(registry: list[dict], query: str) -> list[dict]:
    """Search registry entries by name or description."""
    query_lower = query.lower()
    return [
        p for p in registry
        if query_lower in p["name"].lower() or query_lower in p.get("description", "").lower()
    ]


async def install_plugin(name: str, plugins_dir: str = "plugins") -> dict:
    """Install a plugin from the registry (downloads .py to plugins dir)."""
    registry = await fetch_registry()
    plugin = next((p for p in registry if p["name"] == name), None)
    if plugin is None:
        return {"success": False, "message": f"Plugin '{name}' not found in registry"}

    url = plugin.get("url", "")
    if not url:
        return {"success": False, "message": f"Plugin '{name}' has no download URL (bundled entry only)"}

    dest = Path(plugins_dir)
    dest.mkdir(parents=True, exist_ok=True)
    dest_file = dest / f"{name.replace('-', '_')}.py"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            dest_file.write_text(resp.text)
        logger.info("Installed plugin %s to %s", name, dest_file)
        return {"success": True, "message": f"Plugin '{name}' installed to {dest_file}"}
    except Exception as e:
        logger.error("Failed to install plugin %s: %s", name, e)
        return {"success": False, "message": f"Failed to download plugin: {e}"}
