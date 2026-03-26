# Changelog

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
