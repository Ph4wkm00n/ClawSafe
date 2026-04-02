"""Comparison service — current config vs recommended safe values."""

from __future__ import annotations

import logging

from app.models.schemas import ComparisonItem, ComparisonResponse
from app.services.scanner import get_demo_findings, scan_openclaw

logger = logging.getLogger(__name__)

# Recommended safe configuration values
RECOMMENDED = {
    "bind_address": "127.0.0.1",
    "auth_enabled": "true",
    "high_risk_tools": "disabled",
    "mount_access": "restricted",
    "up_to_date": "true",
}


async def get_config_comparison() -> ComparisonResponse:
    """Compare current config against recommended values."""
    findings = scan_openclaw()
    if not findings.get("openclaw_detected"):
        findings = get_demo_findings()

    net = findings.get("network", {})
    auth = findings.get("auth", {})
    tools = findings.get("tools", {})
    data = findings.get("data", {})
    updates = findings.get("updates", {})

    items = [
        ComparisonItem(
            field="Network Binding",
            current_value=net.get("bind_address", "unknown"),
            recommended_value=RECOMMENDED["bind_address"],
            status="match" if net.get("bind_address") == "127.0.0.1" else "mismatch",
        ),
        ComparisonItem(
            field="Authentication",
            current_value=str(auth.get("auth_enabled", False)).lower(),
            recommended_value=RECOMMENDED["auth_enabled"],
            status="match" if auth.get("auth_enabled") else "mismatch",
        ),
        ComparisonItem(
            field="High-Risk Tools",
            current_value="disabled" if not tools.get("high_risk_enabled") else "enabled",
            recommended_value=RECOMMENDED["high_risk_tools"],
            status="match" if not tools.get("high_risk_enabled") else "mismatch",
        ),
        ComparisonItem(
            field="Mount Access",
            current_value="restricted" if not data.get("broad_access") else "broad",
            recommended_value=RECOMMENDED["mount_access"],
            status="match" if not data.get("broad_access") else "mismatch",
        ),
        ComparisonItem(
            field="Version Up-to-Date",
            current_value=str(updates.get("up_to_date", False)).lower(),
            recommended_value=RECOMMENDED["up_to_date"],
            status="match" if updates.get("up_to_date") else "mismatch",
        ),
    ]

    matches = sum(1 for i in items if i.status == "match")
    pct = round(matches * 100 / max(len(items), 1))

    return ComparisonResponse(items=items, match_percentage=pct)
