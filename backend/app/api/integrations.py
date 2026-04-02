"""API routes for native integrations (PagerDuty, Jira, GitHub)."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.schemas import IntegrationConfig

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("", response_model=IntegrationConfig)
async def get_integrations():
    from app.services.integrations import load_integration_config
    return await load_integration_config()


@router.put("", response_model=IntegrationConfig, dependencies=[Depends(require_auth)])
async def update_integrations(config: IntegrationConfig):
    from app.services.integrations import save_integration_config
    return await save_integration_config(config)


@router.post("/test/{service}", dependencies=[Depends(require_auth)])
async def test_integration(service: str):
    from app.services.integrations import test_integration
    result = await test_integration(service)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
