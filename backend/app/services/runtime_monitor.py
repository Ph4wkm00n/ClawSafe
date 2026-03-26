"""Runtime monitoring — process, network, file integrity, and resource tracking."""

from __future__ import annotations

import hashlib
import logging
import os
import subprocess

logger = logging.getLogger(__name__)


# ── Process Monitoring ──────────────────────────────────────────────────────

def get_process_info(process_name: str = "openclaw") -> dict | None:
    """Get CPU, memory, and file descriptor info for a process."""
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True, timeout=5,
        )
        for line in result.stdout.split("\n"):
            if process_name.lower() in line.lower() and "grep" not in line:
                parts = line.split()
                if len(parts) >= 11:
                    return {
                        "user": parts[0],
                        "pid": int(parts[1]),
                        "cpu_percent": float(parts[2]),
                        "mem_percent": float(parts[3]),
                        "vsz_kb": int(parts[4]),
                        "rss_kb": int(parts[5]),
                        "status": parts[7],
                        "command": " ".join(parts[10:]),
                    }
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass
    return None


# ── Network Connection Tracking ─────────────────────────────────────────────

def get_network_connections(pid: int | None = None) -> list[dict]:
    """Get active network connections (optionally filtered by PID)."""
    connections = []
    try:
        cmd = ["ss", "-tnp"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        for line in result.stdout.split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 5:
                conn = {
                    "state": parts[0],
                    "local_address": parts[3],
                    "remote_address": parts[4],
                }
                if len(parts) > 5:
                    conn["process"] = parts[5] if len(parts) > 5 else ""
                if pid is None or str(pid) in str(conn.get("process", "")):
                    connections.append(conn)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return connections


# ── File Integrity Monitoring ───────────────────────────────────────────────

def compute_file_hash(filepath: str) -> str | None:
    """Compute SHA-256 hash of a file."""
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, IOError):
        return None


def check_file_integrity(file_paths: list[str], known_hashes: dict[str, str]) -> list[dict]:
    """Compare current file hashes against known good hashes."""
    changes = []
    for filepath in file_paths:
        current_hash = compute_file_hash(filepath)
        if current_hash is None:
            changes.append({"file": filepath, "status": "missing", "severity": "high"})
        elif filepath in known_hashes and known_hashes[filepath] != current_hash:
            changes.append({
                "file": filepath,
                "status": "modified",
                "severity": "high",
                "expected_hash": known_hashes[filepath][:16] + "...",
                "current_hash": current_hash[:16] + "...",
            })
    return changes


def baseline_file_hashes(file_paths: list[str]) -> dict[str, str]:
    """Create a baseline of file hashes for integrity monitoring."""
    hashes = {}
    for filepath in file_paths:
        h = compute_file_hash(filepath)
        if h:
            hashes[filepath] = h
    return hashes


# ── Resource Monitoring ─────────────────────────────────────────────────────

def get_resource_usage() -> dict:
    """Get system resource usage (disk, memory)."""
    result = {
        "disk": _get_disk_usage(),
        "memory": _get_memory_info(),
    }
    return result


def _get_disk_usage(path: str = "/") -> dict:
    try:
        stat = os.statvfs(path)
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bfree * stat.f_frsize
        used = total - free
        return {
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "usage_percent": round((used / total) * 100, 1) if total > 0 else 0,
        }
    except OSError:
        return {"total_gb": 0, "used_gb": 0, "free_gb": 0, "usage_percent": 0}


def _get_memory_info() -> dict:
    try:
        with open("/proc/meminfo") as f:
            info = {}
            for line in f:
                parts = line.split()
                if parts[0] in ("MemTotal:", "MemAvailable:", "MemFree:"):
                    info[parts[0].rstrip(":")] = int(parts[1]) * 1024  # Convert KB to bytes
        total = info.get("MemTotal", 0)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        used = total - available
        return {
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "available_gb": round(available / (1024**3), 2),
            "usage_percent": round((used / total) * 100, 1) if total > 0 else 0,
        }
    except (OSError, KeyError):
        return {"total_gb": 0, "used_gb": 0, "available_gb": 0, "usage_percent": 0}


def get_resource_alerts(thresholds: dict | None = None) -> list[dict]:
    """Check resources against thresholds and return alerts."""
    defaults = {"disk_percent": 90, "memory_percent": 90}
    thresh = {**defaults, **(thresholds or {})}
    alerts = []

    resources = get_resource_usage()
    if resources["disk"]["usage_percent"] > thresh["disk_percent"]:
        alerts.append({
            "type": "disk_full",
            "severity": "critical",
            "message": f"Disk usage at {resources['disk']['usage_percent']}% (threshold: {thresh['disk_percent']}%)",
            "value": resources["disk"]["usage_percent"],
        })
    if resources["memory"]["usage_percent"] > thresh["memory_percent"]:
        alerts.append({
            "type": "memory_high",
            "severity": "high",
            "message": f"Memory usage at {resources['memory']['usage_percent']}% (threshold: {thresh['memory_percent']}%)",
            "value": resources["memory"]["usage_percent"],
        })
    return alerts


# ── Combined Runtime Report ─────────────────────────────────────────────────

def get_runtime_report(process_name: str = "openclaw") -> dict:
    """Get a full runtime monitoring report."""
    process = get_process_info(process_name)
    pid = process["pid"] if process else None

    return {
        "process": process,
        "connections": get_network_connections(pid),
        "resources": get_resource_usage(),
        "resource_alerts": get_resource_alerts(),
    }
