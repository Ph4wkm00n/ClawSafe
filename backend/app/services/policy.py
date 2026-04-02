"""Policy service — loads, validates, and applies YAML policy files."""

from __future__ import annotations

import copy
from pathlib import Path

import yaml

from app.db.database import get_db
from app.models.schemas import (
    PolicyConfig,
    PolicyResponse,
    PolicySimulationResult,
    PolicyTemplateResponse,
    PolicyValidation,
)

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


# ── Policy Inheritance ────────────────────────────────────────────────────


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dicts. Override values take precedence."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def merge_policies(base: PolicyConfig, override: PolicyConfig) -> PolicyConfig:
    """Merge a base policy with per-instance overrides."""
    base_dict = base.model_dump()
    override_dict = {k: v for k, v in override.model_dump().items() if v}
    merged = _deep_merge(base_dict, override_dict)
    return PolicyConfig(**merged)


async def get_effective_policy(instance_id: str | None = None) -> PolicyResponse | None:
    """Get effective policy for an instance (base + instance override merged)."""
    base = await get_active_policy()
    if base is None or instance_id is None:
        return base

    db = await get_db()
    row = await db.fetch_one(
        "SELECT content_json FROM policies WHERE name = ? AND active = 0 ORDER BY timestamp DESC LIMIT 1",
        (f"override_{instance_id}",),
    )
    if row is None:
        return base

    override_config = PolicyConfig.model_validate_json(row["content_json"])
    merged = merge_policies(base.config, override_config)
    return PolicyResponse(id=base.id, name=base.name, active=True, config=merged)


async def save_instance_override(instance_id: str, config: PolicyConfig) -> PolicyResponse:
    """Save a per-instance policy override."""
    db = await get_db()
    config_with_name = config.model_copy(update={"name": f"override_{instance_id}"})
    new_id = await db.insert_returning_id(
        "INSERT INTO policies (name, content_json, active) VALUES (?, ?, 0)",
        (config_with_name.name, config_with_name.model_dump_json()),
    )
    await db.commit()
    return PolicyResponse(id=new_id, name=config_with_name.name, active=False, config=config_with_name)


# ── Policy Simulation ────────────────────────────────────────────────────


async def simulate_policy(policy_dict: dict, findings: dict | None = None) -> PolicySimulationResult:
    """Simulate what would happen if a policy were activated."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.scoring import compute_status

    if findings is None:
        findings = scan_openclaw()
        if not findings.get("openclaw_detected"):
            findings = get_demo_findings()

    # Current status (with active policy)
    active = await get_active_policy()
    active_dict = active.config.model_dump() if active else None
    current = compute_status(findings, active_dict)

    # Simulated status (with proposed policy)
    simulated = compute_status(findings, policy_dict)

    changes = []
    for cur_cat, sim_cat in zip(current.categories, simulated.categories):
        if cur_cat.score != sim_cat.score or cur_cat.status != sim_cat.status:
            changes.append({
                "category": cur_cat.category.value,
                "current_score": cur_cat.score,
                "simulated_score": sim_cat.score,
                "current_status": cur_cat.status.value,
                "simulated_status": sim_cat.status.value,
            })

    return PolicySimulationResult(
        current_score=current.score,
        simulated_score=simulated.score,
        current_status=current.status.value,
        simulated_status=simulated.status.value,
        category_changes=changes,
    )


# ── Policy Templates ─────────────────────────────────────────────────────


async def list_policy_templates() -> list[PolicyTemplateResponse]:
    """List all available policy templates."""
    db = await get_db()
    rows = await db.fetch_all(
        "SELECT id, name, description, content_json, category FROM policy_templates ORDER BY name"
    )
    return [
        PolicyTemplateResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            category=row["category"],
            config=PolicyConfig.model_validate_json(row["content_json"]),
        )
        for row in rows
    ]


async def get_policy_template(template_id: int) -> PolicyTemplateResponse | None:
    """Get a policy template by ID."""
    db = await get_db()
    row = await db.fetch_one(
        "SELECT id, name, description, content_json, category FROM policy_templates WHERE id = ?",
        (template_id,),
    )
    if row is None:
        return None
    return PolicyTemplateResponse(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        category=row["category"],
        config=PolicyConfig.model_validate_json(row["content_json"]),
    )


async def apply_policy_template(template_id: int) -> PolicyResponse:
    """Apply a policy template as the active policy."""
    tmpl = await get_policy_template(template_id)
    if tmpl is None:
        raise ValueError("Template not found")
    return await save_policy(tmpl.config)
