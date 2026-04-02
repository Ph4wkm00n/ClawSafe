from app.services.dependency_scanner import (
    get_installed_packages,
    scan_dependencies,
    scan_requirements_file,
)


def test_get_installed_packages():
    packages = get_installed_packages()
    assert len(packages) > 0
    assert all("name" in p and "version" in p for p in packages)


def test_scan_dependencies():
    # May or may not find vulns depending on installed versions
    results = scan_dependencies()
    assert isinstance(results, list)


def test_scan_requirements_nonexistent():
    results = scan_requirements_file("/nonexistent/requirements.txt")
    assert results == []
