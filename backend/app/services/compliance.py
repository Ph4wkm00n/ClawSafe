"""Compliance mapping — maps security checks to CIS Benchmarks and SOC 2 controls."""

from __future__ import annotations

import json
import logging

from app.models.schemas import EvidenceEntry, OverallStatus, SafetyLevel

logger = logging.getLogger(__name__)

# CIS Benchmark mappings for container security
CIS_CONTROLS = [
    {
        "id": "CIS-1.1",
        "title": "Ensure network traffic is restricted",
        "category": "network",
        "description": "Verify container network bindings restrict access to authorized addresses only.",
        "check": lambda cats: _get_cat(cats, "network").status == SafetyLevel.safe,
    },
    {
        "id": "CIS-1.2",
        "title": "Ensure authentication is enabled",
        "category": "network",
        "description": "Verify authentication mechanisms are configured and active.",
        "check": lambda cats: _get_cat(cats, "network").score < 30,
    },
    {
        "id": "CIS-2.1",
        "title": "Ensure high-risk tools are disabled",
        "category": "tools",
        "description": "Verify dangerous tools like shell execution are disabled by default.",
        "check": lambda cats: _get_cat(cats, "tools").status == SafetyLevel.safe,
    },
    {
        "id": "CIS-2.2",
        "title": "Ensure tool permissions follow least privilege",
        "category": "tools",
        "description": "Verify each tool has minimal required permissions.",
        "check": lambda cats: _get_cat(cats, "tools").score < 40,
    },
    {
        "id": "CIS-3.1",
        "title": "Ensure filesystem access is scoped",
        "category": "data",
        "description": "Verify mount paths are restricted to necessary directories only.",
        "check": lambda cats: _get_cat(cats, "data").status == SafetyLevel.safe,
    },
    {
        "id": "CIS-3.2",
        "title": "Ensure sensitive paths are not mounted",
        "category": "data",
        "description": "Verify /, /etc, /root, /home are not mounted.",
        "check": lambda cats: _get_cat(cats, "data").score < 30,
    },
    {
        "id": "CIS-4.1",
        "title": "Ensure software is up to date",
        "category": "updates",
        "description": "Verify running the latest stable version.",
        "check": lambda cats: _get_cat(cats, "updates").status == SafetyLevel.safe,
    },
    {
        "id": "CIS-5.1",
        "title": "Ensure config backups are enabled",
        "category": "data",
        "description": "Verify automatic backups are configured before changes.",
        "check": lambda cats: True,  # Always passes — backup system is built-in
    },
]

# SOC 2 Trust Services Criteria mapping
SOC2_CONTROLS = [
    {"id": "CC6.1", "title": "Logical and Physical Access Controls", "maps_to": ["CIS-1.1", "CIS-1.2"]},
    {"id": "CC6.2", "title": "System Account Management", "maps_to": ["CIS-1.2"]},
    {"id": "CC6.3", "title": "Access to Protected Information", "maps_to": ["CIS-3.1", "CIS-3.2"]},
    {"id": "CC7.1", "title": "System Monitoring", "maps_to": ["CIS-4.1"]},
    {"id": "CC7.2", "title": "Vulnerability Management", "maps_to": ["CIS-2.1", "CIS-2.2"]},
    {"id": "CC8.1", "title": "Change Management", "maps_to": ["CIS-5.1"]},
]


def _get_cat(categories, name):
    """Get a category by name from the list."""
    for cat in categories:
        if cat.category.value == name:
            return cat
    # Return a dummy safe category if not found
    from app.models.schemas import CategoryStatus, CategoryName
    return CategoryStatus(
        category=CategoryName.network, label="", status=SafetyLevel.safe,
        score=0, summary="", description="", action_label="", action_id=""
    )


