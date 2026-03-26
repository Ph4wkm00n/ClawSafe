from fastapi import APIRouter

from app.db.database import db_health_check
from app.services.scheduler import is_scheduler_running

router = APIRouter()


@router.get("/health")
async def health_check():
    db_ok = await db_health_check()
    scheduler_ok = is_scheduler_running()

    checks = {
        "database": "ok" if db_ok else "error",
        "scheduler": "ok" if scheduler_ok else "stopped",
    }
    from app.models.schemas import HealthResponse

    return {
        "status": "ok" if db_ok else "degraded",
        "version": HealthResponse().version,
        "checks": checks,
    }
