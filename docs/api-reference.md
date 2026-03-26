# API Reference

Base URL: `http://localhost:8000`

Full interactive docs available at `http://localhost:8000/docs` (Swagger UI).

## Core Endpoints

### Health
- `GET /api/v1/health` — Service health check

### Status
- `GET /api/v1/status` — Overall safety status with all categories
- `GET /api/v1/status/{category}` — Single category detail (`network`, `tools`, `data`, `updates`)

### Recommendations
- `GET /api/v1/recommendations` — Suggested actions based on current risks

### Activity
- `GET /api/v1/activity?limit=20&offset=0` — Paginated activity event log

### Settings
- `GET /api/v1/settings` — User preferences
- `PUT /api/v1/settings` — Update preferences

## Fix Engine (v0.2+)

### Auto-Fix
- `POST /api/v1/fix/{action_id}` — Apply an auto-fix
- `POST /api/v1/fix/{action_id}/undo` — Undo a previously applied fix

### Backups
- `GET /api/v1/backups` — List config backups

### Policy
- `GET /api/v1/policy` — Active policy
- `PUT /api/v1/policy` — Update and activate a policy
- `POST /api/v1/policy/validate` — Validate a policy without applying

## Integrations (v0.3+)

### Scan History
- `GET /api/v1/scans?limit=20&offset=0` — Paginated scan history

### Notifications
- `GET /api/v1/settings/notifications` — Notification config
- `PUT /api/v1/settings/notifications` — Update notification config
- `POST /api/v1/settings/notifications/test` — Send test notification

### Metrics
- `GET /metrics` — Prometheus-compatible metrics

### OpenClaw Skill
- `GET /api/v1/skill/status` — Plain-language safety summary
- `GET /api/v1/skill/actions` — Top 3 recommended actions
