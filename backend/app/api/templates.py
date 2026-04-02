"""API routes for notification templates."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.schemas import NotificationTemplate, NotificationTemplateCreate
from app.services.templates import (
    create_template,
    delete_template,
    get_template,
    list_templates,
    render_notification,
)

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("", response_model=list[NotificationTemplate])
async def get_templates():
    return await list_templates()


@router.get("/{name}", response_model=NotificationTemplate)
async def get_template_by_name(name: str):
    tmpl = await get_template(name)
    if tmpl is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return tmpl


@router.post("", response_model=NotificationTemplate, dependencies=[Depends(require_auth)])
async def create_new_template(data: NotificationTemplateCreate):
    try:
        return await create_template(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{name}", dependencies=[Depends(require_auth)])
async def delete_template_by_name(name: str):
    if not await delete_template(name):
        raise HTTPException(status_code=404, detail="Template not found")
    return {"deleted": True}


@router.post("/render")
async def render_template_preview(name: str, context: dict):
    tmpl = await get_template(name)
    if tmpl is None:
        raise HTTPException(status_code=404, detail="Template not found")
    rendered = render_notification(tmpl.template_text, context)
    return {"rendered": rendered}
