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
    row = await db.fetch_one(
        "SELECT id, name, content_json, active FROM policies WHERE active = 1 LIMIT 1"
    )
    if row is None:
        # Try loading default from disk
        default_path = POLICIES_DIR / "default.yaml"
        if default_path.exists():
            config = load_policy_file(default_path)
            return PolicyResponse(id=None, name=config.name, active=True, config=config)
        return None

    config = PolicyConfig.model_validate_json(row["content_json"])
    return PolicyResponse(id=row["id"], name=row["name"], active=bool(row["active"]), config=config)


async def save_policy(config: PolicyConfig) -> PolicyResponse:
    db = await get_db()
    # Deactivate existing active policies
    await db.execute("UPDATE policies SET active = 0 WHERE active = 1")
    new_id = await db.insert_returning_id(
        "INSERT INTO policies (name, content_json, active) VALUES (?, ?, 1)",
        (config.name, config.model_dump_json()),
    )
    await db.commit()
    return PolicyResponse(id=new_id, name=config.name, active=True, config=config)


async def get_policy_history(limit: int = 20) -> list[dict]:
    """Get policy version history."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, timestamp, name, active FROM policies ORDER BY timestamp DESC LIMIT ?",
        (limit,),
    )
    return [
        {
            "id": row["id"],
            "timestamp": row["timestamp"],
            "name": row["name"],
            "active": bool(row["active"]),
        }
        for row in rows
    ]


async def export_policy(policy_id: int | None = None) -> str:
    """Export a policy as YAML string. If no ID, exports active policy."""
    import yaml as yaml_lib

    if policy_id is not None:
        db = await get_db()
        row = await db.fetch_one(
            "SELECT content_json FROM policies WHERE id = ?", (policy_id,)
        )
        if row is None:
            raise ValueError("Policy not found.")
        config = PolicyConfig.model_validate_json(row["content_json"])
    else:
        resp = await get_active_policy()
        if resp is None:
            raise ValueError("No active policy.")
        config = resp.config

    return yaml_lib.safe_dump(config.model_dump(), default_flow_style=False)
