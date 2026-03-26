"""Metrics service — Prometheus metrics for ClawSafe."""

from __future__ import annotations


from prometheus_client import Counter, Gauge, Histogram, generate_latest

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
error_counter = Counter(
    "clawsafe_errors_total",
    "Total errors by type",
    ["error_type"],
)
notification_counter = Counter(
    "clawsafe_notifications_total",
    "Notifications sent by channel",
    ["channel", "status"],
)

# Histograms
request_latency = Histogram(
    "clawsafe_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint", "status_code"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)
scan_duration = Histogram(
    "clawsafe_scan_duration_seconds",
    "Time taken to complete a security scan",
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
)

STATUS_MAP = {"safe": 0, "attention": 1, "risk": 2}


def update_metrics(status: OverallStatus) -> None:
    overall_status_gauge.set(STATUS_MAP.get(status.status.value, -1))
    for cat in status.categories:
        risk_score_gauge.labels(category=cat.category.value).set(cat.score)
    scan_counter.inc()


def record_scan_duration(duration_seconds: float) -> None:
    scan_duration.observe(duration_seconds)


def record_error(error_type: str) -> None:
    error_counter.labels(error_type=error_type).inc()


def record_notification(channel: str, success: bool) -> None:
    notification_counter.labels(channel=channel, status="success" if success else "failure").inc()


def get_metrics() -> bytes:
    return generate_latest()
