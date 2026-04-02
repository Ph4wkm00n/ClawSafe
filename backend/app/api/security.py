"""Security intelligence API — secrets scanning, compliance, runtime, advanced scoring."""

from fastapi import APIRouter, Depends, Query

from app.core.auth import require_auth

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/security/secrets")
async def scan_secrets(directory: str = Query(default="/etc/openclaw")):
    """Scan a directory for leaked secrets."""
    from app.services.secrets_scanner import scan_directory_for_secrets
    return scan_directory_for_secrets(directory)


@router.get("/security/secrets/env")
async def scan_env_secrets():
    """Check environment variables for sensitive data."""
    from app.services.secrets_scanner import scan_environment_for_secrets
    return {"findings": scan_environment_for_secrets()}


@router.get("/security/compliance")
async def get_compliance():
    """Evaluate compliance against CIS Benchmarks and SOC 2 controls."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.scoring import compute_status
    from app.services.compliance import evaluate_compliance

    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    status = compute_status(findings)
    return evaluate_compliance(status)


@router.get("/security/compliance/gaps")
async def get_compliance_gaps():
    """Get gap analysis showing failing compliance controls."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.scoring import compute_status
    from app.services.compliance import get_gap_analysis

    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    status = compute_status(findings)
    return {"gaps": get_gap_analysis(status)}


@router.get("/security/runtime")
async def get_runtime_status():
    """Get runtime monitoring report (process, network, resources)."""
    from app.services.runtime_monitor import get_runtime_report
    return get_runtime_report()


@router.get("/security/runtime/resources")
async def get_resources():
    """Get system resource usage and alerts."""
    from app.services.runtime_monitor import get_resource_usage, get_resource_alerts
    return {
        "resources": get_resource_usage(),
        "alerts": get_resource_alerts(),
    }


@router.get("/security/scoring/combined")
async def get_combined_risk():
    """Get combined risk analysis (correlated risks worse than sum of parts)."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.advanced_scoring import compute_combined_risk

    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    return compute_combined_risk(findings)


@router.get("/security/scoring/cvss")
async def get_cvss_score(
    attack_vector: str = Query(default="network"),
    attack_complexity: str = Query(default="low"),
    privileges_required: str = Query(default="none"),
):
    """Compute CVSS 3.1-style score for the current configuration."""
    from app.services.advanced_scoring import compute_cvss_score
    return compute_cvss_score(
        attack_vector=attack_vector,
        attack_complexity=attack_complexity,
        privileges_required=privileges_required,
    )


@router.get("/security/scoring/trends")
async def get_risk_trends(days: int = Query(default=30, ge=1, le=365)):
    """Get risk score trend over time."""
    from app.services.advanced_scoring import get_risk_trends
    trends = await get_risk_trends(days=days)
    return {"trends": trends, "days": days}


@router.get("/security/scoring/blast-radius")
async def get_blast_radius():
    """Estimate blast radius if this instance is compromised."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.advanced_scoring import estimate_blast_radius

    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    return estimate_blast_radius(findings)


@router.get("/security/rules")
async def evaluate_custom_rules():
    """Evaluate custom YAML-based detection rules."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.rule_engine import evaluate_rules

    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    config = findings  # Pass full findings as config context
    results = evaluate_rules(config, findings)
    return {"rules_evaluated": len(results), "triggered": results}


@router.get("/plugins")
async def list_plugins():
    """List all loaded plugins."""
    from app.plugins.loader import list_all_plugins
    return {"plugins": list_all_plugins()}


@router.get("/plugins/registry")
async def get_plugin_registry(query: str = Query(default="")):
    """Browse the plugin registry."""
    from app.services.plugin_registry import fetch_registry, search_plugins
    registry = await fetch_registry()
    if query:
        registry = search_plugins(registry, query)
    return {"plugins": registry, "total": len(registry)}


@router.post("/plugins/install")
async def install_plugin_from_registry(name: str = Query(...)):
    """Install a plugin from the registry."""
    from app.services.plugin_registry import install_plugin
    result = await install_plugin(name)
    return result


# ── Dependency Scanning ───────────────────────────────────────────────────


@router.get("/security/dependencies")
async def scan_deps():
    """Scan installed packages for known vulnerabilities."""
    from app.services.dependency_scanner import scan_dependencies
    vulns = scan_dependencies()
    return {"vulnerabilities": vulns, "total": len(vulns)}


# ── SBOM ──────────────────────────────────────────────────────────────────


@router.get("/security/sbom")
async def get_sbom():
    """Generate Software Bill of Materials (CycloneDX format)."""
    from app.services.sbom import generate_sbom
    return generate_sbom()


@router.get("/security/sbom/json")
async def get_sbom_json():
    """Generate SBOM in native CycloneDX JSON format."""
    from app.services.sbom import generate_sbom_json
    return generate_sbom_json()


# ── Skill Execution Auditing ─────────────────────────────────────────────


@router.get("/security/skill-audit")
async def get_skill_audit(
    instance_id: str | None = Query(default=None),
    skill_name: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
):
    """Get skill execution audit trail."""
    from app.services.skill_audit import get_skill_executions
    executions = await get_skill_executions(instance_id, skill_name, limit)
    return {"executions": [e.model_dump() for e in executions], "total": len(executions)}


@router.get("/security/skill-audit/stats")
async def get_skill_audit_stats():
    """Get aggregated skill execution statistics."""
    from app.services.skill_audit import get_skill_execution_stats
    return await get_skill_execution_stats()


# ── Evidence Collection ───────────────────────────────────────────────────


@router.get("/security/evidence")
async def get_evidence(control_id: str | None = Query(default=None)):
    """List captured compliance evidence."""
    from app.services.compliance import list_evidence
    entries = await list_evidence(control_id)
    return {"evidence": [e.model_dump() for e in entries], "total": len(entries)}


@router.post("/security/evidence/capture")
async def capture_evidence_snapshot(control_id: str = Query(...)):
    """Capture a compliance evidence snapshot for a specific control."""
    from app.services.compliance import capture_evidence
    entry = await capture_evidence(control_id)
    return entry.model_dump()
