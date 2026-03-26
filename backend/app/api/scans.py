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
    cursor = await db.execute(
        "SELECT id, timestamp, overall_status, score FROM scans "
        "ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )
    rows = await cursor.fetchall()

    count_cursor = await db.execute("SELECT COUNT(*) FROM scans")
    total = (await count_cursor.fetchone())[0]

    scans = [
        ScanHistoryEntry(id=r[0], timestamp=r[1], overall_status=r[2], score=r[3])
        for r in rows
    ]
    return ScanHistoryList(scans=scans, total=total)
