from fastapi import APIRouter, Query

from app.services.audit import get_audit_log

router = APIRouter()


@router.get("/audit")
async def list_audit_log(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Get audit trail entries."""
    return await get_audit_log(limit=limit, offset=offset)
