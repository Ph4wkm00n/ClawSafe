"""Scoring service — converts raw findings into safety status and category scores."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from app.models.schemas import (
    CategoryName,
    CategoryStatus,
    OverallStatus,
    SafetyLevel,
)

logger = logging.getLogger(__name__)


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

    # Increase score if running a version with known advisories
    advisories = updates.get("advisories", [])
    if advisories:
        has_critical = any(a.get("severity") == "critical" for a in advisories)
        score = min(score + (40 if has_critical else 20), 100)

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


def _apply_policy_adjustments(
    categories: list[CategoryStatus], policy: dict | None
) -> list[CategoryStatus]:
    """Adjust scores based on active policy rules."""
    if not policy:
        return categories

    adjusted = []
    for cat in categories:
        extra = 0
        if cat.category == CategoryName.tools:
            rules = policy.get("tools", {}).get("rules", [])
            for rule in rules:
                if not isinstance(rule, dict):
                    continue
                if rule.get("action") == "block" and rule.get("risk") in ("high", "critical"):
                    # Policy says block high-risk → if they're still enabled, penalize more
                    pass  # Already handled by base scoring
                elif rule.get("action") == "allow" and rule.get("risk") in ("high", "critical"):
                    # Policy explicitly allows high-risk tools → increase risk
                    extra += 15
        elif cat.category == CategoryName.network:
            net_policy = policy.get("network", {})
            if net_policy.get("vpn_only") and not cat.description.lower().startswith("your"):
                extra += 10  # VPN required but not enforced
        if extra > 0:
            new_score = min(cat.score + extra, 100)
            new_level = _level_from_score(new_score)
            adjusted.append(cat.model_copy(update={"score": new_score, "status": new_level}))
        else:
            adjusted.append(cat)
    return adjusted


# ── Contextual Risk Weighting ─────────────────────────────────────────────

ENVIRONMENT_WEIGHTS = {
    "production": 1.5,
    "staging": 1.0,
    "development": 0.5,
}


def detect_environment() -> str:
    """Auto-detect deployment environment."""
    from app.core.config import settings
    if settings.deploy_environment:
        return settings.deploy_environment

    # Check common environment indicators
    env = os.environ.get("CLAWSAFE_ENVIRONMENT", "")
    if env:
        return env.lower()

    # Kubernetes detection
    if os.environ.get("KUBERNETES_SERVICE_HOST"):
        return "production"

    # Docker detection
    if Path("/.dockerenv").exists():
        return "staging"

    # Default to development
    return "development"


def _apply_environment_weight(score: int) -> int:
    """Apply environment-based weight multiplier to a risk score."""
    env = detect_environment()
    weight = ENVIRONMENT_WEIGHTS.get(env, 1.0)
    return min(int(score * weight), 100)


def compute_status(findings: dict, policy: dict | None = None) -> OverallStatus:
    """Compute per-category and overall safety status from raw findings.

    If a policy dict is provided, scoring is adjusted based on policy rules.
    """
    categories = [
        _score_network(findings),
        _score_tools(findings),
        _score_data(findings),
        _score_updates(findings),
    ]
    categories = _apply_policy_adjustments(categories, policy)

    overall_score = max(c.score for c in categories) if categories else 0
    overall_score = _apply_environment_weight(overall_score)
    overall_level = _level_from_score(overall_score)

    return OverallStatus(
        status=overall_level,
        score=overall_score,
        subtitle=OVERALL_SUBTITLES[overall_level],
        categories=categories,
    )
