from app.services.scoring import compute_status


def test_safe_findings():
    findings = {
        "openclaw_detected": True,
        "network": {"bind_address": "127.0.0.1", "is_localhost": True, "port": 8080, "exposed": False},
        "tools": {"skills": [], "high_risk_enabled": False, "total": 0},
        "data": {"mounts": ["/app/data"], "broad_access": False},
        "auth": {"auth_enabled": True, "method": "token"},
        "updates": {"up_to_date": True, "current_version": "0.1.0", "latest_version": "0.1.0"},
    }
    status = compute_status(findings)
    assert status.status == "safe"
    assert all(c.status == "safe" for c in status.categories)


def test_risky_findings():
    findings = {
        "openclaw_detected": True,
        "network": {"bind_address": "0.0.0.0", "is_localhost": False, "port": 8080, "exposed": True},
        "tools": {"skills": [], "high_risk_enabled": True, "total": 3},
        "data": {"mounts": ["/"], "broad_access": True},
        "auth": {"auth_enabled": False, "method": None},
        "updates": {"up_to_date": False, "current_version": "0.0.9", "latest_version": "0.1.0"},
    }
    status = compute_status(findings)
    assert status.status == "risk"
    assert status.score >= 70


def test_mixed_findings():
    findings = {
        "openclaw_detected": True,
        "network": {"bind_address": "127.0.0.1", "is_localhost": True, "port": 8080, "exposed": False},
        "tools": {"skills": [], "high_risk_enabled": True, "total": 2},
        "data": {"mounts": ["/app"], "broad_access": False},
        "auth": {"auth_enabled": True, "method": "token"},
        "updates": {"up_to_date": True, "current_version": "0.1.0", "latest_version": "0.1.0"},
    }
    status = compute_status(findings)
    # Tools are risky but network/data/updates are safe
    assert status.status in ("attention", "risk")
    network = next(c for c in status.categories if c.category == "network")
    assert network.status == "safe"
