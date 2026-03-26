# Phase 3: Integrations (v0.3)

Goal: Add OpenClaw skill integration, alerts, and monitoring exports.

Covers: FR-12, FR-13, FR-16, FR-17, FR-18.

## Tasks

### 3.1 Scheduled Scanning (Backend)

- [x] Background scheduler (APScheduler or similar)
  - Configurable interval (default: hourly)
  - Detect configuration drift between scans
- [x] Store scan history in SQLite for trend tracking
- [x] `GET /api/v1/scans` - scan history endpoint

### 3.2 Notifications & Alerts (Backend)

- [x] **Email notifications** (SMTP config in settings)
  - Risk level escalation (e.g., Safe -> At Risk)
  - Weekly safety summary (opt-in)
- [x] **Webhook notifications**
  - Slack, Discord, generic webhook URL
  - Configurable event filters
- [x] **API endpoints**
  - `GET /api/v1/settings/notifications` - notification config
  - `PUT /api/v1/settings/notifications` - update notification config
  - `POST /api/v1/settings/notifications/test` - send test notification

### 3.3 Monitoring Exports (Backend)

- [x] **Prometheus metrics endpoint** (`GET /metrics`)
  - Risk scores per category
  - Scan count, fix count, active alerts
- [x] **Structured logging** to stdout (JSON format)
  - Compatible with Loki/ELK ingestion
- [x] Document Grafana dashboard example in docs

### 3.4 OpenClaw Skill (Backend + Skill Package)

- [x] **Internal API** for skill consumption
  - `GET /api/v1/skill/status` - plain-language safety summary
  - `GET /api/v1/skill/actions` - top 3 recommended actions
- [x] **Reference OpenClaw skill** (`skill/clawsafe_skill.py`)
  - Responds to "Is it safe?" queries
  - Returns non-technical summary with suggested actions
- [x] Skill installation instructions in docs

### 3.5 Advanced Settings - Integrations Tab (Frontend)

- [x] Metrics endpoint URL display (read-only)
- [x] Log output format selector
- [x] Webhook URL configuration (add/remove/test)
- [x] Email notification settings
- [x] Notification event filter checkboxes

## Acceptance Criteria

- Scheduled scans detect config drift and log changes
- Webhook/email alerts fire on risk escalation
- Prometheus `/metrics` endpoint returns valid metrics
- OpenClaw skill answers "Is it safe?" with plain-language summary
- Integrations tab allows full webhook/email/metrics configuration
