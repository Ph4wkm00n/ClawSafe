from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse

from app.core.auth import require_auth
from app.services.data_management import (
    create_db_backup,
    export_activity,
    export_scans,
    purge_old_data,
)

router = APIRouter()


@router.post("/data/purge", dependencies=[Depends(require_auth)])
async def purge_data(retention_days: int = Query(default=90, ge=1)):
    """Delete scans and activity older than retention_days."""
    return await purge_old_data(retention_days)


@router.post("/data/backup", dependencies=[Depends(require_auth)])
async def backup_database():
    """Create a backup of the database."""
    try:
        path = await create_db_backup()
        return {"success": True, "backup_path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/data/export/scans")
async def export_scans_endpoint(format: str = Query(default="json", pattern="^(json|csv)$")):
    """Export scan history as JSON or CSV."""
    data = await export_scans(format)
    media = "text/csv" if format == "csv" else "application/json"
    return PlainTextResponse(content=data, media_type=media)


@router.get("/data/export/activity")
async def export_activity_endpoint(format: str = Query(default="json", pattern="^(json|csv)$")):
    """Export activity events as JSON or CSV."""
    data = await export_activity(format)
    media = "text/csv" if format == "csv" else "application/json"
    return PlainTextResponse(content=data, media_type=media)
