from fastapi import APIRouter
from pydantic import BaseModel

from app.models.schemas import NotificationConfig
from app.services.notifications import load_config, save_config, send_test_notification

router = APIRouter()


@router.get("/settings/notifications", response_model=NotificationConfig)
async def get_notification_config():
    return await load_config()


@router.put("/settings/notifications", response_model=NotificationConfig)
async def update_notification_config(config: NotificationConfig):
    await save_config(config)
    return config


class TestWebhookRequest(BaseModel):
    url: str


class TestWebhookResponse(BaseModel):
    success: bool


@router.post("/settings/notifications/test", response_model=TestWebhookResponse)
async def test_notification(req: TestWebhookRequest):
    success = await send_test_notification(req.url)
    return TestWebhookResponse(success=success)
