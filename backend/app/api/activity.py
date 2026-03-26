from fastapi import APIRouter, Query

from app.models.schemas import ActivityList
from app.services.activity import get_recent

router = APIRouter()


@router.get("/activity", response_model=ActivityList)
async def list_activity(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await get_recent(limit=limit, offset=offset)
