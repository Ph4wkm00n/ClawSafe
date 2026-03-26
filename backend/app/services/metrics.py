"""Metrics service — Prometheus metrics for ClawSafe."""

from __future__ import annotations

from prometheus_client import Counter, Gauge, generate_latest

from app.models.schemas import OverallStatus

# Gauges
risk_score_gauge = Gauge(
    "clawsafe_risk_score",
    "Current risk score per category",
    ["category"],
)
overall_status_gauge = Gauge(
    "clawsafe_overall_status",
    "Overall safety status (0=safe, 1=attention, 2=risk)",
)

# Counters
scan_counter = Counter("clawsafe_scan_count", "Total number of scans performed")
fix_counter = Counter("clawsafe_fix_count", "Total number of fixes applied")

STATUS_MAP = {"safe": 0, "attention": 1, "risk": 2}


def update_metrics(status: OverallStatus) -> None:
    overall_status_gauge.set(STATUS_MAP.get(status.status.value, -1))
    for cat in status.categories:
        risk_score_gauge.labels(category=cat.category.value).set(cat.score)
    scan_counter.inc()


def get_metrics() -> bytes:
    return generate_latest()
