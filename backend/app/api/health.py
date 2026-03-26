from fastapi import APIRouter

from app.db.database import db_health_check
from app.services.scheduler import is_scheduler_running
from app.services.scanner import _check_openclaw_reachable

router = APIRouter()


@router.get("/health")
async def health_check():
    db_ok = await db_health_check()
    scheduler_ok = is_scheduler_running()
    openclaw_ok = _check_openclaw_reachable()

    checks = {
        "database": "ok" if db_ok else "error",
        "scheduler": "ok" if scheduler_ok else "stopped",
        "openclaw": "ok" if openclaw_ok else "unreachable",
    }
    all_ok = db_ok  # DB is critical; OpenClaw being unreachable is informational

    from app.models.schemas import HealthResponse

    return {
        "status": "ok" if all_ok else "degraded",
        "version": HealthResponse().version,
        "checks": checks,
    }
