from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.schemas import (
    PolicyConfig,
    PolicyResponse,
    PolicySimulationRequest,
    PolicySimulationResult,
    PolicyTemplateResponse,
    PolicyValidation,
)
from fastapi.responses import PlainTextResponse

from app.services.policy import (
    apply_policy_template,
    export_policy,
    get_active_policy,
    get_effective_policy,
    get_policy_history,
    list_policy_templates,
    save_instance_override,
    save_policy,
    simulate_policy,
    validate_policy,
)

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


@router.get("/policy/history")
async def policy_history():
    """Get policy version history."""
    return await get_policy_history()


@router.get("/policy/export")
async def export_policy_yaml():
    """Export active policy as YAML."""
    try:
        yaml_str = await export_policy()
        return PlainTextResponse(content=yaml_str, media_type="text/yaml")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/policy/effective/{instance_id}", response_model=PolicyResponse)
async def get_effective(instance_id: str):
    """Get effective policy for an instance (base + overrides)."""
    policy = await get_effective_policy(instance_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="No active policy found.")
    return policy


@router.put("/policy/{instance_id}", response_model=PolicyResponse, dependencies=[Depends(require_auth)])
async def set_instance_override(instance_id: str, config: PolicyConfig):
    """Set a per-instance policy override."""
    return await save_instance_override(instance_id, config)


@router.post("/policy/simulate", response_model=PolicySimulationResult)
async def simulate_policy_endpoint(req: PolicySimulationRequest):
    """Simulate applying a policy and see the impact on scores."""
    return await simulate_policy(req.policy, req.findings)


@router.get("/policy/templates", response_model=list[PolicyTemplateResponse])
async def get_policy_templates():
    """List available policy templates."""
    return await list_policy_templates()


@router.post("/policy/templates/{template_id}/apply", response_model=PolicyResponse, dependencies=[Depends(require_auth)])
async def apply_template(template_id: int):
    """Apply a policy template as the active policy."""
    try:
        return await apply_policy_template(template_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
