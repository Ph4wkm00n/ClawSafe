# API Reference

Base URL: `http://localhost:8000`

Full interactive docs: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Write endpoints (PUT, POST) require an API key when `CLAWSAFE_API_KEY` is set:

```
Authorization: Bearer your-api-key
```

Read endpoints (GET) do not require authentication.

---

## Health

### `GET /api/v1/health`

Checks database connectivity and scheduler status.

**Response (200):**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "checks": {
    "database": "ok",
    "scheduler": "ok"
  }
}
```

Returns `"status": "degraded"` with HTTP 503 if any check fails.

---

## Status

### `GET /api/v1/status`

Overall safety status with all four categories. Risk scores are adjusted by the active policy.

**Response:**
```json
{
  "status": "risk",
  "score": 70,
  "subtitle": "Important risks found. Please review these now.",
  "categories": [
    {
      "category": "network",
      "label": "Network",
      "status": "risk",
      "score": 90,
      "summary": "People outside your home can reach OpenClaw.",
      "description": "OpenClaw is exposed on all interfaces without authentication.",
      "action_label": "Make it private",
      "action_id": "fix_network_binding"
    }
  ]
}
```

### `GET /api/v1/status/{category}`

Single category detail. Categories: `network`, `tools`, `data`, `updates`.

---

## Recommendations

### `GET /api/v1/recommendations`

Suggested actions for current risks. Only returns recommendations for non-safe categories.

**Response:**
```json
[
  {
    "id": "fix_network_binding",
    "title": "Make OpenClaw Private",
    "description": "People outside your home can reach your AI right now.",
    "category": "network",
    "severity": "risk",
    "action_label": "Make it private",
    "steps": ["Open your terminal", "Edit the OpenClaw config file", "..."],
    "commands": ["sudo nano /etc/openclaw/config.yaml", "..."]
  }
]
```

---

## Activity

### `GET /api/v1/activity?limit=20&offset=0`

Paginated activity event log.

**Response:**
```json
{
  "events": [
    {
      "id": 1,
      "timestamp": "2026-03-26 12:00:00",
      "event_type": "fix_applied",
      "description": "Auto-fix applied: fix_network_binding",
      "severity": "safe"
    }
  ],
  "total": 42
}
```

---

## Settings

### `GET /api/v1/settings`

User preferences (theme, onboarding status, etc.).

### `PUT /api/v1/settings` 🔒

Update user preferences. Requires auth.

**Request body:**
```json
{
  "onboarding_complete": true,
  "theme": "playful",
  "mode": "dark",
  "usage_type": "home",
  "network_preference": "private"
}
```

---

## Fix Engine

### `POST /api/v1/fix/{action_id}` 🔒

Apply an auto-fix. Requires auth. Creates a config backup before applying.

Valid action IDs: `fix_network_binding`, `fix_tools_policy`, `fix_data_mounts`, `fix_auth`.

**Response:**
```json
{
  "success": true,
  "action_id": "fix_network_binding",
  "message": "Bound OpenClaw to localhost (127.0.0.1).",
  "backup_id": 3
}
```

### `POST /api/v1/fix/{action_id}/undo` 🔒

Undo the most recent fix for this action. Restores from backup.

### `GET /api/v1/backups`

List all config backups (auto-cleaned at 50 max).

---

## Policy

### `GET /api/v1/policy`

Active policy configuration.

### `PUT /api/v1/policy` 🔒

Update and activate a policy. Validated before saving.

### `POST /api/v1/policy/validate`

Validate a policy configuration without applying. Returns validation errors.

**Response:**
```json
{
  "valid": false,
  "errors": ["tools.rules[0] missing 'name'."]
}
```

---

## Scan History

### `GET /api/v1/scans?limit=20&offset=0`

Paginated history of background scans.

**Response:**
```json
{
  "scans": [
    {
      "id": 1,
      "timestamp": "2026-03-26 12:00:00",
      "overall_status": "safe",
      "score": 10
    }
  ],
  "total": 100
}
```

---

## Notifications

### `GET /api/v1/settings/notifications`

Current notification configuration.

### `PUT /api/v1/settings/notifications` 🔒

Update notification config. Webhook URLs are validated (must not target private IPs).

**Request body:**
```json
{
  "webhooks": [
    {
      "url": "https://hooks.slack.com/services/...",
      "name": "Slack",
      "events": ["escalation"]
    }
  ],
  "email_enabled": false,
  "email_address": "",
  "events": ["escalation", "weekly_summary"]
}
```

### `POST /api/v1/settings/notifications/test` 🔒

Send a test notification to a webhook URL. URL is validated before sending.

**Request:** `{"url": "https://hooks.slack.com/..."}`
**Response:** `{"success": true}`

---

## Metrics

### `GET /metrics`

Prometheus-compatible metrics in text format. Not under `/api/v1` prefix.

Available metrics:
- `clawsafe_risk_score{category="network"}` — risk score per category
- `clawsafe_overall_status` — overall status (0=safe, 1=attention, 2=risk)
- `clawsafe_scan_count` — total scans
- `clawsafe_fix_count` — total fixes applied

---

## OpenClaw Skill

### `GET /api/v1/skill/status`

Plain-language safety summary for OpenClaw skill integration.

**Response:**
```json
{
  "summary": "Important risks found. Please review these now.",
  "status": "risk",
  "score": 70,
  "top_actions": [
    "Network: People outside your home can reach OpenClaw.",
    "Tools & Skills: High-risk abilities are active."
  ]
}
```

### `GET /api/v1/skill/actions`

Top 3 recommended actions as plain strings.

---

**Legend:** 🔒 = requires `Authorization: Bearer <key>` when `CLAWSAFE_API_KEY` is set.
