from fastapi import APIRouter

from app.models.schemas import BackupList, FixResult
from app.services.backup import list_backups
from app.services.fixer import apply_fix, undo_fix

router = APIRouter()


@router.post("/fix/{action_id}", response_model=FixResult)
async def post_fix(action_id: str):
    return await apply_fix(action_id)


@router.post("/fix/{action_id}/undo", response_model=FixResult)
async def post_undo(action_id: str):
    return await undo_fix(action_id)


@router.get("/backups", response_model=BackupList)
async def get_backups():
    return await list_backups()
