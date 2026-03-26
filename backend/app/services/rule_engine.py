"""Custom rule engine — YAML-based detection rules."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

RULES_DIR = Path("rules")


def _load_rules(rules_dir: Path | None = None) -> list[dict]:
    """Load custom detection rules from YAML files."""
    directory = rules_dir or RULES_DIR
    rules = []
    if not directory.exists():
        return rules

    for rule_file in sorted(directory.glob("*.yaml")):
        try:
            with open(rule_file) as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and "rules" in data:
                    for rule in data["rules"]:
                        rule["source_file"] = str(rule_file)
                        rules.append(rule)
                elif isinstance(data, list):
                    for rule in data:
                        rule["source_file"] = str(rule_file)
                        rules.append(rule)
        except Exception as e:
            logger.warning("Failed to load rules from %s: %s", rule_file, e)

    return rules


def evaluate_rules(config: dict | None, findings: dict) -> list[dict]:
    """Evaluate custom rules against scan findings."""
    rules = _load_rules()
    results = []

    for rule in rules:
        rule_id = rule.get("id", "unknown")
        rule_name = rule.get("name", rule_id)
        severity = rule.get("severity", "medium")
        condition = rule.get("condition", {})

        triggered = _evaluate_condition(condition, config, findings)
        if triggered:
            results.append({
                "rule_id": rule_id,
                "name": rule_name,
                "severity": severity,
                "description": rule.get("description", ""),
                "remediation": rule.get("remediation", ""),
                "source": rule.get("source_file", ""),
            })

    return results


def _evaluate_condition(condition: dict, config: dict | None, findings: dict) -> bool:
    """Evaluate a single rule condition against config/findings."""
    if not condition or not isinstance(condition, dict):
        return False

    condition.get("type", "")
    field = condition.get("field", "")
    operator = condition.get("operator", "equals")
    value = condition.get("value")

    # Get the actual value from config or findings
    actual = _get_nested_value(config or {}, field) or _get_nested_value(findings, field)
    if actual is None:
        return False

    if operator == "equals":
        return actual == value
    elif operator == "not_equals":
        return actual != value
    elif operator == "contains":
        return value in str(actual)
    elif operator == "greater_than":
        return float(actual) > float(value)
    elif operator == "less_than":
        return float(actual) < float(value)
    elif operator == "matches":
        return bool(re.search(str(value), str(actual)))
    elif operator == "exists":
        return actual is not None
    elif operator == "in_list":
        return actual in (value if isinstance(value, list) else [value])

    return False


def _get_nested_value(data: dict, field: str):
    """Get a nested value using dot notation (e.g., 'network.bind_address')."""
    keys = field.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current
