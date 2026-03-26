"""Secrets scanner — detects leaked credentials in config files and environment."""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Patterns for common secret types
SECRET_PATTERNS = [
    {"name": "AWS Access Key", "pattern": r"AKIA[0-9A-Z]{16}", "severity": "critical"},
    {"name": "AWS Secret Key", "pattern": r"(?i)aws_secret_access_key\s*[=:]\s*[A-Za-z0-9/+=]{40}", "severity": "critical"},
    {"name": "GitHub Token", "pattern": r"gh[ps]_[A-Za-z0-9_]{36,}", "severity": "critical"},
    {"name": "Generic API Key", "pattern": r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{20,}['\"]?", "severity": "high"},
    {"name": "Generic Secret", "pattern": r"(?i)(secret|password|passwd|pwd)\s*[=:]\s*['\"]?[^\s'\"]{8,}['\"]?", "severity": "high"},
    {"name": "Private Key Header", "pattern": r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "severity": "critical"},
    {"name": "JWT Token", "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "severity": "high"},
    {"name": "Slack Token", "pattern": r"xox[bpors]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}", "severity": "critical"},
    {"name": "Database URL with Password", "pattern": r"(?i)(postgres|mysql|mongodb)://[^:]+:[^@]+@", "severity": "high"},
    {"name": "Bearer Token in Config", "pattern": r"(?i)bearer\s+[A-Za-z0-9_\-.]{20,}", "severity": "high"},
]

# Files to skip
SKIP_EXTENSIONS = {".pyc", ".pyo", ".so", ".dll", ".exe", ".bin", ".jpg", ".png", ".gif", ".ico"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".next", "venv", ".venv"}


def scan_file_for_secrets(filepath: str) -> list[dict]:
    """Scan a single file for secret patterns."""
    findings = []
    path = Path(filepath)

    if path.suffix in SKIP_EXTENSIONS:
        return []

    try:
        content = path.read_text(errors="ignore")
    except (OSError, UnicodeDecodeError):
        return []

    for pattern_def in SECRET_PATTERNS:
        matches = re.finditer(pattern_def["pattern"], content)
        for match in matches:
            # Find line number
            line_num = content[:match.start()].count("\n") + 1
            # Redact the actual secret value
            matched = match.group()
            redacted = matched[:10] + "..." + matched[-4:] if len(matched) > 20 else matched[:6] + "***"

            findings.append({
                "file": str(path),
                "line": line_num,
                "type": pattern_def["name"],
                "severity": pattern_def["severity"],
                "match": redacted,
            })

    return findings


def scan_directory_for_secrets(directory: str, max_files: int = 500) -> dict:
    """Scan a directory tree for secrets."""
    all_findings = []
    files_scanned = 0

    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if files_scanned >= max_files:
                break
            filepath = os.path.join(root, fname)
            findings = scan_file_for_secrets(filepath)
            all_findings.extend(findings)
            files_scanned += 1

    critical = sum(1 for f in all_findings if f["severity"] == "critical")
    high = sum(1 for f in all_findings if f["severity"] == "high")

    return {
        "files_scanned": files_scanned,
        "total_findings": len(all_findings),
        "critical_count": critical,
        "high_count": high,
        "findings": all_findings,
    }


def scan_environment_for_secrets() -> list[dict]:
    """Check environment variables for potentially leaked secrets."""
    findings = []
    sensitive_vars = ["PASSWORD", "SECRET", "TOKEN", "KEY", "CREDENTIAL", "PRIVATE"]

    for key, value in os.environ.items():
        if any(s in key.upper() for s in sensitive_vars):
            if value and len(value) > 3:
                findings.append({
                    "variable": key,
                    "severity": "info",
                    "note": "Contains potentially sensitive data (expected for config, verify not leaked)",
                    "value_length": len(value),
                })

    return findings
