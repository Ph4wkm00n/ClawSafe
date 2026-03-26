from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.schemas import PolicyConfig, PolicyResponse, PolicyValidation
from app.services.policy import get_active_policy, save_policy, validate_policy

router = APIRouter()


@router.get("/policy", response_model=PolicyResponse)
async def get_policy():
    policy = await get_active_policy()
    if policy is None:
        raise HTTPException(status_code=404, detail="No active policy found.")
    return policy


@router.put("/policy", response_model=PolicyResponse, dependencies=[Depends(require_auth)])
async def update_policy(config: PolicyConfig):
    validation = validate_policy(config.model_dump())
    if not validation.valid:
        raise HTTPException(status_code=422, detail=validation.errors)
    return await save_policy(config)


@router.post("/policy/validate", response_model=PolicyValidation)
async def validate_policy_endpoint(config: PolicyConfig):
    return validate_policy(config.model_dump())
