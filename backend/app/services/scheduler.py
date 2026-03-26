"""Scheduler service — runs periodic security scans with backoff."""

from __future__ import annotations

import asyncio
import json
import logging
import time

from app.services.metrics import record_error, record_scan_duration, update_metrics
from app.services.scanner import get_demo_findings, scan_openclaw
from app.services.scoring import compute_status

logger = logging.getLogger(__name__)

_task: asyncio.Task | None = None
_running = False
_consecutive_failures = 0
MAX_BACKOFF_MULTIPLIER = 4


def is_scheduler_running() -> bool:
    return _running and _task is not None and not _task.done()


async def run_scan() -> None:
    """Execute a scan, store results, update metrics, and check for drift."""
    global _consecutive_failures

    from app.db.database import get_db
    from app.services.activity import log_event
    from app.services.notifications import notify_escalation

    scan_start = time.perf_counter()
    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()

    status = compute_status(findings)
    update_metrics(status)

    db = await get_db()

    # Get previous scan status
    prev_row = await db.fetch_one(
        "SELECT overall_status FROM scans ORDER BY timestamp DESC LIMIT 1"
    )
    prev_status = prev_row["overall_status"] if prev_row else None

    # Store new scan
    await db.execute(
        "INSERT INTO scans (overall_status, score, results_json) VALUES (?, ?, ?)",
        (status.status.value, status.score, json.dumps(findings)),
    )
    await db.commit()

    # Log if status changed
    if prev_status and prev_status != status.status.value:
        await log_event(
            "status_change",
            f"Safety status changed from {prev_status} to {status.status.value}",
            status.status.value,
        )
        await notify_escalation(prev_status, status.status.value)

    scan_duration = time.perf_counter() - scan_start
    record_scan_duration(scan_duration)
    _consecutive_failures = 0
    logger.info("Scan complete: status=%s score=%d duration=%.2fs", status.status.value, status.score, scan_duration)

    # Emit event for WebSocket broadcast
    from app.services.event_bus import emit
    await emit("scan_complete", {"status": status.status.value, "score": status.score})


async def _scan_loop(interval: int) -> None:
    global _running, _consecutive_failures
    while _running:
        try:
            await run_scan()
        except Exception as e:
            _consecutive_failures += 1
            record_error("scan_failure")
            logger.error("Scan failed (attempt %d): %s", _consecutive_failures, e)

        # Exponential backoff on failures, capped at MAX_BACKOFF_MULTIPLIER * interval
        backoff = min(2**_consecutive_failures, MAX_BACKOFF_MULTIPLIER) if _consecutive_failures > 0 else 1
        sleep_time = interval * backoff
        logger.debug("Next scan in %ds (backoff=%dx)", sleep_time, backoff)
        await asyncio.sleep(sleep_time)


async def start_scheduler(interval: int = 3600) -> None:
    """Start the background scan loop."""
    global _task, _running
    _running = True
    _task = asyncio.create_task(_scan_loop(interval))
    logger.info("Scheduler started (interval=%ds)", interval)


async def stop_scheduler() -> None:
    """Stop the background scan loop."""
    global _task, _running
    _running = False
    if _task:
        _task.cancel()
        try:
            await _task
        except asyncio.CancelledError:
            pass
        _task = None
    logger.info("Scheduler stopped")
