"""Advanced scoring — CVSS vectors, combined risk, contextual weighting, trends."""

from __future__ import annotations

import logging

from app.db.database import get_db

logger = logging.getLogger(__name__)

# CVSS 3.1 Base Score components (simplified)
ATTACK_VECTOR = {"network": 0.85, "adjacent": 0.62, "local": 0.55, "physical": 0.20}
ATTACK_COMPLEXITY = {"low": 0.77, "high": 0.44}
PRIVILEGES_REQUIRED = {"none": 0.85, "low": 0.62, "high": 0.27}
USER_INTERACTION = {"none": 0.85, "required": 0.62}
IMPACT_CONFIDENTIALITY = {"high": 0.56, "low": 0.22, "none": 0.0}
IMPACT_INTEGRITY = {"high": 0.56, "low": 0.22, "none": 0.0}
IMPACT_AVAILABILITY = {"high": 0.56, "low": 0.22, "none": 0.0}


def compute_cvss_score(
    attack_vector: str = "network",
    attack_complexity: str = "low",
    privileges_required: str = "none",
    user_interaction: str = "none",
    confidentiality: str = "low",
    integrity: str = "low",
    availability: str = "low",
) -> dict:
    """Compute CVSS 3.1-style base score from vector components."""
    av = ATTACK_VECTOR.get(attack_vector, 0.85)
    ac = ATTACK_COMPLEXITY.get(attack_complexity, 0.77)
    pr = PRIVILEGES_REQUIRED.get(privileges_required, 0.85)
    ui = USER_INTERACTION.get(user_interaction, 0.85)

    # Exploitability sub-score
    exploitability = 8.22 * av * ac * pr * ui

    # Impact sub-score
    isc_base = 1 - (
        (1 - IMPACT_CONFIDENTIALITY.get(confidentiality, 0.22))
        * (1 - IMPACT_INTEGRITY.get(integrity, 0.22))
        * (1 - IMPACT_AVAILABILITY.get(availability, 0.22))
    )
    impact = 6.42 * isc_base

    if impact <= 0:
        base_score = 0.0
    else:
        base_score = min(10.0, round(1.08 * (impact + exploitability), 1))

    severity = "none"
    if base_score >= 9.0:
        severity = "critical"
    elif base_score >= 7.0:
        severity = "high"
    elif base_score >= 4.0:
        severity = "medium"
    elif base_score > 0:
        severity = "low"

    return {
        "base_score": base_score,
        "severity": severity,
        "exploitability": round(exploitability, 2),
        "impact": round(impact, 2),
        "vector": f"AV:{attack_vector[0].upper()}/AC:{attack_complexity[0].upper()}/PR:{privileges_required[0].upper()}/UI:{user_interaction[0].upper()}/C:{confidentiality[0].upper()}/I:{integrity[0].upper()}/A:{availability[0].upper()}",
    }


def compute_combined_risk(findings: dict) -> dict:
    """Analyze combined risk across categories (correlations, not just addition)."""
    network = findings.get("network", {})
    auth = findings.get("auth", {})
    tools = findings.get("tools", {})
    data = findings.get("data", {})

    # Combined risk patterns (worse than sum of parts)
    critical_combos = []
    combined_score = 0

    # Exposed + no auth = critical
    if network.get("exposed") and not auth.get("auth_enabled"):
        critical_combos.append({
            "pattern": "exposed_no_auth",
            "description": "Publicly exposed without authentication — anyone can access and control OpenClaw.",
            "severity": "critical",
            "score_boost": 30,
        })
        combined_score += 30

    # Exposed + shell_exec enabled = critical
    if network.get("exposed") and tools.get("high_risk_enabled"):
        critical_combos.append({
            "pattern": "exposed_shell_access",
            "description": "Public exposure combined with shell execution — remote code execution possible.",
            "severity": "critical",
            "score_boost": 40,
        })
        combined_score += 40

    # No auth + broad mounts = critical
    if not auth.get("auth_enabled") and data.get("broad_access"):
        critical_combos.append({
            "pattern": "no_auth_broad_access",
            "description": "No authentication with broad filesystem access — data exfiltration risk.",
            "severity": "critical",
            "score_boost": 25,
        })
        combined_score += 25

    # Shell exec + broad mounts = high
    if tools.get("high_risk_enabled") and data.get("broad_access"):
        critical_combos.append({
            "pattern": "shell_broad_access",
            "description": "Shell execution with broad filesystem access — system compromise risk.",
            "severity": "high",
            "score_boost": 20,
        })
        combined_score += 20

    return {
        "combined_score": min(combined_score, 100),
        "critical_combinations": critical_combos,
        "total_patterns": len(critical_combos),
    }


async def get_risk_trends(instance_id: str = "default", days: int = 30) -> list[dict]:
    """Get risk score trend over time from scan history."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT timestamp, score, overall_status FROM scans "
        "WHERE timestamp > datetime('now', ?) "
        "ORDER BY timestamp ASC",
        (f"-{days} days",),
    )
    return [
        {
            "timestamp": row["timestamp"],
            "score": row["score"],
            "status": row["overall_status"],
        }
        for row in rows
    ]


def estimate_blast_radius(findings: dict) -> dict:
    """Estimate the blast radius if this instance is compromised."""
    network = findings.get("network", {})
    tools = findings.get("tools", {})
    data = findings.get("data", {})

    affected_systems = []
    risk_level = "low"

    if network.get("exposed"):
        affected_systems.append("External network (internet-facing)")
        risk_level = "high"

    if not network.get("is_localhost"):
        affected_systems.append("Local network (other devices on same network)")
        if risk_level == "low":
            risk_level = "medium"

    if data.get("broad_access"):
        affected_systems.append("Host filesystem (sensitive system files)")
        risk_level = "critical"

    if tools.get("high_risk_enabled"):
        affected_systems.append("Host operating system (via shell execution)")
        risk_level = "critical"

    mounts = data.get("mounts", [])
    if isinstance(mounts, list):
        for mount in mounts:
            if isinstance(mount, str) and mount not in ("/", "/etc", "/root", "/home"):
                affected_systems.append(f"Mounted directory: {mount}")

    return {
        "risk_level": risk_level,
        "affected_systems": affected_systems,
        "total_affected": len(affected_systems),
        "recommendation": _blast_radius_recommendation(risk_level),
    }


def _blast_radius_recommendation(risk_level: str) -> str:
    recommendations = {
        "critical": "Isolate this instance immediately. Restrict network access and disable shell execution.",
        "high": "Reduce exposure by binding to localhost and enabling authentication.",
        "medium": "Consider restricting network access to private subnets only.",
        "low": "Current blast radius is minimal. Continue monitoring.",
    }
    return recommendations.get(risk_level, "Monitor and review regularly.")
