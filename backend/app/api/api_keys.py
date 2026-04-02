"""API routes for API key management."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.schemas import ApiKeyCreate, ApiKeyCreated, ApiKeyResponse

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.get("", response_model=list[ApiKeyResponse])
async def list_keys():
    from app.services.api_keys import list_api_keys
    return await list_api_keys()


@router.post("", response_model=ApiKeyCreated, dependencies=[Depends(require_auth)])
async def create_key(data: ApiKeyCreate):
    from app.services.api_keys import create_api_key
    return await create_api_key(data)


@router.delete("/{key_id}", dependencies=[Depends(require_auth)])
async def revoke_key(key_id: int):
    from app.services.api_keys import revoke_api_key
    if not await revoke_api_key(key_id):
        raise HTTPException(status_code=404, detail="API key not found")
    return {"revoked": True}
