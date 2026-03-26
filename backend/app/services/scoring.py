"""Scoring service — converts raw findings into safety status and category scores."""

from __future__ import annotations

from app.models.schemas import (
    CategoryName,
    CategoryStatus,
    OverallStatus,
    SafetyLevel,
)


def _level_from_score(score: int) -> SafetyLevel:
    if score < 30:
        return SafetyLevel.safe
    if score < 70:
        return SafetyLevel.attention
    return SafetyLevel.risk


def _score_network(findings: dict) -> CategoryStatus:
    net = findings.get("network", {})
    auth = findings.get("auth", {})

    score = 0
    if net.get("exposed"):
        score += 50
    if not auth.get("auth_enabled"):
        score += 30
    if net.get("bind_address") == "0.0.0.0":
        score += 10

    level = _level_from_score(score)

    summaries = {
        SafetyLevel.safe: "Only reachable from this machine. Nice and private.",
        SafetyLevel.attention: "OpenClaw might be reachable from your local network.",
        SafetyLevel.risk: "People outside your home can reach OpenClaw. This makes hacking easier.",
    }
    descriptions = {
        SafetyLevel.safe: "Your OpenClaw instance is bound to localhost and protected with authentication.",
        SafetyLevel.attention: "Some network settings could be tighter. Consider restricting access.",
        SafetyLevel.risk: "OpenClaw is exposed on all interfaces without proper authentication. This is dangerous.",
    }
    actions = {
        SafetyLevel.safe: "Review details",
        SafetyLevel.attention: "Tighten access",
        SafetyLevel.risk: "Make it private",
    }

    return CategoryStatus(
        category=CategoryName.network,
        label="Network",
        status=level,
        score=score,
        summary=summaries[level],
        description=descriptions[level],
        action_label=actions[level],
        action_id="fix_network_binding",
    )


def _score_tools(findings: dict) -> CategoryStatus:
    tools = findings.get("tools", {})

    score = 0
    if tools.get("high_risk_enabled"):
        score += 60
    if tools.get("total", 0) > 5:
        score += 10

    level = _level_from_score(score)

    summaries = {
        SafetyLevel.safe: "Only safe abilities are turned on.",
        SafetyLevel.attention: "Some powerful abilities are enabled. Review if you need them.",
        SafetyLevel.risk: "High-risk abilities are active (e.g., shell access). This is dangerous unless you know why.",
    }
    descriptions = {
        SafetyLevel.safe: "All enabled skills are low-risk. No dangerous tools are active.",
        SafetyLevel.attention: "Some medium-risk skills are enabled. Consider whether you need all of them.",
        SafetyLevel.risk: "Dangerous skills like shell execution are active. Disable them unless required.",
    }
    actions = {
        SafetyLevel.safe: "Review abilities",
        SafetyLevel.attention: "Review abilities",
        SafetyLevel.risk: "Disable risky tools",
    }

    return CategoryStatus(
        category=CategoryName.tools,
        label="Tools & Skills",
        status=level,
        score=score,
        summary=summaries[level],
        description=descriptions[level],
        action_label=actions[level],
        action_id="fix_tools_policy",
    )


def _score_data(findings: dict) -> CategoryStatus:
    data = findings.get("data", {})

    score = 0
    if data.get("broad_access"):
        score += 70
    elif len(data.get("mounts", [])) > 3:
        score += 30

    level = _level_from_score(score)

    summaries = {
        SafetyLevel.safe: "OpenClaw can only see the folders it needs.",
        SafetyLevel.attention: "Some broad folder access detected. Consider limiting it.",
        SafetyLevel.risk: "OpenClaw can access sensitive areas of your system.",
    }
    descriptions = {
        SafetyLevel.safe: "File mounts are scoped to safe directories only.",
        SafetyLevel.attention: "Several directories are mounted. Review whether all are needed.",
        SafetyLevel.risk: "Root or sensitive system paths are mounted. This gives OpenClaw too much access.",
    }
    actions = {
        SafetyLevel.safe: "Review details",
        SafetyLevel.attention: "Limit access",
        SafetyLevel.risk: "Limit access",
    }

    return CategoryStatus(
        category=CategoryName.data,
        label="Data & Files",
        status=level,
        score=score,
        summary=summaries[level],
        description=descriptions[level],
        action_label=actions[level],
        action_id="fix_data_mounts",
    )


def _score_updates(findings: dict) -> CategoryStatus:
    updates = findings.get("updates", {})

    score = 0 if updates.get("up_to_date") else 50

    level = _level_from_score(score)

    summaries = {
        SafetyLevel.safe: "Everything is up to date.",
        SafetyLevel.attention: "An update is available.",
        SafetyLevel.risk: "You're running an old version with known security issues.",
    }
    descriptions = {
        SafetyLevel.safe: f"Running version {updates.get('current_version', 'unknown')}. No updates needed.",
        SafetyLevel.attention: f"Version {updates.get('latest_version', 'unknown')} is available. You're on {updates.get('current_version', 'unknown')}.",
        SafetyLevel.risk: f"Your version {updates.get('current_version', 'unknown')} is outdated. Please update to {updates.get('latest_version', 'unknown')}.",
    }
    actions = {
        SafetyLevel.safe: "Review details",
        SafetyLevel.attention: "See update guide",
        SafetyLevel.risk: "See update guide",
    }

    return CategoryStatus(
        category=CategoryName.updates,
        label="Updates & Health",
        status=level,
        score=score,
        summary=summaries[level],
        description=descriptions[level],
        action_label=actions[level],
        action_id="fix_updates",
    )


OVERALL_SUBTITLES = {
    SafetyLevel.safe: "Your AI helper looks well protected.",
    SafetyLevel.attention: "Some things could be safer. We'll show you how.",
    SafetyLevel.risk: "Important risks found. Please review these now.",
}


def compute_status(findings: dict) -> OverallStatus:
    """Compute per-category and overall safety status from raw findings."""
    categories = [
        _score_network(findings),
        _score_tools(findings),
        _score_data(findings),
        _score_updates(findings),
    ]

    overall_score = max(c.score for c in categories) if categories else 0
    overall_level = _level_from_score(overall_score)

    return OverallStatus(
        status=overall_level,
        score=overall_score,
        subtitle=OVERALL_SUBTITLES[overall_level],
        categories=categories,
    )
