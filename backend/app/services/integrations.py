"""Native integrations service — PagerDuty, Jira, GitHub Issues."""

from __future__ import annotations

import logging

import httpx

from app.db.database import get_db
from app.models.schemas import IntegrationConfig

logger = logging.getLogger(__name__)

SETTINGS_KEY = "integration_config"


async def load_integration_config() -> IntegrationConfig:
    """Load integration config from settings."""
    db = await get_db()
    row = await db.fetch_one("SELECT value FROM settings WHERE key = ?", (SETTINGS_KEY,))
    if row is None:
        return IntegrationConfig()
    return IntegrationConfig.model_validate_json(row["value"])


async def save_integration_config(config: IntegrationConfig) -> IntegrationConfig:
    """Save integration config."""
    db = await get_db()
    await db.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (SETTINGS_KEY, config.model_dump_json()),
    )
    await db.commit()
    return config


async def send_pagerduty(routing_key: str, summary: str, severity: str = "warning") -> bool:
    """Create a PagerDuty incident via Events API v2."""
    payload = {
        "routing_key": routing_key,
        "event_action": "trigger",
        "payload": {
            "summary": summary,
            "severity": severity,
            "source": "ClawSafe",
        },
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                "https://events.pagerduty.com/v2/enqueue",
                json=payload,
            )
            return resp.status_code < 400
    except Exception as e:
        logger.error("PagerDuty send failed: %s", e)
        return False


async def send_jira_issue(
    url: str, project: str, email: str, token: str, summary: str, description: str
) -> bool:
    """Create a Jira issue via REST API."""
    payload = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
        }
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{url.rstrip('/')}/rest/api/2/issue",
                json=payload,
                auth=(email, token),
            )
            return resp.status_code < 400
    except Exception as e:
        logger.error("Jira issue creation failed: %s", e)
        return False


async def send_github_issue(repo: str, token: str, title: str, body: str) -> bool:
    """Create a GitHub issue via GitHub API."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"https://api.github.com/repos/{repo}/issues",
                json={"title": title, "body": body},
                headers={
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            )
            return resp.status_code < 400
    except Exception as e:
        logger.error("GitHub issue creation failed: %s", e)
        return False


async def notify_integrations(event_type: str, message: str, severity: str = "warning") -> None:
    """Send notifications to all enabled integrations."""
    config = await load_integration_config()

    if "pagerduty" in config.enabled_integrations and config.pagerduty_routing_key:
        await send_pagerduty(config.pagerduty_routing_key, message, severity)

    if "jira" in config.enabled_integrations and config.jira_url:
        await send_jira_issue(
            config.jira_url, config.jira_project, config.jira_email,
            config.jira_token, f"ClawSafe: {event_type}", message,
        )

    if "github" in config.enabled_integrations and config.github_repo:
        await send_github_issue(
            config.github_repo, config.github_token,
            f"ClawSafe Alert: {event_type}", message,
        )


async def test_integration(service: str) -> dict:
    """Test connectivity to an integration service."""
    config = await load_integration_config()

    if service == "pagerduty":
        if not config.pagerduty_routing_key:
            return {"success": False, "message": "PagerDuty routing key not configured"}
        ok = await send_pagerduty(config.pagerduty_routing_key, "ClawSafe test notification", "info")
        return {"success": ok, "message": "PagerDuty test sent" if ok else "PagerDuty send failed"}

    if service == "jira":
        if not config.jira_url:
            return {"success": False, "message": "Jira URL not configured"}
        return {"success": True, "message": "Jira configuration present (dry-run only)"}

    if service == "github":
        if not config.github_repo:
            return {"success": False, "message": "GitHub repo not configured"}
        return {"success": True, "message": "GitHub configuration present (dry-run only)"}

    return {"success": False, "message": f"Unknown integration: {service}"}
