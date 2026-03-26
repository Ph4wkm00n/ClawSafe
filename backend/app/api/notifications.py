from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.auth import require_auth
from app.models.schemas import NotificationConfig
from app.services.notifications import (
    load_config,
    save_config,
    send_test_notification,
    validate_webhook_url,
)

router = APIRouter()


@router.get("/settings/notifications", response_model=NotificationConfig)
async def get_notification_config():
    return await load_config()


@router.put("/settings/notifications", response_model=NotificationConfig, dependencies=[Depends(require_auth)])
async def update_notification_config(config: NotificationConfig):
    for webhook in config.webhooks:
        error = validate_webhook_url(webhook.url)
        if error:
            raise HTTPException(status_code=400, detail=f"Invalid webhook URL '{webhook.url}': {error}")
    await save_config(config)
    return config


class TestWebhookRequest(BaseModel):
    url: str


class TestWebhookResponse(BaseModel):
    success: bool


@router.post("/settings/notifications/test", response_model=TestWebhookResponse, dependencies=[Depends(require_auth)])
async def test_notification(req: TestWebhookRequest):
    error = validate_webhook_url(req.url)
    if error:
        raise HTTPException(status_code=400, detail=error)
    success = await send_test_notification(req.url)
    return TestWebhookResponse(success=success)
