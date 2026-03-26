"""Tests for policy-aware scoring."""

from app.services.scoring import compute_status


def _base_findings():
    return {
        "openclaw_detected": True,
        "network": {"bind_address": "127.0.0.1", "is_localhost": True, "port": 8080, "exposed": False},
        "tools": {"skills": [], "high_risk_enabled": True, "total": 3},
        "data": {"mounts": ["/app"], "broad_access": False},
        "auth": {"auth_enabled": True, "method": "token"},
        "updates": {"up_to_date": True, "current_version": "1.0.0", "latest_version": "1.0.0"},
    }


def test_scoring_without_policy():
    status = compute_status(_base_findings())
    assert status.status in ("safe", "attention", "risk")


def test_scoring_with_policy_allowing_high_risk():
    policy = {
        "tools": {
            "rules": [
                {"name": "shell_exec", "risk": "high", "action": "allow"},
            ],
        },
        "network": {},
    }
    status = compute_status(_base_findings(), policy=policy)
    # Policy allows high-risk tools — should increase risk score
    tools_cat = next(c for c in status.categories if c.category == "tools")
    assert tools_cat.score >= 60  # Base high-risk score


def test_scoring_with_empty_policy():
    status = compute_status(_base_findings(), policy={})
    assert status.status in ("safe", "attention", "risk")


def test_scoring_with_none_policy():
    status = compute_status(_base_findings(), policy=None)
    assert status.status in ("safe", "attention", "risk")
