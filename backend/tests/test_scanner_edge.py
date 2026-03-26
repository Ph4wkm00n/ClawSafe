"""Edge case tests for the scanner service."""

from app.services.scanner import scan_openclaw, _check_network, _check_tools, _check_data


def test_check_network_with_none():
    result = _check_network(None)
    assert result["exposed"] is True
    assert result["bind_address"] == "unknown"


def test_check_network_with_localhost():
    config = {"bind_address": "127.0.0.1", "port": 8080}
    result = _check_network(config)
    assert result["is_localhost"] is True
    assert result["exposed"] is False


def test_check_tools_with_no_skills():
    config = {"skills": []}
    result = _check_tools(config)
    assert result["high_risk_enabled"] is False
    assert result["total"] == 0


def test_check_tools_with_non_list_skills():
    config = {"skills": "not a list"}
    result = _check_tools(config)
    assert result["total"] == 0


def test_check_data_with_non_list_mounts():
    config = {"mounts": "not a list"}
    result = _check_data(config)
    assert result["broad_access"] is False


def test_check_data_with_sensitive_mounts():
    config = {"mounts": ["/", "/home/user/docs"]}
    result = _check_data(config)
    assert result["broad_access"] is True


def test_scan_openclaw_returns_all_categories():
    result = scan_openclaw()
    assert "network" in result
    assert "tools" in result
    assert "data" in result
    assert "auth" in result
    assert "updates" in result
    assert "openclaw_detected" in result
