from fastapi import APIRouter, Query

from app.db.database import get_db
from app.models.schemas import ScanHistoryEntry, ScanHistoryList

router = APIRouter()


@router.get("/scans", response_model=ScanHistoryList)
async def list_scans(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, timestamp, overall_status, score FROM scans "
        "ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )

    total = await db.fetch_scalar("SELECT COUNT(*) FROM scans") or 0

    scans = [
        ScanHistoryEntry(
            id=r["id"],
            timestamp=r["timestamp"],
            overall_status=r["overall_status"],
            score=r["score"],
        )
        for r in rows
    ]
    return ScanHistoryList(scans=scans, total=total)
