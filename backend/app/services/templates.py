"""Template service — Jinja2-based notification templates."""

from __future__ import annotations

import logging

from jinja2 import BaseLoader, Environment, TemplateSyntaxError

from app.db.database import get_db
from app.models.schemas import NotificationTemplate, NotificationTemplateCreate

logger = logging.getLogger(__name__)

_jinja_env = Environment(loader=BaseLoader(), autoescape=True)


async def list_templates() -> list[NotificationTemplate]:
    """List all notification templates."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, name, channel, template_text, created_at "
        "FROM notification_templates ORDER BY name"
    )
    return [
        NotificationTemplate(
            id=row["id"],
            name=row["name"],
            channel=row["channel"],
            template_text=row["template_text"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


async def get_template(name: str) -> NotificationTemplate | None:
    """Get a template by name."""
    db = await get_db()
    row = await db.fetch_one(
        "SELECT id, name, channel, template_text, created_at "
        "FROM notification_templates WHERE name = ?",
        (name,),
    )
    if row is None:
        return None
    return NotificationTemplate(
        id=row["id"],
        name=row["name"],
        channel=row["channel"],
        template_text=row["template_text"],
        created_at=row["created_at"],
    )


async def create_template(data: NotificationTemplateCreate) -> NotificationTemplate:
    """Create a new notification template."""
    # Validate template syntax
    try:
        _jinja_env.parse(data.template_text)
    except TemplateSyntaxError as e:
        raise ValueError(f"Invalid template syntax: {e}") from e

    db = await get_db()
    tid = await db.insert_returning_id(
        "INSERT INTO notification_templates (name, channel, template_text) VALUES (?, ?, ?)",
        (data.name, data.channel, data.template_text),
    )
    await db.commit()
    return NotificationTemplate(id=tid, name=data.name, channel=data.channel, template_text=data.template_text)


async def delete_template(name: str) -> bool:
    """Delete a template by name."""
    db = await get_db()
    existing = await get_template(name)
    if existing is None:
        return False
    await db.execute("DELETE FROM notification_templates WHERE name = ?", (name,))
    await db.commit()
    return True


def render_notification(template_text: str, context: dict) -> str:
    """Render a notification template with the given context."""
    try:
        tmpl = _jinja_env.from_string(template_text)
        return tmpl.render(**context)
    except Exception as e:
        logger.error("Template render failed: %s", e)
        return context.get("message", str(e))
