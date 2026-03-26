# Changelog

## [1.1.0] - 2026-03-26

### Added
- API key authentication for all write endpoints
- Input validation (action IDs, webhook URLs) preventing path traversal and SSRF
- Structured JSON logging with configurable log level
- Real health check (DB connectivity + scheduler status verification)
- Policy-aware scoring: risk adjustments based on active policy rules
- Prometheus metrics actually populated during scheduled scans
- Scheduler exponential backoff on repeated failures
- Onboarding wizard connected to dashboard (shows on first visit, saves to API)
- Theme flash prevention via localStorage + inline head script
- Settings tabs save to policy API with debounced auto-save and toast feedback
- Focus trap in SideSheet modal for keyboard accessibility
- Toast notification system with role="alert" for screen readers
- Severity text labels on activity dots (not color-only)
- Error boundary (error.tsx) for graceful component crash recovery
- Polling backoff (30s → 300s) on API failures
- Non-root Docker containers with health checks and resource limits
- Production Docker overlay with Caddy reverse proxy (auto HTTPS)
- Makefile for one-command install/dev/test/build/prod
- Security documentation (auth, HTTPS, SSRF protection)
- Operations documentation (backup/restore, upgrades, monitoring, troubleshooting)
- CI: test coverage thresholds, Trivy container scanning
- Scanner and scoring edge case tests

### Changed
- CORS restricted to explicit methods/headers
- Demo data only seeded when CLAWSAFE_DEMO_MODE=true
- Backup retention auto-cleanup at 50 backups
- Settings page loads policy from API instead of using hardcoded data

## [1.0.0] - 2026-03-26

### Added
- UX polish: loading skeletons, empty/error states, mascot illustrations
- Accessibility: skip-to-content link, focus-visible outlines, ARIA labels
- Comprehensive documentation (installation, configuration, API reference, contributing)
- Additional test coverage for all components

## [0.3.0] - 2026-03-26

### Added
- Background scan scheduler with configurable interval
- Webhook notifications for risk escalation events
- Prometheus metrics endpoint (`/metrics`)
- OpenClaw skill integration (plain-language safety queries)
- Scan history tracking and API endpoint
- Integrations tab in Advanced Settings (metrics, webhooks, email)

## [0.2.0] - 2026-03-26

### Added
- One-click auto-fix engine for network, tools, data, and auth
- Config backup and restore with undo support
- Policy-as-code with YAML validation and management
- Advanced Settings page with 4 working tabs (Network, Tools, Data, Integrations)
- SettingRow component with "What this really means" tooltips

## [0.1.0] - 2026-03-26

### Added
- Initial release: FastAPI backend with security scanner and risk scoring
- Next.js frontend with dashboard, category cards, and activity feed
- Onboarding wizard (4-step setup flow)
- Fix flow with step-by-step manual instructions
- Design token system with Playful/Minimal themes and Light/Dark modes
- Docker Compose deployment with home and SMB overlays
- YAML policy files (default, home, SMB examples)
- GitHub Actions CI pipeline
