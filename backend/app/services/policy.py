"""Policy service — loads, validates, and applies YAML policy files."""

from __future__ import annotations

from pathlib import Path

import yaml

from app.db.database import get_db
from app.models.schemas import PolicyConfig, PolicyResponse, PolicyValidation

POLICIES_DIR = Path("policies")

REQUIRED_SECTIONS = ["network", "tools", "data", "auth"]


def _validate_policy_dict(data: dict) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["Policy must be a YAML mapping."]

    if "version" not in data:
        errors.append("Missing required field: 'version'.")
    if "name" not in data:
        errors.append("Missing required field: 'name'.")

    for section in REQUIRED_SECTIONS:
        if section not in data:
            errors.append(f"Missing required section: '{section}'.")
        elif not isinstance(data[section], dict):
            errors.append(f"Section '{section}' must be a mapping.")

    net = data.get("network", {})
    if isinstance(net, dict):
        bind = net.get("bind_address")
        if bind and not isinstance(bind, str):
            errors.append("network.bind_address must be a string.")

    tools = data.get("tools", {})
    if isinstance(tools, dict):
        rules = tools.get("rules", [])
        if not isinstance(rules, list):
            errors.append("tools.rules must be a list.")
        for i, rule in enumerate(rules):
            if isinstance(rule, dict):
                if "name" not in rule:
                    errors.append(f"tools.rules[{i}] missing 'name'.")
                if "action" in rule and rule["action"] not in ("allow", "ask", "block"):
                    errors.append(f"tools.rules[{i}].action must be 'allow', 'ask', or 'block'.")

    return errors


def load_policy_file(path: str | Path) -> PolicyConfig:
    p = Path(path)
    with open(p) as f:
        data = yaml.safe_load(f) or {}
    return PolicyConfig(**{k: v for k, v in data.items() if k in PolicyConfig.model_fields})


def validate_policy(data: dict) -> PolicyValidation:
    errors = _validate_policy_dict(data)
    return PolicyValidation(valid=len(errors) == 0, errors=errors)


async def get_active_policy() -> PolicyResponse | None:
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, name, content_json, active FROM policies WHERE active = 1 LIMIT 1"
    )
    row = await cursor.fetchone()
    if row is None:
        # Try loading default from disk
        default_path = POLICIES_DIR / "default.yaml"
        if default_path.exists():
            config = load_policy_file(default_path)
            return PolicyResponse(id=None, name=config.name, active=True, config=config)
        return None

    config = PolicyConfig.model_validate_json(row[2])
    return PolicyResponse(id=row[0], name=row[1], active=bool(row[3]), config=config)


async def save_policy(config: PolicyConfig) -> PolicyResponse:
    db = await get_db()
    # Deactivate existing active policies
    await db.execute("UPDATE policies SET active = 0 WHERE active = 1")
    cursor = await db.execute(
        "INSERT INTO policies (name, content_json, active) VALUES (?, ?, 1)",
        (config.name, config.model_dump_json()),
    )
    await db.commit()
    return PolicyResponse(id=cursor.lastrowid, name=config.name, active=True, config=config)
