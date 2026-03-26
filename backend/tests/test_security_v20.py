"""Tests for v2.0 Security Intelligence features."""

import pytest


# ── Secrets Scanner ─────────────────────────────────────────────────────────

def test_secrets_scanner_detects_aws_key():
    from app.services.secrets_scanner import SECRET_PATTERNS
    import re
    pattern = next(p for p in SECRET_PATTERNS if p["name"] == "AWS Access Key")
    assert re.search(pattern["pattern"], "AKIAIOSFODNN7EXAMPLE")


def test_secrets_scanner_detects_private_key():
    from app.services.secrets_scanner import SECRET_PATTERNS
    import re
    pattern = next(p for p in SECRET_PATTERNS if p["name"] == "Private Key Header")
    assert re.search(pattern["pattern"], "-----BEGIN RSA PRIVATE KEY-----")


def test_scan_environment():
    from app.services.secrets_scanner import scan_environment_for_secrets
    results = scan_environment_for_secrets()
    assert isinstance(results, list)


# ── Rule Engine ─────────────────────────────────────────────────────────────

def test_rule_engine_evaluate():
    from app.services.rule_engine import _evaluate_condition
    condition = {"field": "network.exposed", "operator": "equals", "value": True}
    config = {"network": {"exposed": True}}
    assert _evaluate_condition(condition, config, {}) is True


def test_rule_engine_nested_field():
    from app.services.rule_engine import _get_nested_value
    data = {"a": {"b": {"c": 42}}}
    assert _get_nested_value(data, "a.b.c") == 42
    assert _get_nested_value(data, "a.b.d") is None


# ── Compliance ──────────────────────────────────────────────────────────────

def test_compliance_evaluation():
    from app.services.compliance import evaluate_compliance
    from app.services.scoring import compute_status
    from app.services.scanner import get_demo_findings

    findings = get_demo_findings()
    status = compute_status(findings)
    result = evaluate_compliance(status)
    assert "compliance_score" in result
    assert "cis_controls" in result
    assert "soc2_controls" in result
    assert result["cis_total"] > 0


def test_gap_analysis():
    from app.services.compliance import get_gap_analysis
    from app.services.scoring import compute_status
    from app.services.scanner import get_demo_findings

    findings = get_demo_findings()
    status = compute_status(findings)
    gaps = get_gap_analysis(status)
    assert isinstance(gaps, list)
    # Demo findings should have some failing controls
    assert len(gaps) > 0


# ── Advanced Scoring ────────────────────────────────────────────────────────

def test_cvss_computation():
    from app.services.advanced_scoring import compute_cvss_score
    result = compute_cvss_score(
        attack_vector="network",
        attack_complexity="low",
        privileges_required="none",
    )
    assert "base_score" in result
    assert "severity" in result
    assert "vector" in result
    assert result["base_score"] > 0


def test_combined_risk_analysis():
    from app.services.advanced_scoring import compute_combined_risk
    from app.services.scanner import get_demo_findings
    findings = get_demo_findings()
    result = compute_combined_risk(findings)
    assert "combined_score" in result
    assert "critical_combinations" in result
    # Demo data has exposed + no auth + shell_exec
    assert result["total_patterns"] > 0


def test_blast_radius():
    from app.services.advanced_scoring import estimate_blast_radius
    from app.services.scanner import get_demo_findings
    findings = get_demo_findings()
    result = estimate_blast_radius(findings)
    assert "risk_level" in result
    assert "affected_systems" in result
    assert result["total_affected"] > 0


# ── Runtime Monitor ─────────────────────────────────────────────────────────

def test_resource_usage():
    from app.services.runtime_monitor import get_resource_usage
    result = get_resource_usage()
    assert "disk" in result
    assert "memory" in result


def test_resource_alerts():
    from app.services.runtime_monitor import get_resource_alerts
    alerts = get_resource_alerts(thresholds={"disk_percent": 99, "memory_percent": 99})
    assert isinstance(alerts, list)


def test_file_hash():
    from app.services.runtime_monitor import compute_file_hash
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("test content")
        f.flush()
        h = compute_file_hash(f.name)
        assert h is not None
        assert len(h) == 64  # SHA-256 hex


# ── Plugin System ───────────────────────────────────────────────────────────

def test_plugin_loader():
    from app.plugins.loader import list_all_plugins
    plugins = list_all_plugins()
    assert isinstance(plugins, list)


# ── API Endpoints ───────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_compliance_endpoint(client):
    resp = await client.get("/api/v1/security/compliance")
    assert resp.status_code == 200
    data = resp.json()
    assert "compliance_score" in data
    assert "cis_controls" in data


@pytest.mark.anyio
async def test_combined_risk_endpoint(client):
    resp = await client.get("/api/v1/security/scoring/combined")
    assert resp.status_code == 200
    data = resp.json()
    assert "combined_score" in data


@pytest.mark.anyio
async def test_cvss_endpoint(client):
    resp = await client.get("/api/v1/security/scoring/cvss")
    assert resp.status_code == 200
    data = resp.json()
    assert "base_score" in data


@pytest.mark.anyio
async def test_blast_radius_endpoint(client):
    resp = await client.get("/api/v1/security/scoring/blast-radius")
    assert resp.status_code == 200
    data = resp.json()
    assert "risk_level" in data


@pytest.mark.anyio
async def test_runtime_endpoint(client):
    resp = await client.get("/api/v1/security/runtime")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_plugins_endpoint(client):
    resp = await client.get("/api/v1/plugins")
    assert resp.status_code == 200
    data = resp.json()
    assert "plugins" in data


@pytest.mark.anyio
async def test_risk_trends_endpoint(client):
    resp = await client.get("/api/v1/security/scoring/trends")
    assert resp.status_code == 200
    data = resp.json()
    assert "trends" in data


@pytest.mark.anyio
async def test_custom_rules_endpoint(client):
    resp = await client.get("/api/v1/security/rules")
    assert resp.status_code == 200
    data = resp.json()
    assert "rules_evaluated" in data
