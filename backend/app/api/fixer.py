from fastapi import APIRouter, Depends

from app.core.auth import require_auth, validate_action_id
from app.models.schemas import BackupList, FixResult
from app.services.backup import list_backups
from app.services.fixer import apply_fix, undo_fix

router = APIRouter()


@router.post("/fix/{action_id}", response_model=FixResult, dependencies=[Depends(require_auth)])
async def post_fix(action_id: str):
    validate_action_id(action_id)
    return await apply_fix(action_id)


@router.post("/fix/{action_id}/undo", response_model=FixResult, dependencies=[Depends(require_auth)])
async def post_undo(action_id: str):
    validate_action_id(action_id)
    return await undo_fix(action_id)


@router.get("/backups", response_model=BackupList)
async def get_backups():
    return await list_backups()
