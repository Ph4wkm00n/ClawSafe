# Phase 3: Integrations (v0.3)

Goal: Add OpenClaw skill integration, alerts, and monitoring exports.

Covers: FR-12, FR-13, FR-16, FR-17, FR-18.

## Tasks

### 3.1 Scheduled Scanning (Backend)

- [ ] Background scheduler (APScheduler or similar)
  - Configurable interval (default: hourly)
  - Detect configuration drift between scans
- [ ] Store scan history in SQLite for trend tracking
- [ ] `GET /api/v1/scans` - scan history endpoint

### 3.2 Notifications & Alerts (Backend)

- [ ] **Email notifications** (SMTP config in settings)
  - Risk level escalation (e.g., Safe -> At Risk)
  - Weekly safety summary (opt-in)
- [ ] **Webhook notifications**
  - Slack, Discord, generic webhook URL
  - Configurable event filters
- [ ] **API endpoints**
  - `GET /api/v1/settings/notifications` - notification config
  - `PUT /api/v1/settings/notifications` - update notification config
  - `POST /api/v1/settings/notifications/test` - send test notification

### 3.3 Monitoring Exports (Backend)

- [ ] **Prometheus metrics endpoint** (`GET /metrics`)
  - Risk scores per category
  - Scan count, fix count, active alerts
- [ ] **Structured logging** to stdout (JSON format)
  - Compatible with Loki/ELK ingestion
- [ ] Document Grafana dashboard example in docs

### 3.4 OpenClaw Skill (Backend + Skill Package)

- [ ] **Internal API** for skill consumption
  - `GET /api/v1/skill/status` - plain-language safety summary
  - `GET /api/v1/skill/actions` - top 3 recommended actions
- [ ] **Reference OpenClaw skill** (`skill/clawsafe_skill.py`)
  - Responds to "Is it safe?" queries
  - Returns non-technical summary with suggested actions
- [ ] Skill installation instructions in docs

### 3.5 Advanced Settings - Integrations Tab (Frontend)

- [ ] Metrics endpoint URL display (read-only)
- [ ] Log output format selector
- [ ] Webhook URL configuration (add/remove/test)
- [ ] Email notification settings
- [ ] Notification event filter checkboxes

## Acceptance Criteria

- Scheduled scans detect config drift and log changes
- Webhook/email alerts fire on risk escalation
- Prometheus `/metrics` endpoint returns valid metrics
- OpenClaw skill answers "Is it safe?" with plain-language summary
- Integrations tab allows full webhook/email/metrics configuration
