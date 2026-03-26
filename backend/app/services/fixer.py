"""Fixer service — applies auto-fix actions to OpenClaw configuration."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from app.core.config import settings
from app.models.schemas import FixResult
from app.services.activity import log_event
from app.services.backup import create_backup, restore_backup
from app.services.metrics import fix_counter

logger = logging.getLogger(__name__)


async def _load_config() -> dict:
    path = Path(settings.openclaw_config_path)
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        logger.error("Failed to load config: %s", e)
        return {}


async def _save_config(config: dict) -> None:
    path = Path(settings.openclaw_config_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)
    except OSError as e:
        logger.error("Failed to save config: %s", e)
        raise


async def _fix_network_binding(config: dict) -> str:
    config["bind_address"] = "127.0.0.1"
    config["host"] = "127.0.0.1"
    return "Bound OpenClaw to localhost (127.0.0.1)."


async def _fix_tools_policy(config: dict) -> str:
    skills = config.get("skills", config.get("tools", []))
    if not isinstance(skills, list):
        skills = []
    disabled = []
    for skill in skills:
        if isinstance(skill, dict) and skill.get("risk") in ("high", "critical"):
            skill["enabled"] = False
            disabled.append(skill.get("name", "unknown"))
    if "skills" in config:
        config["skills"] = skills
    elif "tools" in config:
        config["tools"] = skills
    return f"Disabled high-risk skills: {', '.join(disabled) or 'none found'}."


async def _fix_data_mounts(config: dict) -> str:
    mounts = config.get("mounts", config.get("volumes", []))
    if not isinstance(mounts, list):
        mounts = []
    sensitive = {"/", "/etc", "/root", "/home"}
    safe_mounts = [m for m in mounts if not (isinstance(m, str) and m.rstrip("/") in sensitive)]
    if "mounts" in config:
        config["mounts"] = safe_mounts
    elif "volumes" in config:
        config["volumes"] = safe_mounts
    removed = len(mounts) - len(safe_mounts)
    return f"Removed {removed} broad mount(s). {len(safe_mounts)} safe mount(s) remain."


async def _fix_auth(config: dict) -> str:
    if not isinstance(config.get("auth"), dict):
        config["auth"] = {}
    config["auth"]["enabled"] = True
    config["auth"]["method"] = "token"
    return "Enabled token authentication."


FIX_HANDLERS = {
    "fix_network_binding": _fix_network_binding,
    "fix_tools_policy": _fix_tools_policy,
    "fix_data_mounts": _fix_data_mounts,
    "fix_auth": _fix_auth,
    "fix_updates": None,  # Updates are manual only
}


async def apply_fix(action_id: str) -> FixResult:
    handler = FIX_HANDLERS.get(action_id)
    if handler is None:
        return FixResult(
            success=False,
            action_id=action_id,
            message=f"No auto-fix available for '{action_id}'.",
        )

    try:
        backup_id = await create_backup(settings.openclaw_config_path, action_id)
        config = await _load_config()
        message = await handler(config)
        await _save_config(config)
        await log_event("fix_applied", f"Auto-fix applied: {action_id}", "safe")
        fix_counter.inc()
        logger.info("Fix applied: %s", action_id)
        return FixResult(
            success=True,
            action_id=action_id,
            message=message,
            backup_id=backup_id,
        )
    except Exception as e:
        logger.error("Fix failed for %s: %s", action_id, e)
        await log_event("fix_failed", f"Auto-fix failed: {action_id} — {e}", "risk")
        return FixResult(
            success=False,
            action_id=action_id,
            message=f"Fix failed: {e}",
        )


async def undo_fix(action_id: str) -> FixResult:
    from app.db.database import get_db

    db = await get_db()
    cursor = await db.execute(
        "SELECT id FROM backups WHERE action_id = ? AND status = 'active' "
        "ORDER BY timestamp DESC LIMIT 1",
        (action_id,),
    )
    row = await cursor.fetchone()
    if row is None:
        return FixResult(
            success=False,
            action_id=action_id,
            message="No backup found to restore.",
        )

    success = await restore_backup(row[0])
    if success:
        await log_event("fix_undone", f"Undid fix: {action_id}", "safe")
        return FixResult(success=True, action_id=action_id, message="Fix undone. Previous config restored.")

    return FixResult(success=False, action_id=action_id, message="Failed to restore backup.")
