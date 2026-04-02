from app.services.advisories import check_advisories


def test_old_version_has_advisories():
    results = check_advisories("0.5.0")
    assert len(results) >= 1
    assert any(a["cve_id"] == "CVE-2025-0001" for a in results)


def test_current_version_no_advisories():
    results = check_advisories("2.0.0")
    assert results == []


def test_invalid_version_returns_empty():
    results = check_advisories("not-a-version")
    assert results == []


def test_affected_range_boundary():
    results = check_advisories("1.2.3")
    cves = [a["cve_id"] for a in results]
    assert "CVE-2025-0042" in cves
    assert "CVE-2025-0078" in cves