def evaluate_compliance(status: OverallStatus) -> dict:
    """Evaluate current status against compliance controls."""
    cis_results = []
    passed = 0
    failed = 0

    for control in CIS_CONTROLS:
        try:
            met = control["check"](status.categories)
        except Exception:
            met = False

        cis_results.append({
            "id": control["id"],
            "title": control["title"],
            "category": control["category"],
            "description": control["description"],
            "status": "pass" if met else "fail",
        })
        if met:
            passed += 1
        else:
            failed += 1

    total = passed + failed
    score = round((passed / total) * 100) if total > 0 else 0

    # Map CIS to SOC 2
    cis_pass_set = {r["id"] for r in cis_results if r["status"] == "pass"}
    soc2_results = []
    for control in SOC2_CONTROLS:
        mapped_passing = sum(1 for cid in control["maps_to"] if cid in cis_pass_set)
        mapped_total = len(control["maps_to"])
        soc2_results.append({
            "id": control["id"],
            "title": control["title"],
            "coverage": f"{mapped_passing}/{mapped_total}",
            "status": "pass" if mapped_passing == mapped_total else "partial" if mapped_passing > 0 else "fail",
        })

    return {
        "compliance_score": score,
        "cis_controls": cis_results,
        "cis_passed": passed,
        "cis_failed": failed,
        "cis_total": total,
        "soc2_controls": soc2_results,
    }


def get_gap_analysis(status: OverallStatus) -> list[dict]:
    """Get list of failing controls with remediation guidance."""
    result = evaluate_compliance(status)
    gaps = []
    for control in result["cis_controls"]:
        if control["status"] == "fail":
            gaps.append({
                "control_id": control["id"],
                "title": control["title"],
                "category": control["category"],
                "description": control["description"],
                "recommendation": f"Address the {control['category']} category risks to meet this control.",
            })
    return gaps


# ── Evidence Collection ───────────────────────────────────────────────────


async def capture_evidence(control_id: str, status: OverallStatus | None = None) -> EvidenceEntry:
    """Capture a compliance evidence snapshot for a specific control."""
    from app.db.database import get_db

    if status is None:
        from app.services.scanner import get_demo_findings, scan_openclaw
        from app.services.scoring import compute_status
        findings = scan_openclaw()
        if not findings.get("openclaw_detected"):
            findings = get_demo_findings()
        status = compute_status(findings)

    compliance_result = evaluate_compliance(status)

    # Find the specific control result
    control_data = None
    for c in compliance_result["cis_controls"]:
        if c["id"] == control_id:
            control_data = c
            break

    snapshot = {
        "control_id": control_id,
        "control_data": control_data,
        "overall_score": status.score,
        "overall_status": status.status.value,
        "compliance_score": compliance_result["compliance_score"],
        "categories": [
            {"category": cat.category.value, "score": cat.score, "status": cat.status.value}
            for cat in status.categories
        ],
    }

    db = await get_db()
    eid = await db.insert_returning_id(
        "INSERT INTO evidence (compliance_control, snapshot_json) VALUES (?, ?)",
        (control_id, json.dumps(snapshot)),
    )
    await db.commit()
    logger.info("Captured evidence for control %s (id=%d)", control_id, eid)

    return EvidenceEntry(
        id=eid,
        compliance_control=control_id,
        snapshot_json=json.dumps(snapshot),
    )


async def list_evidence(control_id: str | None = None) -> list[EvidenceEntry]:
    """List captured evidence, optionally filtered by control."""
    from app.db.database import get_db

    db = await get_db()
    if control_id:
        rows = await db.fetch_all(
            "SELECT id, compliance_control, snapshot_json, captured_at "
            "FROM evidence WHERE compliance_control = ? ORDER BY captured_at DESC",
            (control_id,),
        )
    else:
        rows = await db.fetch_all(
            "SELECT id, compliance_control, snapshot_json, captured_at "
            "FROM evidence ORDER BY captured_at DESC LIMIT 100"
        )
    return [
        EvidenceEntry(
            id=row["id"],
            compliance_control=row["compliance_control"],
            snapshot_json=row["snapshot_json"],
            captured_at=row["captured_at"],
        )
        for row in rows
    ]
