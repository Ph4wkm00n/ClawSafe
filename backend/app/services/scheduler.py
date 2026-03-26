"""Scheduler service — runs periodic security scans."""

from __future__ import annotations

import asyncio
import json
import logging

from app.services.scanner import get_demo_findings, scan_openclaw
from app.services.scoring import compute_status

logger = logging.getLogger(__name__)

_task: asyncio.Task | None = None
_running = False


async def run_scan() -> None:
    """Execute a scan, store results, and check for drift."""
    from app.db.database import get_db
    from app.services.activity import log_event
    from app.services.notifications import notify_escalation

    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()

    status = compute_status(findings)
    db = await get_db()

    # Get previous scan status
    cursor = await db.execute(
        "SELECT overall_status FROM scans ORDER BY timestamp DESC LIMIT 1"
    )
    prev_row = await cursor.fetchone()
    prev_status = prev_row[0] if prev_row else None

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

    logger.info("Scan complete: status=%s score=%d", status.status.value, status.score)


async def _scan_loop(interval: int) -> None:
    global _running
    while _running:
        try:
            await run_scan()
        except Exception as e:
            logger.error("Scan failed: %s", e)
        await asyncio.sleep(interval)


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
